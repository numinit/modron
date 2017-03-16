"""
Defines the state of a column for the data cleaner, including
the column index, the name, the expected type, and the discovered
types.
"""

from collections import namedtuple
import copy
import inspect


class Column(namedtuple('Column', ['idx', 'name', 'etype', 'atype'])):
    """
    A column. Inherits from namedtuple.
    """
    __slots__ = ()

    def __new__(cls, idx, name, etype=object, atype=None):
        """
        Constructs a column.
        Args:
            idx (int): The zero-based column index.
            name (str): The column name.
            etype (class|str): The expected type.

        """
        if not atype:
            atype = dict()
        return super(Column, cls).__new__(cls, idx, name, etype, atype)

    @property
    def expected_type(self):
        """
        Returns the expected type of the column.
        """
        return self.etype

    @property
    def actual_types(self):
        """
        Returns a dict mapping actual types to number of occurrences.
        """
        return self.atype

    def clone(self):
        """
        Clones this column, returning a deeply copied instance.
        """
        return self.__class__.__new__(
            self.__class__, self.idx, self.name,
            self.etype, copy.deepcopy(self.atype)
        )

    def add_type_counts(self, dtype, count):
        """
        Adds `count` to the counter for `dtype`.
        Args:
            count (int): A natural number
        """
        if count <= 0:
            raise ValueError('invalid count')
        if dtype not in self.atype:
            self.atype[dtype] = 0
        self.atype[dtype] += count

    @staticmethod
    def stringify_dtype(dtype):
        """
        Converts a data type to a string.
        Experimental API for now.
        """
        ret = None
        if inspect.isclass(dtype):
            ret = dtype.__name__
        else:
            ret = str(dtype)
        return ret
