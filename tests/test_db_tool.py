import pytest
from WeddingAgentPy import query_playlist_db

def test_db_is_reachable():
    """Chinook.db must be present and queryable on the CI runner."""
    result = query_playlist_db.invoke("SELECT 1 AS alive")
    assert "Error" not in result, f"DB unreachable: {result}"

def test_playlist_table_exists():
    """The Playlist table must exist in the Chinook schema."""
    result = query_playlist_db.invoke(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='Playlist'"
    )
    assert "Playlist" in result, (
        "Playlist table not found. Is resources/Chinook.db present?"
    )

def test_genre_table_has_data():
    """Genre table must contain at least one row."""
    result = query_playlist_db.invoke("SELECT COUNT(*) FROM Genre")
    assert "Error" not in result

    # Strip brackets, parens, spaces and grab the number
    count = int(result.strip().strip("[]").strip("()").split(",")[0].strip())
    assert count > 0, f"Expected at least 1 genre, got {count}"

def test_rock_genre_exists():
    """
    Chinook has a 'Rock' genre. If missing, the agent's playlist
    recommendations for rock-adjacent genres won't work.
    """
    result = query_playlist_db.invoke(
        "SELECT Name FROM Genre WHERE Name LIKE '%Rock%'"
    )
    assert "Rock" in result, (
        "Expected Rock genre in Chinook.db. DB may be corrupt or wrong version."
    )


def test_invalid_query_returns_error_gracefully():
    """
    The query_playlist_db tool must not crash on bad SQL —
    it should return an error string (see the try/except in WeddingAgentPy).
    """
    result = query_playlist_db.invoke("SELECT * FROM NonExistentTable")
    assert "Error" in result, (
        "Expected graceful error string for invalid query, got: " + result
    )
