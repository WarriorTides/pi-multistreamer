import os
import subprocess
import json
from kill import getProcesses, killCameras, killPID 

dir_path = os.path.dirname(os.path.realpath(__file__))

statepath = str(os.path.join(dir_path, "state.json"))
# camrunpath = str(os.path.join(dir_path, "camrun.sh"))

with open(statepath) as f:
    data = json.load(f)
    # print(data)

for i in data["cameras"]:
    print(i)

def scanCam():
    try:
        result = subprocess.run(["v4l2-ctl", "--list-devices"], stdout = subprocess.PIPE)
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
    
        return devices



    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error: " + str(e)




# print(camrun)
def singleCam(index):
    with open(statepath) as f:
        data = json.load(f)
    processes=getProcesses()
    for i in processes:

        if i[1] == data["cameras"][index]["video port"] :
            killPID(i[0])
    i=data["cameras"][index]
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


if __name__ == "__main__":
    arr = scanCam()
    # for l in arr:
    #     print(l)
    print("Done")
