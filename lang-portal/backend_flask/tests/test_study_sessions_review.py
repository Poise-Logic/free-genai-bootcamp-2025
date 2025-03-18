import json

def test_batch_submit_reviews_success(client, app):
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
    with app.app_context():
        conn = app.db
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM word_review_items WHERE study_session_id = 1')
        count = cursor.fetchone()['count']
        assert count == 2
        
        cursor.execute('SELECT correct FROM word_review_items WHERE word_id = 1 AND study_session_id = 1')
        correct_value = cursor.fetchone()['correct']
        assert correct_value == 1  # True
        
        cursor.execute('SELECT correct FROM word_review_items WHERE word_id = 2 AND study_session_id = 1')
        correct_value = cursor.fetchone()['correct']
        assert correct_value == 0  # False

def test_batch_submit_reviews_session_not_found(client, app):
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

def test_batch_submit_reviews_invalid_word(client, app):
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

def test_batch_submit_reviews_invalid_format(client, app):
    """Test submitting reviews with invalid format"""
    # Missing reviews array
    response = client.post('/api/study_sessions/1/review', 
                          data=json.dumps({}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    
    # Empty reviews array
    response = client.post('/api/study_sessions/1/review', 
                          data=json.dumps({"reviews": []}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    
    # Missing required fields
    response = client.post('/api/study_sessions/1/review', 
                          data=json.dumps({"reviews": [{"word_id": 1}]}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
