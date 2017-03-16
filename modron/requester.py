"""
A base class for making requests.
"""

import urllib.parse as urlparse
import requests

import modron.version as version


class Requester:
    """
    A base class for making requests.
    Should override the `request(self, uri)` method, which should
    return an I/O stream for the requested file.
    """
    def request(self, uri):
        """
        Makes the request. Will raise a ValueError on an invalid URI.
        Args:
            uri (str): The URI
        """
        # Normalize the URI
        normalized = Requester.normalize_uri(uri)

        # Create a new session
        session = requests.Session()
        session.headers.update({
            'User-Agent': '%s/%s' % (
                version.__package__, version.__version__
            ),
            'X-Requested-With': version.__ident__
        })

        # Download it as streaming data
        response = session.get(normalized, stream=True)

        # Set raw_read up so it decodes content
        # XXX: would use functools.partial here, but the linter explodes
        old_raw_read = response.raw.read

        def raw_read(*args, **kw):
            """Performs a raw read while decoding the content."""
            kw['decode_content'] = True
            return old_raw_read(*args, **kw)

        response.raw.read = raw_read
        return response.raw

    @classmethod
    def normalize_uri(cls, uri, schemes=('https',)):
        """
        Normalizes the provided URI and checks it against the whitelist
        `schemes`. Returns the normalized URI as a string.
        Args:
            uri (str): The URI
            schemes (list): The supported schemes
        """
        parsed = urlparse.urlsplit(uri)
        if parsed.scheme not in schemes:
            raise ValueError('invalid URI scheme `%s`' % parsed.scheme)
        return parsed.geturl()
