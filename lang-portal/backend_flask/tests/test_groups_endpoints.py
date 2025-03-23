import json

def test_get_group_words_raw_success(client, app):
    """Test successful retrieval of words from a valid group."""
    response = client.get('/groups/1/words/raw')
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert 'words' in data
    assert isinstance(data['words'], list)
    assert len(data['words']) == 2  # We inserted 2 words in the test group
    
    # Check structure of the first word
    word = data['words'][0]
    assert 'id' in word
    assert 'spanish' in word
    assert 'pronunciation' in word
    assert 'english' in word
    assert 'parts' in word
    assert isinstance(word['parts'], list)
    
    # Check specific values
    assert word['spanish'] == 'pagar'
    assert word['pronunciation'] == 'pah-GAR'
    assert word['english'] == 'to pay'
    assert len(word['parts']) == 2
    assert word['parts'][0]['spanish'] == 'pag'
    assert word['parts'][0]['pronunciation'] == ['pah', 'g']
    assert word['parts'][1]['spanish'] == 'ar'
    assert word['parts'][1]['pronunciation'] == ['ar']


def test_get_group_words_raw_group_not_found(client, app):
    """Test response when group doesn't exist."""
    response = client.get('/groups/999/words/raw')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Group not found'


def test_get_group_words_raw_empty_group(client, app):
    """Test response when group exists but has no words."""
    # Use the existing empty group (ID 2)
    response = client.get('/groups/2/words/raw')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'words' in data
    assert len(data['words']) == 0


def test_get_group_words_raw_dynamic_empty_group(client, app, create_empty_group):
    """Test response with a dynamically created empty group."""
    group_id = create_empty_group()
    response = client.get(f'/groups/{group_id}/words/raw')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'words' in data
    assert len(data['words']) == 0
