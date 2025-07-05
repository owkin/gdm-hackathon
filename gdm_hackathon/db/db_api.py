"""
Flask API to expose the LocalDatabase as a web service.
"""

from flask import Flask, request, jsonify
from .local_db import LocalDatabase
import os

app = Flask(__name__)

# Initialize the database
db = LocalDatabase("api_db.json")

@app.route('/health', methods=['GET'])
def health_check():
    """Check if the database is healthy."""
    return jsonify({
        'healthy': db.is_healthy(),
        'total_keys': len(db.keys),
        'total_entries': len(db.data)
    })

@app.route('/keys', methods=['GET'])
def get_keys():
    """Get all keys in the database."""
    return jsonify({
        'keys': db.keys,
        'count': len(db.keys)
    })

@app.route('/cache/<key>', methods=['GET'])
def check_key_in_cache(key):
    """Check if a key exists in the database."""
    return jsonify({
        'key': key,
        'exists': db.is_key_in_cache(key)
    })

@app.route('/entry/<key>', methods=['GET'])
def get_key(key):
    """Get the entry for a specific key."""
    entry = db.get_key(key)
    if entry is None:
        return jsonify({'error': 'Key not found'}), 404
    return jsonify({
        'key': key,
        'entry': entry
    })

@app.route('/entry/<key>', methods=['POST'])
def set_key(key):
    """Add or update an entry in the database."""
    try:
        entry = request.get_json()
        if entry is None:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        success = db.set_key(key, entry)
        if success:
            return jsonify({
                'key': key,
                'success': True,
                'message': 'Entry added/updated successfully'
            })
        else:
            return jsonify({'error': 'Failed to add/update entry'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/best', methods=['GET'])
def get_best_entry():
    """Get the entry with the highest accuracy."""
    best = db.get_best_entry()
    if best is None:
        return jsonify({'error': 'No entries in database'}), 404
    
    key, entry = best
    return jsonify({
        'best_key': key,
        'best_entry': entry,
        'accuracy': entry.get('accuracy', 0.0)
    })

@app.route('/entries', methods=['GET'])
def get_all_entries():
    """Get all entries in the database."""
    return jsonify({
        'entries': db.get_all_entries(),
        'count': len(db.data)
    })

@app.route('/entries/sorted', methods=['GET'])
def get_sorted_entries():
    """Get all entries sorted by accuracy (highest first)."""
    sorted_entries = db.get_accuracy_sorted_entries()
    return jsonify({
        'entries': [{'key': key, 'entry': entry} for key, entry in sorted_entries],
        'count': len(sorted_entries)
    })

@app.route('/clear', methods=['POST'])
def clear_database():
    """Clear all data from the database."""
    db.clear()
    return jsonify({
        'success': True,
        'message': 'Database cleared successfully'
    })

@app.route('/', methods=['GET'])
def index():
    """API documentation."""
    return jsonify({
        'message': 'Local Database API',
        'endpoints': {
            'GET /health': 'Check database health',
            'GET /keys': 'Get all keys',
            'GET /cache/<key>': 'Check if key exists',
            'GET /entry/<key>': 'Get entry for key',
            'POST /entry/<key>': 'Add/update entry for key',
            'GET /best': 'Get best entry by accuracy',
            'GET /entries': 'Get all entries',
            'GET /entries/sorted': 'Get entries sorted by accuracy',
            'POST /clear': 'Clear database'
        },
        'example_usage': {
            'add_entry': 'POST /entry/patient_001 with JSON body: {"name": "John", "accuracy": 0.95}',
            'get_entry': 'GET /entry/patient_001',
            'get_best': 'GET /best'
        }
    })

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    print(f"Starting Local Database API on port {port}")
    print(f"API will be available at: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=port, debug=True) 