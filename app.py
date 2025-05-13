from flask import Flask, request, jsonify, send_from_directory
from agentic_ai_core import generate_proposal
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    client_brief = data.get('brief', '')
    if not client_brief:
        return jsonify({'error': 'Brief is required'}), 400

    proposal = generate_proposal(client_brief)
    return jsonify({'proposal': proposal})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
