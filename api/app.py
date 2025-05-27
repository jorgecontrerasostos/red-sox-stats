from flask import Flask, jsonify
from flask_cors import CORS
from red_sox import RedSoxDataExplorer

app = Flask(__name__)
# Configure CORS to allow requests from the frontend
CORS(app, resources={
    r"/*": {  # Allow all routes
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/')
def index():
    return jsonify({
        "message": "Red Sox Stats API",
        "endpoints": {
            "roster": "/api/roster"
        }
    })

@app.route('/api/roster')
def get_roster():
    try:
        explorer = RedSoxDataExplorer()
        roster = explorer.get_team_roster()
        return jsonify(roster)
    except Exception as e:
        app.logger.error(f"Error fetching roster: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 