import time
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import cameras
import os
import json

# read state.json file

dir_path = os.path.dirname(os.path.realpath(__file__))

statepath = str(os.path.join(dir_path, "state.json"))
print(statepath)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/")
def main():
    return render_template("index.html")


# get State of cameras in json
@app.route("/state", methods=["POST", "GET"])
def get_state():
    with open(statepath) as f:
        data = json.load(f)
        print(data)
        return jsonify(data)


@app.route("/stateIndex/<int:id>", methods=["POST", "GET"])
def get_state_index(id):
    with open(statepath) as f:
        data = json.load(f)
        camera_data = data["cameras"][id]
        print(camera_data)
        return jsonify(camera_data)


@app.route("/getProcesses", methods=["POST", "GET"])
def getProcesses():
    return jsonify(cameras.getProcesses())


@app.route("/killCameras", methods=["POST"])
def killCameras():
    state = cameras.killCameras()
    return jsonify({"status": state})


@app.route("/rescanCams", methods=["POST", "GET"])
def rescanCameras():
    cams = cameras.scanCam()
    return jsonify({"status": cams})


@app.route("/startup", methods=["POST"])
def startup():
    cameras.killCameras()
    time.sleep(0.5)
    cameras.startup()
    return jsonify({"status": "done"})


@app.route("/killSingle/<int:pid>", methods=["POST"])
def kill_single(pid):
    cameras.killPID(pid)
    return jsonify({"status": "done"})


@app.route("/killSingleIndex/<int:id>", methods=["POST", "GET"])
def kill_single_index(id):
    cameras.killIndex(id)
    return jsonify({"status": "done"})


@app.route("/startSingle/<int:id>", methods=["POST"])
def starte_Sinlge(id):
    cameras.singleCam(id)
    return jsonify({"status": "done"})


@app.route("/update-camera/<int:id>", methods=["PATCH", "POST"])
def update_camera(id):

    try:

        with open(statepath, "r") as file:
            state = json.load(file)

        if id < 0 or id >= len(state["cameras"]):
            return jsonify({"error": "Camera ID not found"}), 404

        camera = state["cameras"][id]

        updates = request.json

        for key, value in updates.items():
            if key in camera:
                camera[key] = value
            else:
                return jsonify({"error": f"Invalid property: {key}"}), 400

        with open(statepath, "w") as file:
            json.dump(state, file, indent=4)

        return jsonify({"message": "Camera updated successfully", "camera": camera})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
