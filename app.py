from flask import Flask, render_template, request, json
from flask_cors import CORS
import requests
import hashlib
import json
import base64
import cv2
import numpy as np
from tool import solve_sudoku

app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "https://sudoku.com"}})

@app.route('/')
def index():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/upload', methods=['POST'])
def board():
    data = request.get_json()
    imgstring = data.get('image')
    imageData = base64.b64decode(imgstring)
    nparr = np.frombuffer(imageData, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # add border 100px white color to the image
    img = cv2.copyMakeBorder(img, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    board, origin = solve_sudoku(img)
    print(board)
    
    return json.dumps({'success':True, 'data': {'origin': origin, 'board': board}}), 200, {'ContentType':'application/json'}





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1026)
    # app.run(debug=True)