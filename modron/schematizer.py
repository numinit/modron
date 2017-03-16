"""
Performs schema inference over one or more files using pandas.
"""

from collections import namedtuple
from contextlib import closing
import pandas as pd

from .requester import Requester
from .column import Column


class Schematizer:
    """
    A Schematizer is initialized with an expected set of Column instances and
    a Requester instance, and can then perform schematization on URIs retrieved
    through the Requester.
    """
    class Result(namedtuple('Result', ['columns', 'errors'])):
        """
        The result of schematization.
        """
        __slots__ = ()

    def __init__(self, columns=None, requester=None):
        """
        Initializes this Schematizer.
        Args:
            columns (list): A list of Column instances, or None to detect
                            the schema.
            requester: An optional requester, or None to use the default
                       HTTPS requester.
        """
        self._columns = columns
        self._requester = requester if requester else Requester()

    def schematize_csvs(self, uris, nrows=-1, chunk_size=1024):
        """
        Schematizes a set of URIs pointing to CSVs.
        Args:
            uris (list): A list of URIs to request.
            nrows (int): The number of rows. Pass None or less than 1 to
                         schematize the whole document.
            chunk_size (int): How many rows of the document to read in a
                              single iteration. Default is 1024.
        """
        used_cols, col_names, col_types, columns = None, None, None, None
        if self._columns is not None:
            # Get the used columns, their names, and the expected types
            used_cols = [col.idx for col in self._columns]
            col_names = [col.name for col in self._columns]
            col_types = {col.name: col.etype for col in self._columns}

            # Duplicate the stored columns
            columns = [col.clone() for col in self._columns]

        # Expand the list of URIs
        uris = list(uris)

        # If they pass a zero/negative row count, schematize the whole document
        if isinstance(nrows, int) and nrows <= 0:
            nrows = None

        # Schematize the documents
        errors = {}
        for uri, stream in self._streams_for(uris):
            try:
                reader = pd.read_csv(stream, engine='c', comment='#',
                                     nrows=nrows, usecols=used_cols,
                                     names=col_names, dtype=col_types,
                                     iterator=True, chunksize=chunk_size)
                columns = Schematizer._process_chunks(columns, reader)
            except ValueError as ex:
                # Skip this file
                errors[uri] = ex

        # Done
        return Schematizer.Result(columns, errors)

    def _streams_for(self, uris):
        """
        Returns an array of auto-closed streams for the specified
        list of URIs.
        Args:
            uris (list): A list of URIs
        """
        # Eagerly make all the requests
        all_results = [(uri, self._requester.request(uri)) for uri in uris]

        # Lazily read them
        for (uri, unclosed_result) in all_results:
            with closing(unclosed_result) as result:
                yield (uri, result)

    @staticmethod
    def _process_chunks(columns, reader):
        """
        Given a reader, process each chunk.
        """
        for chunk in reader:
            # TODO (mjones): filter the chunk

            if columns is None:
                # Let the first chunk define the expected columns
                dtypes = chunk.dtypes
                names = dtypes.index
                columns = [None] * len(dtypes)
                for idx, value in enumerate(dtypes):
                    columns[idx] = Column(idx, names[idx], value)

            if len(chunk.dtypes) != len(columns):
                # Schema mismatch for this chunk. The previous chunk
                # wasn't good enough to define the actual schema,
                # so we're essentially totally hosed here despite
                # Pandas trying its best to make sense of this terrible
                # dataset.
                raise ValueError('schema mismatch partway through file')

            # Get the datatype counts
            for idx, dtype in enumerate(chunk.dtypes):
                column = columns[idx]
                column.add_type_counts(dtype, 1)

            # TODO (mjones): store the chunk

        # Done, return the resolved columns
        return columns
