from flask import Flask, jsonify
from flask_cors import CORS
from red_sox import RedSoxDataExplorer

app = Flask(__name__)
CORS(app)

@app.route('/api/roster')
def get_roster():
    explorer = RedSoxDataExplorer()
    roster = explorer.get_team_roster()
    return jsonify(roster)

if __name__ == '__main__':
    app.run(debug=True) 