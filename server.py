import socket
import firebase_admin
from firebase_admin import credentials, firestore, storage
import datetime
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import cv2

# Authenticate user on Firebase
cred = credentials.Certificate(
    '/home/pawan/Documents/leafdoctor-x-firebase-adminsdk-s28tj-0fcfc769de.json')

firebase_admin.initialize_app(cred, {
    'storageBucket': 'leafdoctor-x.appspot.com'})

# Objects to be used for the transaction
bucket = storage.bucket()
blob = bucket.blob('images/Uploaded.jpg')
db = firestore.client()


HEADERSIZE = 10
SUCCESS = "Success"
FAILED = "Failed"
SERVER_IP = '192.168.0.107'
SERVER_PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP, SERVER_PORT))
# Wait for connection from client
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    status = clientsocket.recv(1024).decode('utf-8')[HEADERSIZE:]
    # print(status)

    if status == SUCCESS:
        # Download the image uploaded from Android
        url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
        response = requests.get(url)
        img_recvd = Image.open(BytesIO(response.content))
        img = np.array(img_recvd)

        '''=====================Image Processing Start======================'''

        x, y = img.shape[1]//5, img.shape[0]//5
        img = cv2.resize(img, (x, y))

        dots = np.zeros((y, x))

        Yc, Xc = y//2, x//2
        dx = x//20
        dy = y//20

        for a in range(dx, x-dx):
            dots[y - dy, a] = 2
            dots[dy, a] = 2

        for a in range(dy, y-dy):
            dots[a, dx] = 2
            dots[a, x - dx] = 2

        dots[Yc - dy, Xc] = 1
        dots[Yc, Xc - dx] = 1
        dots[Yc - dy, Xc - dx] = 1
        dots[Yc + dy, Xc] = 1
        dots[Yc, Xc + dx] = 1
        dots[Yc + dy, Xc + dx] = 1
        dots[Yc + dy, Xc - dx] = 1
        dots[Yc - dy, Xc + dx] = 1

        # Apply watershed
        markers = cv2.watershed(img, dots.astype(int)).get()
        markers = (markers + 1)/3.0 * 255
        markers[markers == 255] = 0
        markers[markers > 0] = 255.0
        markers = markers.astype(np.uint8)

        '''========================Image Processing End====================='''
        final = cv2.bitwise_and(img, img, mask=markers)
        outfile = './Image.jpg'

        # Color correction
        final = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
        cv2.imwrite(outfile, final)
        # print("Image Saved!")

        # Save the file locally
        with open(outfile, 'rb') as my_file:
            blob.upload_from_file(my_file)
        # print("Upload Done")

        # Report Success to the app
        clientsocket.send(bytes(SUCCESS+"\n", 'utf-8'))
        #  print("Message Sent!")
