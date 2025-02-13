from flask import Flask, jsonify, request
from flask_cors import CORS
import random 

app = Flask(__name__)
CORS(app)

@app.route('/receiver-position', methods=['GET'])
def receiver_position():
    # Example position of the receiver
    position = {
        "row": random.random() * 8,
        "column": random.random() * 8
    }
    return jsonify(position)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


# Information is supposed to be gotten from rpi

# @app.route('/receiver-position', methods=['GET'])
# def receiver_position():
#     data = request.get_json()  # Receive JSON data from RPI
#     print(f"Received data: {data}")
#     return jsonify({"status": "success", "received": data})