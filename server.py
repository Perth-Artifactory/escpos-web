# Flask server that implements an API for escpos

from flask import Flask, request, jsonify
import logging
import json
from pprint import pprint
import wrap
import printer

with open("config.json", "r") as f:
    config = json.load(f)

if config["server"]["debug"]:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# register escpos functions

commands = {"text": wrap.text, "cut": wrap.cut, "image": wrap.image, "qr": wrap.qr}

# Initialize printer
local_printer = printer.connect()

# Initialize Flask app
app = Flask(__name__)


# Receive commands via JSON array
@app.route("/control", methods=["POST"])
def control():
    c = request.get_json()
    if c is None:
        return jsonify({"error": "No commands received"})

    for command in c:
        s = command["command"]
        if "data" not in command and s == "cut":
            data = {}
        else:
            data = command["data"]

        if s in commands:
            return commands[s](local_printer, data)
        else:
            return jsonify({"error": f'Command "{s}" not found'})

    return jsonify({"success": True})


if __name__ == "__main__":
    logging.info("Starting...")

    from waitress import serve

    serve(app, host=config["server"]["address"], port=config["server"]["port"])
