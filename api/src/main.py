from flask import Flask, request, send_file, Response
import numpy as np
from segmenters.watershed_segmenter import WaterShedSegmenter
from typing import Dict 
import cv2
import io
from PIL import Image

class Server():
    def __init__(self):
        self.segmenter = WaterShedSegmenter()
        self.app = Flask(__name__)

    def send_image(self, img: np.ndarray) -> Response:
        res = Image.fromarray(img.astype("uint8"), "RGB")
        frame_file = io.BytesIO()
        res.save(frame_file, "JPEG", quality=85)
        frame_file.seek(0)
        return send_file(frame_file, attachment_filename="latest-frame.jpg")

    def __init_apis(self):
        @self.app.route('/')
        def hello_world():
            return 'Hello, World!'

        @self.app.route('/segment', methods=['POST'])
        def segment():
            filestr = request.files['imagefile'].read()
            npimg = np.fromstring(filestr, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            res =  self.segmenter.run(img)
            return self.send_image(res)
        
    def start(self):
        self.__init_apis()
        self.app.run()
    
if __name__ == "__main__":
    server = Server()
    server.start()




