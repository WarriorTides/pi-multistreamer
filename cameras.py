import os
import subprocess
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

statepath = str(os.path.join(dir_path, "state.json"))


# Starts up all cameras based on state JSON
def startup():
    port = 8000
    with open(statepath) as f:
        data = json.load(f)
    # print(data)
    for i in data["cameras"]:
        command = [
            "ustreamer",
            "--device",
            str(i["video port"]),
            "--resolution",
            f'{str(i["width"])}x{str(i["height"])}',
            "--format",
            "MJPEG",
            "--desired-fps",
            str(i["fps"]),
            "-l",
            "--encoder",
            "HW",
            "--host",
            "::",
            "--port",
            str(i["stream port"]),
            "--brightness",
            str(i["brightness"]),
            "--contrast",
            str(i["contrast"]),
            "--saturation",
            str(i["saturation"]),
            "--hue",
            str(i["hue"]),
            "--gamma",
            str(i["gamma"]),
            "--sharpness",
            str(i["sharpness"]),
            "--backlight-compensation",
            str(i["backlight compensation"]),
            "--white-balance",
            str(i["white balance"]),
            "--gain",
            str(i["gain"]),
            "--color-effect",
            str(i["color effect"]),
            "--rotate",
            str(i["rotate"]),
            "--flip-vertical",
            str(i["flip vertical"]),
            "--flip-horizontal",
            str(i["flip horizontal"]),
        ]

        print(command)
        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(p.pid)
        port += 1


# Kills all µstreamer processes
def killCameras():
    try:

        toKill = getProcesses()
        print(toKill)
        if len(toKill) == 0:
            print("No cameras to kill")
            return "None"
        for pid in toKill:
            # print(pid)
            subprocess.run(["kill", "-9", str(pid[0])])
            print(f"Killed process with PID: {pid[0]}")
        return "Done"

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error" + str(e)


# Returns an array of µstreamer processes
def getProcesses():
    try:
        result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE)
        processes = result.stdout.decode().splitlines()

        toKill = []
        command = []
        for process in processes:
            if "ustreamer" in process:
                temp = process.split()
                pid = temp[1]

                toKill.append(
                    (
                        pid,
                        [item for item in temp if "video" in item][0],
                        temp[
                            temp.index([item for item in temp if "port" in item][0]) + 1
                        ],
                        str(process),
                    ),
                )

        # toKill = toKill[:4]
        return toKill
    except Exception as e:
        print(f"An error occurred: {e}")


# Kills specific PID
def killPID(pid):
    try:

        subprocess.run(["kill", "-9", str(pid)])
        print(f"Killed process with PID: {pid}")
        return "Done"

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error" + str(e)


# Kills camera based on index in state.json
def killIndex(index):
    print(index)
    with open(statepath) as f:
        data = json.load(f)
    processes = getProcesses()
    for i in processes:
        if i[1] == data["cameras"][index]["video port"]:
            killPID(i[0])


# Scans for cameras nd regenerates state.json
def scanCam():
    try:
        result = subprocess.run(["v4l2-ctl", "--list-devices"], stdout=subprocess.PIPE)
        lines = result.stdout.decode().splitlines()

        devices = []
        usb = False

        for line in lines:
            line = line.strip()

            if line.endswith(":"):
                if "usb-" in line:
                    usb = True
                else:
                    usb = False

            elif usb and "/dev/video" in line:
                devices.append(line)
                usb = False

        state = {"cameras": []}
        i = 0
        for cam in devices:
            state["cameras"].append(
                {
                    "video port": cam,
                    "height": 480,
                    "width": 640,
                    "fps": 25,
                    "stream port": (8000 + i),
                    "brightness": "default",
                    "contrast": "default",
                    "saturation": "default",
                    "hue": "default",
                    "gamma": "default",
                    "sharpness": "default",
                    "backlight compensation": "default",
                    "white balance": "default",
                    "gain": "default",
                    "color effect": "default",
                    "rotate": "default",
                    "flip vertical": "default",
                    "flip horizontal": "default",
                }
            )
            i += 1

        with open(statepath, "w") as f:
            json.dump(state, f, indent=4)
            # with open(statepath) as f:
            # data = json.load(f)
            # print(data)
            # return jsonify(state)
            return state

    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error: " + str(e)


# Kills and restarts a single camera baswd on index in state.json
def singleCam(index):
    with open(statepath) as f:
        data = json.load(f)
    processes = getProcesses()
    for i in processes:

        if i[1] == data["cameras"][index]["video port"]:
            killPID(i[0])
    i = data["cameras"][index]
    command = [
        "ustreamer",
        "--device",
        str(i["video port"]),
        "--resolution",
        f'{str(i["width"])}x{str(i["height"])}',
        "--format",
        "MJPEG",
        "--desired-fps",
        str(i["fps"]),
        "-l",
        "--encoder",
        "HW",
        "--host",
        "::",
        "--port",
        str(i["stream port"]),
        "--brightness",
        str(i["brightness"]),
        "--contrast",
        str(i["contrast"]),
        "--saturation",
        str(i["saturation"]),
        "--hue",
        str(i["hue"]),
        "--gamma",
        str(i["gamma"]),
        "--sharpness",
        str(i["sharpness"]),
        "--backlight-compensation",
        str(i["backlight compensation"]),
        "--white-balance",
        str(i["white balance"]),
        "--gain",
        str(i["gain"]),
        "--color-effect",
        str(i["color effect"]),
        "--rotate",
        str(i["rotate"]),
        "--flip-vertical",
        str(i["flip vertical"]),
        "--flip-horizontal",
        str(i["flip horizontal"]),
    ]

    print(command)
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(p.pid)
    return "Done"


if __name__ == "__main__":
    scanCam()
    # for l in arr:
    #     print(l)
    print("Scanned")
