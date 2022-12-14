import cv2, io, base64
from PIL import Image
import threading
from time import sleep
import numpy as np

trainedfacedata = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')


class VideoCamera(object):
    def __init__(self):

        self.to_process = []
        self.output_image_rgb = []
        self.output_image_bgr = []
        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.to_process:
            return
        input_str = self.to_process.pop(0)
        imgdata = base64.b64decode(input_str)
        input_img = np.array(Image.open(io.BytesIO(imgdata)))
        """ h
        After getting the image you can do any preprocessing here
        """
        # ______________________________________Performing some pre processing______________________________________________

        bgr_image = cv2.flip(input_img, 1)  # Flip the image

        # img = cv2.imread("me5.png")
        frame = bgr_image
        grayimage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        facecord = trainedfacedata.detectMultiScale(grayimage)
        for (x, y, w, h) in facecord:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 10)  # the 0 255 are color of rec
            # cv2.imshow("me5.png", frame)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)# Changing color from bgr to rgb

        # ____________________________________________________________________________________________________________________

        ret, rgb_jpeg = cv2.imencode('.jpg', rgb_image)
        _, bgr_jpeg = cv2.imencode('.jpg', bgr_image)

        self.output_image_rgb.append(rgb_jpeg.tobytes())
        self.output_image_bgr.append(bgr_jpeg.tobytes())





    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.01)

    def enqueue_input(self, input):
        self.to_process.append(input)

    def get_frame(self):
        while not self.output_image_rgb:
            sleep(0.05)
        return self.output_image_rgb.pop(0), self.output_image_bgr.pop(0)


"""
# def stringToImage(base64_string):
#     imgdata = base64.b64decode(base64_string)
#     return np.array(Image.open(io.BytesIO(imgdata)))
"""