from flask import Flask, render_template, jsonify, request
import json
import os
from database import db

app = Flask(__name__, template_folder='templates', static_folder='static')

def load_metadata():
    """Load metadata from JSON file in deploy directory"""
    metadata_path = os.path.join(os.path.dirname(__file__), '..', 'deploy', 'metadata.json')
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "site": {"name": "FinTrack", "description": "Financial tracking platform for startups"},
            "navigation": {"main": [], "auth": []},
            "footer": {"links": [], "social": []},
            "challenge": {"title": "Team Member Search", "description": "Search and manage team members", "skills": [], "points": 0},
            "cta": {"label": "Access Dashboard", "link": "/lab"}
        }

def get_fallback_team_members():
    """Return fallback team member data when database is unavailable"""
    return [
        {
            "id": 1,
            "xyz_username": "admin",
            "def_email": "admin@fintrack.com",
            "ghi_full_name": "Administrator",
            "jkl_role": "admin",
            "stu_department": "IT",
            "mno_created_at": None
        },
        {
            "id": 2,
            "xyz_username": "john.doe",
            "def_email": "john.doe@fintrack.com",
            "ghi_full_name": "John Doe",
            "jkl_role": "user",
            "stu_department": "Finance",
            "mno_created_at": None
        },
        {
            "id": 3,
            "xyz_username": "jane.smith",
            "def_email": "jane.smith@fintrack.com",
            "ghi_full_name": "Jane Smith",
            "jkl_role": "manager",
            "stu_department": "Marketing",
            "mno_created_at": None
        }
    ]

@app.route('/')
def home():
    metadata = load_metadata()
    return render_template('home.html', metadata=metadata)

@app.route('/lab')
def lab():
    """Team member search dashboard"""
    metadata = load_metadata()
    search_term = request.args.get('search', '')
    debug_mode = request.args.get('debug', 'false').lower() == 'true'
    
    try:
        if search_term:
            # Use the vulnerable search function
            team_members = db.search_team_members(search_term)
            if debug_mode:
                print(f"DEBUG: Search term: '{search_term}'")
                print(f"DEBUG: Raw results: {team_members}")
        else:
            # Show all team members when no search term
            team_members = db.get_all_users()
        
        # REMOVED: No longer use fallback data to hide injection results
        # This allows SQL injection results to be displayed
        
    except Exception as e:
        print(f"Database error: {e}")
        if debug_mode:
            team_members = []  # Show empty results instead of fallback
        else:
            team_members = get_fallback_team_members()
    
    return render_template('lab.html', metadata=metadata, team_members=team_members, search_term=search_term, debug_mode=debug_mode)

@app.route('/api/metadata')
def api_metadata():
    return jsonify(load_metadata())

@app.route('/api/search')
def api_search():
    """API endpoint for team member search"""
    search_term = request.args.get('q', '')
    try:
        results = db.search_team_members(search_term)
        if not results:
            results = get_fallback_team_members()
    except Exception as e:
        print(f"Database error in API: {e}")
        results = get_fallback_team_members()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 