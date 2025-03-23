import os
import tempfile
import pytest
import json
import sqlite3

from app import create_app


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Create the database and load test data
    with app.app_context():
        init_test_database(app)
    
    yield app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def init_test_database(app):
    """Initialize the test database with schema and test data."""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    
    # Create tables
    conn.execute('''
    CREATE TABLE IF NOT EXISTS words (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      spanish TEXT NOT NULL,
      pronunciation TEXT NOT NULL,
      english TEXT NOT NULL,
      parts TEXT NOT NULL
    )
    ''')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS groups (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      words_count INTEGER DEFAULT 0
    )
    ''')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS word_groups (
      word_id INTEGER NOT NULL,
      group_id INTEGER NOT NULL,
      FOREIGN KEY (word_id) REFERENCES words(id),
      FOREIGN KEY (group_id) REFERENCES groups(id)
    )
    ''')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS study_activities (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      url TEXT NOT NULL
    )
    ''')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS study_sessions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      group_id INTEGER NOT NULL,
      study_activity_id INTEGER NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (group_id) REFERENCES groups(id),
      FOREIGN KEY (study_activity_id) REFERENCES study_activities(id)
    )
    ''')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS word_review_items (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      word_id INTEGER NOT NULL,
      study_session_id INTEGER NOT NULL,
      correct BOOLEAN NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (word_id) REFERENCES words(id),
      FOREIGN KEY (study_session_id) REFERENCES study_sessions(id)
    )
    ''')
    
    # Insert test data
    # Add a group
    conn.execute("INSERT INTO groups (name, words_count) VALUES (?, ?)", 
                 ("Test Group", 2))
    
    # Add words with parts as JSON
    word1_parts = json.dumps([
        {"spanish": "pag", "pronunciation": ["pah", "g"]},
        {"spanish": "ar", "pronunciation": ["ar"]}
    ])
    
    word2_parts = json.dumps([
        {"spanish": "i", "pronunciation": ["ee"]},
        {"spanish": "r", "pronunciation": ["r"]}
    ])
    
    conn.execute("INSERT INTO words (spanish, pronunciation, english, parts) VALUES (?, ?, ?, ?)",
                 ("pagar", "pah-GAR", "to pay", word1_parts))
    
    conn.execute("INSERT INTO words (spanish, pronunciation, english, parts) VALUES (?, ?, ?, ?)",
                 ("ir", "EER", "to go", word2_parts))
    
    # Add word-group relationships
    conn.execute("INSERT INTO word_groups (word_id, group_id) VALUES (1, 1)")
    conn.execute("INSERT INTO word_groups (word_id, group_id) VALUES (2, 1)")
    
    # Add an empty group for testing
    conn.execute("INSERT INTO groups (name, words_count) VALUES (?, ?)", 
                 ("Empty Group", 0))
    
    # Add study activities
    conn.execute("INSERT INTO study_activities (name, url) VALUES (?, ?)",
                ("Flashcards", "http://example.com/flashcards"))
    
    conn.execute("INSERT INTO study_activities (name, url) VALUES (?, ?)",
                ("Quiz", "http://example.com/quiz"))
    
    # Add a study session
    conn.execute("INSERT INTO study_sessions (id, group_id, study_activity_id, created_at) VALUES (?, ?, ?, ?)",
                (1, 1, 1, "2025-03-18T10:00:00Z"))
    
    conn.commit()
    conn.close()


@pytest.fixture
def create_empty_group(app):
    """Fixture to create an empty group and return its ID."""
    def _create_empty_group():
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO groups (name, words_count) VALUES (?, ?)", 
                     ("Dynamic Empty Group", 0))
        group_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return group_id
    
    return _create_empty_group
