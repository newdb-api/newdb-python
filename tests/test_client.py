"""Tests for NewDB Python SDK."""

import unittest
from unittest.mock import Mock
from newdb import NewDBClient, AsyncNewDBClient
from newdb.exceptions import AuthenticationError


class TestNewDBClient(unittest.TestCase):
    def test_client_init_requires_api_key(self):
        with self.assertRaises(AuthenticationError):
            NewDBClient(api_key="")

    def test_async_client_init_requires_api_key(self):
        with self.assertRaises(AuthenticationError):
            AsyncNewDBClient(api_key="")

    def test_client_namespaces_exist(self):
        client = NewDBClient(api_key="test_token")
        self.assertTrue(hasattr(client, "person"))
        self.assertTrue(hasattr(client, "legal"))
        self.assertTrue(hasattr(client, "foreign"))
        self.assertTrue(hasattr(client, "property"))

    def test_client_test_mode(self):
        client = NewDBClient(test_mode=True)
        self.assertTrue(client.test_mode)
        self.assertEqual(client.base_url, "https://api.newdb.net/test/v2")
        self.assertEqual(client.api_key, "test_token_newdb_sandbox")

    def test_client_property_methods(self):
        client = NewDBClient(api_key="test_token")
        self.assertTrue(hasattr(client.property, "check_intellectual_property"))
        self.assertTrue(hasattr(client.property, "check_vin"))
        self.assertTrue(hasattr(client.property, "check_rosreestr"))

    def test_client_person_methods(self):
        client = NewDBClient(api_key="test_token")
        self.assertTrue(hasattr(client.person, "check_fssp"))
        self.assertTrue(hasattr(client.person, "check_court_arbitration"))
        self.assertTrue(hasattr(client.person, "check_arbitr_debt_sum"))
        self.assertTrue(hasattr(client.person, "check_fssp_company"))
        self.assertTrue(hasattr(client.person, "check_opensanctions"))

    def test_opensanctions_helper_builds_exact_filter_request(self):
        client = NewDBClient(api_key="test_token")
        client.execute = Mock(return_value={"state": "queued"})

        client.person.check_opensanctions(
            query="ИВАНОВ ИВАН ИВАНОВИЧ",
            inn="500100732259",
            birth_date="1980-01-01",
            max_results=10,
        )

        client.execute.assert_called_once_with({
            "method": "opensanctions",
            "query": "ИВАНОВ ИВАН ИВАНОВИЧ",
            "inn": "500100732259",
            "birth_date": "1980-01-01",
            "max_results": 10,
            "country": "ru",
        })


if __name__ == "__main__":
    unittest.main()
