import pytest
import httpretty

from modron import requester


def test_normalize_uri_1():
    uri = 'HTTPS://google.com/?query#fragment'
    normalized = requester.Requester.normalize_uri(uri)
    assert normalized == 'https://google.com/?query#fragment'


def test_normalize_uri_2():
    uri = 'ftp://anonymous:toukmond@foo/bar/baz'
    normalized = requester.Requester.normalize_uri(uri, ['ftp'])
    assert normalized == uri


def test_normalize_uri_invalid_1():
    uri = 'file:///etc/passwd'
    with pytest.raises(ValueError):
        requester.Requester.normalize_uri(uri)


def test_normalize_uri_invalid_2():
    uri = 'http://google.com'
    with pytest.raises(ValueError):
        requester.Requester.normalize_uri(uri)


def mock_sas_uri():
    uri = 'https://modron.blob.core.windows.net/container/bucket/file.csv'
    httpretty.HTTPretty.allow_net_connect = False
    httpretty.register_uri(
        httpretty.GET,
        uri,
        body=b'some data',
        content_type='text/csv'
    )
    return uri


@httpretty.activate
def test_mock_request():
    uri = mock_sas_uri()
    r = requester.Requester()
    result = r.request(uri)
    assert result.read() == b'some data'
