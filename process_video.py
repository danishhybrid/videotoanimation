import cv2
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import flask
from flask import Flask, request
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_file = request.files["video_file"]
        video_file.save("video.mp4")

        # Load the video file
        cap = cv2.VideoCapture("video.mp4")

        # Define the frame size
        frame_width = int(cap.get(3) * 0.5)
        frame_height = int(cap.get(4) * 0.5)

        # Extract the frames from the video
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (frame_width, frame_height), cv2.INTER_LINEAR)
            frames.append(frame)

        # Define the animation function
        def update_frame(i, ims):
            im = ims[i]
            plt.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))

        # Set up the animation
        fig = plt.figure()
        ims = []
        for frame in frames:
            im = plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            ims.append([im])
        ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)

        # Convert the animation to HTML5 video
        buffer = BytesIO()
        ani.save(buffer, writer='html', dpi=80)
        video = buffer.getvalue()

    return """
    <html>
      <head>
        <title>Video to Animation Converter</title>
      </head>
      <body>
        <h1>Video to Animation Converter</h1>
        <form action="animation.html" method="post" enctype="multipart/form-data">
          <input type="file" name="video_file">
          <input type="submit" value="Convert">
        </form>
        <br>
        {}
      </body>
    </html>
    """.format(video.decode())

if __name__ == "__main__":
    app.run()
