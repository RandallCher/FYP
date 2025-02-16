from flask import Flask, jsonify, request
from flask_cors import CORS
import torch

app = Flask(__name__)
CORS(app)

model = YourModelClass()
model.load_state_dict(torch.load("../../models/Grid_based/DNN_model_[256, 512, 256, 512].pth"))
model.eval()

app = Flask(__name__)
CORS(app)

@app.route('/receiver-position', methods=['POST'])
def receiver_position():
    """Receive RSSI values from React and predict position."""
    data = request.json
    rssi_values = data.get("rssi", [127] * 8)  # Default to 127 if missing

    # Convert RSSI values to tensor
    inputs = torch.tensor([rssi_values], dtype=torch.float32)

    # Run model inference
    with torch.no_grad():
        preds = model(inputs)

    row, column = preds[0].tolist()  # Convert tensor to list

    return jsonify({"row": row, "column": column})

# @app.route('/receiver-position', methods=['GET'])
# def receiver_position():
#     # Example position of the receiver
#     position = {
#         "row": random.random() * 8,
#         "column": random.random() * 8
#     }
#     return jsonify(position)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)


# Information is supposed to be gotten from rpi
