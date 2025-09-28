from flask import Flask, render_template, request, jsonify
from suggestions import check_spelling_and_structure
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/check', methods=['POST'])
def api_check():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '') if isinstance(data, dict) else ''
    if not isinstance(text, str):
        return jsonify({'error': 'Invalid input, expected JSON with `text` string.'}), 400
    result = check_spelling_and_structure(text)
    return jsonify(result), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
