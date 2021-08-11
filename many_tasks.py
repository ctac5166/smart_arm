#Import necessary libraries
from flask import Flask, render_template, Response
import cv2
import numpy as np
#Initialize the Flask app
app = Flask(__name__)

def gen_frames(camera_id, camera_id_second):
    camera = cv2.VideoCapture(camera_id)
    camera2 = cv2.VideoCapture(camera_id_second)
    while True:
        success, frame = camera.read()  # read the camera frame
        success2, frame2 = camera2.read()  # read the camera frame
        if not success or not success2:
            break
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            ret, buffer = cv2.imencode('.jpg', frame)
            cv2.imwrite('test.jpg', buffer)
            ret2, buffer2 = cv2.imencode('.jpg', frame2)
            cv2.imwrite('test2.jpg', buffer2)
            frame = buffer.tobytes()
            frame2 = buffer2.tobytes()

            img1 = cv2.imread('test.jpg')
            img2 = cv2.imread('test2.jpg')

            h1, w1 = img1.shape[:2]
            h2, w2 = img2.shape[:2]

            # create empty matrix
            vis = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)

            # combine 2 images
            vis[:h1, :w1, :3] = img1
            vis[:h2, w1:w1 + w2, :3] = img2

            print(vis)



            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + vis.tobytes() + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(0, 1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    return Response(gen_frames(1, 0), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="192.168.0.109",debug=True, port=5001)

