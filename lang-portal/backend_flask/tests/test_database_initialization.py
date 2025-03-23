import os
import json
import sqlite3
import subprocess
import tempfile

def test_database_initialization():
    """Test that the database initializes correctly with Spanish data."""
    # Create a temporary database file for testing
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    
    try:
        # Set environment variable to use the test database
        os.environ["DATABASE_PATH"] = db_path
        
        # Run the database initialization command
        result = subprocess.run(
            ["uv", "run", "-m", "invoke", "init-db"],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Check if the command executed successfully
        assert result.returncode == 0, f"Database initialization failed with error: {result.stderr}"
        
        # Connect to the database to verify data
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if words table exists and has Spanish columns
        cursor.execute("PRAGMA table_info(words)")
        columns = {row["name"] for row in cursor.fetchall()}
        assert "spanish" in columns, "Column 'spanish' not found in words table"
        assert "pronunciation" in columns, "Column 'pronunciation' not found in words table"
        
        # Check if data was loaded properly
        cursor.execute("SELECT COUNT(*) as count FROM words")
        word_count = cursor.fetchone()["count"]
        assert word_count > 0, "No words were loaded into the database"
        
        # Check sample Spanish words
        cursor.execute("SELECT * FROM words LIMIT 5")
        words = cursor.fetchall()
        for word in words:
            # Ensure all words have Spanish and pronunciation data
            assert word["spanish"], f"Word with ID {word['id']} has empty spanish field"
            assert word["pronunciation"], f"Word with ID {word['id']} has empty pronunciation field"
            
            # Verify parts structure for Spanish
            parts = json.loads(word["parts"])
            assert isinstance(parts, list), f"Word parts for {word['spanish']} is not a list"
            for part in parts:
                assert "spanish" in part, f"Part in {word['spanish']} missing 'spanish' field"
                assert "pronunciation" in part, f"Part in {word['spanish']} missing 'pronunciation' field"
        
        # Check groups were created
        cursor.execute("SELECT COUNT(*) as count FROM groups")
        group_count = cursor.fetchone()["count"]
        assert group_count > 0, "No groups were created in the database"
        
        # Check word-group relationships
        cursor.execute("SELECT COUNT(*) as count FROM word_groups")
        word_group_count = cursor.fetchone()["count"]
        assert word_group_count > 0, "No word-group relationships were created"
        
        # Verify word groups have correct word counts
        cursor.execute("""
            SELECT g.id, g.name, g.words_count, COUNT(wg.word_id) as actual_count
            FROM groups g
            LEFT JOIN word_groups wg ON g.id = wg.group_id
            GROUP BY g.id
        """)
        
        for group in cursor.fetchall():
            assert group["words_count"] == group["actual_count"], \
                f"Group '{group['name']}' has incorrect word count: {group['words_count']} vs {group['actual_count']}"
        
    finally:
        # Clean up test database
        os.unlink(db_path)
        if "DATABASE_PATH" in os.environ:
            del os.environ["DATABASE_PATH"] 