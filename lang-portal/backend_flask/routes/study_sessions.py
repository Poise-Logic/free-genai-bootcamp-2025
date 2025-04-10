from flask import request, jsonify, g
from flask_cors import cross_origin
from datetime import datetime
import math

def load(app):
  # Implementation of POST /api/study_sessions endpoint
  @app.route('/api/study_sessions', methods=['POST'])
  @cross_origin()
  def create_study_session():
    try:
      # Get and validate required parameters
      data = request.get_json()
      
      if not data:
        return jsonify({"error": "No data provided"}), 400
      
      if 'group_id' not in data:
        return jsonify({"error": "group_id is required"}), 400
      
      if 'study_activity_id' not in data:
        return jsonify({"error": "study_activity_id is required"}), 400
      
      group_id = data['group_id']
      study_activity_id = data['study_activity_id']
      
      # Validate that group exists
      cursor = app.db.cursor()
      cursor.execute('SELECT id FROM groups WHERE id = ?', (group_id,))
      group = cursor.fetchone()
      
      if not group:
        return jsonify({"error": f"Group with id {group_id} not found"}), 404
      
      # Validate that study activity exists
      cursor.execute('SELECT id FROM study_activities WHERE id = ?', (study_activity_id,))
      activity = cursor.fetchone()
      
      if not activity:
        return jsonify({"error": f"Study activity with id {study_activity_id} not found"}), 404
      
      # Create a new study session
      current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
      
      cursor.execute(
        'INSERT INTO study_sessions (group_id, study_activity_id, created_at) VALUES (?, ?, ?)',
        (group_id, study_activity_id, current_time)
      )
      
      session_id = cursor.lastrowid
      app.db.commit()
      
      # Return the created study session
      return jsonify({
        "study_session": {
          "id": session_id,
          "group_id": group_id,
          "study_activity_id": study_activity_id,
          "created_at": current_time
        }
      }), 201
    except Exception as e:
      # Error handling without rollback since it's not supported
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study_sessions', methods=['GET'])
  @cross_origin()
  def get_study_sessions():
    try:
      cursor = app.db.cursor()
      
      # Get pagination parameters
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('per_page', 10, type=int)
      offset = (page - 1) * per_page

      # Get total count
      cursor.execute('''
        SELECT COUNT(*) as count 
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
      ''')
      total_count = cursor.fetchone()['count']

      # Get paginated sessions
      cursor.execute('''
        SELECT 
          ss.id,
          ss.group_id,
          g.name as group_name,
          sa.id as activity_id,
          sa.name as activity_name,
          ss.created_at,
          COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
        GROUP BY ss.id
        ORDER BY ss.created_at DESC
        LIMIT ? OFFSET ?
      ''', (per_page, offset))
      sessions = cursor.fetchall()

      return jsonify({
        'items': [{
          'id': session['id'],
          'group_id': session['group_id'],
          'group_name': session['group_name'],
          'activity_id': session['activity_id'],
          'activity_name': session['activity_name'],
          'start_time': session['created_at'],
          'end_time': session['created_at'],  # For now, just use the same time since we don't track end time
          'review_items_count': session['review_items_count']
        } for session in sessions],
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_count / per_page)
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study_sessions/<id>', methods=['GET'])
  @cross_origin()
  def get_study_session(id):
    try:
      cursor = app.db.cursor()
      
      # Get session details
      cursor.execute('''
        SELECT 
          ss.id,
          ss.group_id,
          g.name as group_name,
          sa.id as activity_id,
          sa.name as activity_name,
          ss.created_at,
          COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
        WHERE ss.id = ?
        GROUP BY ss.id
      ''', (id,))
      
      session = cursor.fetchone()
      if not session:
        return jsonify({"error": "Study session not found"}), 404

      # Get pagination parameters
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('per_page', 10, type=int)
      offset = (page - 1) * per_page

      # Get the words reviewed in this session with their review status
      cursor.execute('''
        SELECT 
          w.*,
          COALESCE(SUM(CASE WHEN wri.correct = 1 THEN 1 ELSE 0 END), 0) as session_correct_count,
          COALESCE(SUM(CASE WHEN wri.correct = 0 THEN 1 ELSE 0 END), 0) as session_wrong_count
        FROM words w
        JOIN word_review_items wri ON wri.word_id = w.id
        WHERE wri.study_session_id = ?
        GROUP BY w.id
        ORDER BY w.spanish
        LIMIT ? OFFSET ?
      ''', (id, per_page, offset))
      
      words = cursor.fetchall()

      # Get total count of words
      cursor.execute('''
        SELECT COUNT(DISTINCT w.id) as count
        FROM words w
        JOIN word_review_items wri ON wri.word_id = w.id
        WHERE wri.study_session_id = ?
      ''', (id,))
      
      total_count = cursor.fetchone()['count']

      return jsonify({
        'session': {
          'id': session['id'],
          'group_id': session['group_id'],
          'group_name': session['group_name'],
          'activity_id': session['activity_id'],
          'activity_name': session['activity_name'],
          'start_time': session['created_at'],
          'end_time': session['created_at'],  # For now, just use the same time
          'review_items_count': session['review_items_count']
        },
        'words': [{
          'id': word['id'],
          'spanish': word['spanish'],
          'pronunciation': word['pronunciation'],
          'english': word['english'],
          'correct_count': word['session_correct_count'],
          'wrong_count': word['session_wrong_count']
        } for word in words],
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_count / per_page)
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

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

  @app.route('/api/study_sessions/reset', methods=['POST'])
  @cross_origin()
  def reset_study_sessions():
    try:
      cursor = app.db.cursor()
      
      # First delete all word review items since they have foreign key constraints
      cursor.execute('DELETE FROM word_review_items')
      
      # Then delete all study sessions
      cursor.execute('DELETE FROM study_sessions')
      
      app.db.commit()
      
      return jsonify({"message": "Study history cleared successfully"}), 200
    except Exception as e:
      return jsonify({"error": str(e)}), 500