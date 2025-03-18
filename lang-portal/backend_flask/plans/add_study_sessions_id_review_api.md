# Implementation Plan: POST /api/study_sessions/:id/review Endpoint

## Overview
This document outlines the implementation plan for the `POST /api/study_sessions/:id/review` endpoint. This endpoint will allow users to submit multiple word reviews for a specific study session in batch, recording whether each word was answered correctly or incorrectly.

## Requirements
Based on the Backend Technical Specs:
- The endpoint is `POST /api/study_sessions/:id/review`
- It creates multiple word review entries in batch for a specific study session
- The endpoint accepts a study session ID in the URL parameter
- The request payload contains an array of reviews with word_id and is_correct properties
- The response includes success status, message, study session ID, review count, and creation timestamp

## Implementation Tasks

### Task 1: Add POST /api/study_sessions/:id/review endpoint
Add the endpoint to the `study_sessions.py` file to handle batch review submissions.

```python
# Implementation task for adding the review endpoint
@app.route('/api/study_sessions/<id>/review', methods=['POST'])
@cross_origin()
def batch_submit_reviews(id):
    """
    Endpoint to submit multiple word reviews for a study session in batch.
    
    Args:
        id: The study session ID
        
    Request Body:
        {
            "reviews": [
                {
                    "word_id": 1,
                    "is_correct": true
                },
                {
                    "word_id": 2,
                    "is_correct": false
                }
            ]
        }
    
    Returns:
        JSON response with success status, message, study session ID, 
        review count, and creation timestamp
    """
    try:
        # Get and validate the request data
        data = request.get_json()
        
        # Verify study session exists
        cursor = app.db.cursor()
        cursor.execute('SELECT id FROM study_sessions WHERE id = ?', (id,))
        session = cursor.fetchone()
        
        if not session:
            return jsonify({"error": f"Study session with id {id} not found"}), 404
        
        # Validate request payload
        if not data or 'reviews' not in data or not isinstance(data['reviews'], list):
            return jsonify({"error": "Invalid request format. 'reviews' array is required"}), 400
        
        if not data['reviews']:
            return jsonify({"error": "Reviews array cannot be empty"}), 400
        
        # Create word review items
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        reviews_count = 0
        
        for review in data['reviews']:
            # Validate review object
            if 'word_id' not in review or 'is_correct' not in review:
                return jsonify({"error": "Each review must have 'word_id' and 'is_correct' fields"}), 400
            
            word_id = review['word_id']
            is_correct = review['is_correct']
            
            # Verify word exists
            cursor.execute('SELECT id FROM words WHERE id = ?', (word_id,))
            word = cursor.fetchone()
            
            if not word:
                return jsonify({"error": f"Word with id {word_id} not found"}), 404
            
            # Insert review record
            cursor.execute(
                'INSERT INTO word_review_items (word_id, study_session_id, correct, created_at) VALUES (?, ?, ?, ?)',
                (word_id, id, 1 if is_correct else 0, current_time)
            )
            reviews_count += 1
        
        app.db.commit()
        
        return jsonify({
            "success": True,
            "message": "Reviews submitted successfully",
            "study_session_id": int(id),
            "review_count": reviews_count,
            "created_at": current_time
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### Task 2: Write Tests for the Endpoint

Create a test file to validate the endpoint's functionality:

```python
# Implementation task for testing the review endpoint
import pytest
import json
from app import create_app

@pytest.fixture
def client():
    app = create_app(':memory:')
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Set up test data (study session and words)
            cursor = app.db.cursor()
            
            # Create words
            cursor.execute('INSERT INTO words (id, spanish, english, parts) VALUES (1, "hablar", "to speak", "{\\"stem\\": \\"habl\\", \\"ending\\": \\"ar\\", \\"type\\": \\"regular verb\\"}")')
            cursor.execute('INSERT INTO words (id, spanish, english, parts) VALUES (2, "comer", "to eat", "{\\"stem\\": \\"com\\", \\"ending\\": \\"er\\", \\"type\\": \\"regular verb\\"}")')
            
            # Create a group
            cursor.execute('INSERT INTO groups (id, name) VALUES (1, "Test Group")')
            
            # Create a study activity
            cursor.execute('INSERT INTO study_activities (id, name, url) VALUES (1, "Test Activity", "http://test.com")')
            
            # Create a study session
            cursor.execute('INSERT INTO study_sessions (id, group_id, study_activity_id, created_at) VALUES (1, 1, 1, "2025-03-18T10:00:00Z")')
            
            app.db.commit()
            
        yield client

def test_batch_submit_reviews_success(client):
    """Test successful batch submission of reviews"""
    # Prepare test data
    review_data = {
        "reviews": [
            {
                "word_id": 1,
                "is_correct": True
            },
            {
                "word_id": 2,
                "is_correct": False
            }
        ]
    }
    
    # Send request
    response = client.post('/api/study_sessions/1/review', 
                          data=json.dumps(review_data),
                          content_type='application/json')
    
    # Verify response
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['message'] == "Reviews submitted successfully"
    assert data['study_session_id'] == 1
    assert data['review_count'] == 2
    assert 'created_at' in data
    
    # Verify data was added to database
    cursor = client.application.db.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM word_review_items WHERE study_session_id = 1')
    count = cursor.fetchone()['count']
    assert count == 2
    
    cursor.execute('SELECT correct FROM word_review_items WHERE word_id = 1')
    correct_value = cursor.fetchone()['correct']
    assert correct_value == 1  # True
    
    cursor.execute('SELECT correct FROM word_review_items WHERE word_id = 2')
    correct_value = cursor.fetchone()['correct']
    assert correct_value == 0  # False

def test_batch_submit_reviews_session_not_found(client):
    """Test submitting reviews for non-existent session"""
    review_data = {
        "reviews": [
            {
                "word_id": 1,
                "is_correct": True
            }
        ]
    }
    
    response = client.post('/api/study_sessions/999/review', 
                          data=json.dumps(review_data),
                          content_type='application/json')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert 'not found' in data['error']

def test_batch_submit_reviews_invalid_word(client):
    """Test submitting reviews with non-existent word"""
    review_data = {
        "reviews": [
            {
                "word_id": 999,
                "is_correct": True
            }
        ]
    }
    
    response = client.post('/api/study_sessions/1/review', 
                          data=json.dumps(review_data),
                          content_type='application/json')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert 'not found' in data['error']

def test_batch_submit_reviews_invalid_format(client):
    """Test submitting reviews with invalid format"""
    # Missing reviews array
    response = client.post('/api/study_sessions/1/review', 
                          data=json.dumps({}),
                          content_type='application/json')
    
    assert response.status_code == 400
    
    # Empty reviews array
    response = client.post('/api/study_sessions/1/review', 
                          data=json.dumps({"reviews": []}),
                          content_type='application/json')
    
    assert response.status_code == 400
    
    # Missing required fields
    response = client.post('/api/study_sessions/1/review', 
                          data=json.dumps({"reviews": [{"word_id": 1}]}),
                          content_type='application/json')
    
    assert response.status_code == 400
```

## Integration Steps

1. Add the implementation to `routes/study_sessions.py`
2. Create the test file in `tests/test_study_sessions_review.py`
3. Run tests to verify the implementation
4. Update the README.md file if necessary to document the new endpoint

## Considerations

- We're storing the correct/incorrect status as 1/0 in the SQLite database
- We're validating that both the study session and words exist before creating reviews
- We're handling batch operations in a single database transaction
- Error handling is implemented for common edge cases

## Testing Strategy

- Unit tests for successful review submissions
- Tests for validation of study session existence
- Tests for validation of word existence
- Tests for invalid request formats
- Integration testing with existing endpoints

## Completion Criteria

- All implementation tasks are completed
- All tests pass
- The API behaves according to specifications
- Code follows project conventions
