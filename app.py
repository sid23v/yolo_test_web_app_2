from flask import Flask, render_template, Response, request
from camera import VideoCamera

app = Flask(__name__)

camera = None  # Global camera instance

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames(camera):
    while camera.is_running:
        frame = camera.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    global camera
    if camera is None or not camera.is_running:
        return "Camera not started", 400
    return Response(generate_frames(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start', methods=['POST'])
def start():
    global camera
    if camera is None or not camera.is_running:
        camera = VideoCamera()
        camera.start()
    return "Started"

@app.route('/stop', methods=['POST'])
def stop():
    global camera
    if camera and camera.is_running:
        camera.stop()
    return "Stopped"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)