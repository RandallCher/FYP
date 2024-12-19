from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/receiver-position', methods=['GET'])
def receiver_position():
    # Example position of the receiver
    position = {
        "row": 2,
        "column": 2.5
    }
    return jsonify(position)

if __name__ == '__main__':
    # Run the Flask server on localhost:5000
    app.run(debug=True, host='0.0.0.0', port=5000)
