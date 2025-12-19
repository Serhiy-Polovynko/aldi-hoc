from unittest.mock import patch, MagicMock
from aldi_hoc_companion.db.queries import list_campaigns


def test_list_campaigns_returns_project_objects():
    """
    Test list_campaigns() without touching a real database.
    We mock:
      - get_connection()
      - cursor.execute()
      - cursor.fetchall()
    """

    # Fake DB rows returned by fetchall()
    fake_rows = [
        {
            "campaign_id": "8240-003179",
            "campaign_name": "Kwaliteitscampagne",
            "campaign_year": 2025,
        },
        {
            "campaign_id": "8240-001234",
            "campaign_name": "Zomercampagne",
            "campaign_year": 2024,
        },
    ]

    fake_cursor = MagicMock()
    fake_cursor.fetchall.return_value = fake_rows

    fake_conn = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor

    # Patch get_connection to return our fake connection
    with patch("aldi_hoc_companion.db.queries.get_connection", return_value=fake_conn):
        campaigns = list_campaigns(limit=2)

    # The function should return 2 Project objects
    assert len(campaigns) == 2

    c1 = campaigns[0]
    c2 = campaigns[1]

    assert c1.campaign_id == "8240-003179"
    assert c1.campaign_name == "Kwaliteitscampagne"
    assert c1.campaign_year == 2025

    assert c2.campaign_id == "8240-001234"
    assert c2.campaign_name == "Zomercampagne"
    assert c2.campaign_year == 2024

    # Ensure DB was actually used
    fake_cursor.execute.assert_called_once()
    fake_cursor.fetchall.assert_called_once()
