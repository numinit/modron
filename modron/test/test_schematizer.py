import os.path as path
import pytest
import httpretty

from modron import schematizer
from modron import requester


def mock_csv_data(name):
    root = path.abspath(path.dirname(__file__))
    with open(path.join(root, 'test_schematizer', '%s.csv' % name), 'rb') as f:
        return f.read()


def mock_sas_uris():
    uri_to_data = {}
    files = ['bestiary_1', 'bestiary_2', 'bestiary_3', 'bestiary_4']
    for file in files:
        fmt = 'https://modron.blob.core.windows.net/container/bucket/%s.csv'
        uri = requester.Requester.normalize_uri(fmt % file)
        data = mock_csv_data(file)
        uri_to_data[uri] = data

    httpretty.HTTPretty.allow_net_connect = False
    for uri, data in uri_to_data.items():
        httpretty.register_uri(
            httpretty.GET,
            uri,
            body=data,
            content_type='text/csv'
        )
    return uri_to_data


@httpretty.activate
def test_schematize_blind():
    items = mock_sas_uris()
    s = schematizer.Schematizer()
    result = s.schematize_csvs(items.keys())
