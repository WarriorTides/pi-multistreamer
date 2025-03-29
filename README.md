# Raspberry Pi Multi-Camera MJPEG Streamer

This project sets up a lightweight multi-camera streaming server using `ustreamer`, Flask, and a web interface. It enables streaming from multiple USB cameras on a Raspberry Pi. It is actively maintained by the Valley Christian Warriortides MATE ROV team.  

---

## 🧰 Requirements

- Raspberry Pi 4B (64-bit, Bookworm OS recommended)
- Multiple **UVC  Compliant** USB webcams, Arducam Webcams work great

---

## ⚙️ Setup Instructions

### 1. Clone & Prepare
Place your project files in `/home/pi/pi-multistreamer/`.

### 2. One-Command Setup (on the Pi)

Run:
```bash
sudo bash pisetup.sh
```

This will:
- Ensure the system is online
- Update and upgrade packages
- Install dependencies:
  - `ustreamer`
  - `python3-flask`
  - `python3-flask-cors`
- Run the initial `cameras.py` script
- Add the Flask server to crontab for startup
- Reboot the Pi
---

## 📦 File Structure

| File             | Purpose                                                   |
|------------------|-----------------------------------------------------------|
| `server.py`      | Flask backend for controlling camera processes            |
| `cameras.py`     | Reads camera configs and launches `ustreamer` processes   |
| `state.json`     | Camera configuration: ports, resolutions, FPS, etc.       |
| `camrun.sh`      | Shell wrapper to start `ustreamer` with arguments         |
| `pisetup.sh`     | One-click setup script for Raspberry Pi                   |
| `index.html`     | Web UI frontend                                           |
| `script.js`      | Camera control logic via HTTP API                         |

---

## 🌐 Web Interface

Accessible on:  
```http
http://<RASPBERRY_PI_IP>:80/
```

Features:
- Start/Stop streaming
- View multiple MJPEG camera feeds
- Auto-scan for new devices

---

## 📡 HTTP API Reference

All API requests are made to the server running on port `5000`.

### POST `/rescanCams`

Re-scans cameras and updates `state.json`.

**Example:**
```bash
curl -X POST http://<PI_IP>/rescanCams
```

---

### POST `/startup`

Starts all cameras defined in `state.json`.

**Example:**
```bash
curl -X POST http://<PI_IP>/startup
```

---

### POST `/killCameras`

Kills all active `ustreamer` camera processes.

**Example:**
```bash
curl -X POST http://<PI_IP>/killCameras
```

---

### GET `/getProcesses`

Returns a JSON list of running camera processes and their stream ports.


**Example:**
```bash
curl http://<PI_IP>/getProcesses
```
---

### PATCH/POST `/update-camera/<id>`

Updates configuration values for a specific camera listed in `state.json`.

**Parameters:**

- `id` — Integer index of the camera in the `cameras` array (e.g., `0` for the first camera) can be found using getProcesses

**Payload (JSON):**

You can pass any subset of the configurable camera properties. Only keys present in the `state.json` for the selected camera will be updated. Invalid keys will return a `400` error.

**Example Request:**

```bash
curl -X POST http://<PI_IP>:5000/update-camera/0 \
  -H "Content-Type: application/json" \
  -d '{
        "brightness": 1500,
        "fps": 20,
        "width": 640
      }'
```

**Example Response:**

```json
{
  "message": "Camera updated successfully",
  "camera": {
    "video port": "/dev/video0",
    "height": 720,
    "width": 640,
    "fps": 20,
    "stream port": 8000,
    "brightness": 1500,
    ...
  }
}
```
⚠️ Not all webcams support all controls. Unsupported settings are safely ignored.


**Error Codes:**

- `404 Not Found`: Invalid camera ID
- `400 Bad Request`: Invalid camera property
- `500 Internal Server Error`: On file access or unexpected issues

---



## 📺 Viewing Streams

Each camera stream is available at:
```http
http://<PI_IP>:<stream_port>/stream
```

Example:
- `http://<PI_IP>:8000/stream`
- `http://<PI_IP>:8001/stream`

Ports are defined per camera in `state.json`.

---

## 📝 `state.json` Sample

```json
{
  "cameras": [
    {
      "video port": "/dev/video0",
      "height": 720,
      "width": 1280,
      "fps": 25,
      "stream port": 8000
    },
    ...
  ]
}
```
