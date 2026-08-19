"""Tests for NewDB Python SDK."""

import pytest
from newdb import NewDBClient, AsyncNewDBClient
from newdb.exceptions import AuthenticationError


def test_client_init_requires_api_key():
    with pytest.raises(AuthenticationError):
        NewDBClient(api_key="")


def test_async_client_init_requires_api_key():
    with pytest.raises(AuthenticationError):
        AsyncNewDBClient(api_key="")


def test_client_namespaces_exist():
    client = NewDBClient(api_key="test_token")
    assert hasattr(client, "person")
    assert hasattr(client, "legal")
    assert hasattr(client, "foreign")
    assert hasattr(client, "property")
