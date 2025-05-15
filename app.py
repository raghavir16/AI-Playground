from flask import Flask, request, jsonify, send_from_directory
from agentic_ai import generate_proposal

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    requirements = data.get('requirements', '')

    if not requirements.strip():
        return jsonify({'error': 'Requirements are required'}), 400

    try:
        proposal = generate_proposal(requirements)
        return jsonify({'proposal': proposal})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
