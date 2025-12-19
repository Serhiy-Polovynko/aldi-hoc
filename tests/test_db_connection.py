from unittest.mock import patch, MagicMock
from aldi_hoc_companion.db.connection import get_connection


def test_get_connection_returns_psycopg_connection():
    """
    Simple test:
    - Mock psycopg2.connect
    - Ensure get_connection() calls it
    - Ensure the returned object is what psycopg2.connect() returned
    """

    fake_conn = MagicMock()

    # Patch psycopg2.connect inside our module
    with patch("aldi_hoc_companion.db.connection.psycopg2.connect", return_value=fake_conn) as mock_connect:
        conn = get_connection()

        # psycopg2.connect must be called exactly once
        mock_connect.assert_called_once()

        # get_connection must return the fake connection
        assert conn is fake_conn
