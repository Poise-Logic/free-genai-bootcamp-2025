# Implementation Plan: GET /groups/:id/words/raw Endpoint

## Overview
This plan outlines the implementation of a new endpoint `GET /groups/:id/words/raw` that will return the raw data for all words in a specific group.

## Background and Purpose
This endpoint will provide raw word data for a specific group, including the complete `parts` JSON field which is needed for certain learning applications. Unlike the existing `/groups/:id/words` endpoint which returns processed data with pagination, this endpoint will return all words in their raw format without pagination.

## Technical Specifications

### Endpoint:
```
GET /groups/:id/words/raw
```

### Path Parameters:
- `id` - The ID of the group to get words from

### Response Format:
```json
{
  "words": [
    {
      "id": 1,
      "kanji": "払う",
      "romaji": "harau",
      "english": "to pay",
      "parts": [
        { "kanji": "払", "romaji": ["ha","ra"] },
        { "kanji": "う", "romaji": ["u"] }
      ]
    },
    // More words...
  ]
}
```

## Implementation Tasks

### Task 1: Add the new endpoint to groups.py
- Add a new route handler for `GET /groups/:id/words/raw`
- Implement database query to fetch all words in a group with their complete data
- Return raw word data including the parsed JSON parts field
- Handle error cases (group not found, server errors)

### Task 2: Write tests for the new endpoint
- Test successful retrieval of words from a valid group
- Test response when group doesn't exist
- Test response when group exists but has no words

## Implementation Details

### Task 1: Add the new endpoint to groups.py
This endpoint will be added to the existing `groups.py` file, which already contains routes for group-related endpoints. The implementation will:

1. Query the database to verify the group exists
2. Join the `words` and `word_groups` tables to get all words for the group
3. Parse the `parts` field from JSON string to a Python object
4. Return the complete word data without pagination

```python
@app.route('/groups/<int:id>/words/raw', methods=['GET'])
@cross_origin()
def get_group_words_raw(id):
  try:
    cursor = app.db.cursor()
    
    # First, check if the group exists
    cursor.execute('SELECT name FROM groups WHERE id = ?', (id,))
    group = cursor.fetchone()
    if not group:
      return jsonify({"error": "Group not found"}), 404
    
    # Query to fetch all words in the group with their complete data
    cursor.execute('''
      SELECT w.*
      FROM words w
      JOIN word_groups wg ON w.id = wg.word_id
      WHERE wg.group_id = ?
    ''', (id,))
    
    words = cursor.fetchall()
    
    # Format the response with parsed parts field
    words_data = []
    for word in words:
      parts = json.loads(word["parts"])
      words_data.append({
        "id": word["id"],
        "kanji": word["kanji"],
        "romaji": word["romaji"],
        "english": word["english"],
        "parts": parts
      })
    
    return jsonify({
      'words': words_data
    })
  except Exception as e:
    return jsonify({"error": str(e)}), 500
```

### Task 2: Write tests for the new endpoint
Test the endpoint's functionality with pytest:

```python
def test_get_group_words_raw_success(client, app):
    # Test successful retrieval of words from a valid group
    response = client.get('/groups/1/words/raw')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'words' in data
    assert isinstance(data['words'], list)
    for word in data['words']:
        assert 'id' in word
        assert 'kanji' in word
        assert 'romaji' in word
        assert 'english' in word
        assert 'parts' in word
        assert isinstance(word['parts'], list)

def test_get_group_words_raw_group_not_found(client, app):
    # Test response when group doesn't exist
    response = client.get('/groups/999/words/raw')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Group not found'

def test_get_group_words_raw_empty_group(client, app, create_empty_group):
    # Test response when group exists but has no words
    group_id = create_empty_group()
    response = client.get(f'/groups/{group_id}/words/raw')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'words' in data
    assert len(data['words']) == 0
```

## Conclusion
This endpoint will provide access to the raw word data for a specific group, including the complete parts field in JSON format. It differs from the existing `/groups/:id/words` endpoint by returning all words without pagination and including the full parts data.
