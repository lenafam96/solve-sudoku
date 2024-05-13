# DataFlair Sudoku solver

import sys
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import imutils
from sudokutools import solve
from auto import auto
import pyautogui as pya
import tkinter as tk
from PIL import ImageGrab
from tkinter import messagebox
from tkmacosx import Button


classes = np.arange(0, 10)

model = load_model('model-OCR.h5')
# print(model.summary())
input_size = 48


def get_perspective(img, location, height = 900, width = 900):
    """Takes an image and location os interested region.
        And return the only the selected region with a perspective transformation"""
    pts1 = np.float32([location[0], location[3], location[1], location[2]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result

def find_board(img):
    """Takes an image as input and finds a sudoku board inside of the image"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 13, 20, 20)
    edged = cv2.Canny(bfilter, 30, 180)
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours  = imutils.grab_contours(keypoints)

    newimg = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 3)


    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    location = None
    
    # Finds rectangular contour
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 15, True)
        if len(approx) == 4:
            location = approx
            break
    
    if location is None:
        print("Board not found")
        return None, None

    result = get_perspective(img, location)
    return result, location


# split the board into 81 individual images
def split_boxes(board):
    """Takes a sudoku board and split it into 81 cells. 
        each cell contains an element of that board either given or an empty cell."""
    rows = np.vsplit(board,9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r,9)
        for box in cols:
            box = cv2.resize(box, (input_size, input_size))/255.0
            # cv2.imshow("Splitted block", box)
            # cv2.waitKey(50)
            boxes.append(box)
    cv2.destroyAllWindows()
    return boxes

# Read image
# img = cv2.imread('sudoku1.jpg')
# img = cv2.imread('1.png')


def main():
    # if window os is windows
    if sys.platform == 'win32':
        im = pya.screenshot(region=(300, 180, 580, 530))
    elif sys.platform == 'darwin':
        im = pya.screenshot(region=(330, 230, 550, 530))

    img = np.array(im)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # cv2.imshow("Original Image", img)
    # cv2.waitKey(0)
    # exit()
    board, location = find_board(img)

    if board is None:
        messagebox.showinfo("Error", "Board not found")
        return


    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    # print(gray.shape)
    rois = split_boxes(gray)
    rois = np.array(rois).reshape(-1, input_size, input_size, 1)

    # get prediction
    prediction = model.predict(rois)
    # print(prediction)

    predicted_numbers = []
    # get classes from prediction
    for i in prediction: 
        index = (np.argmax(i)) # returns the index of the maximum number of the array
        predicted_number = classes[index]
        predicted_numbers.append(predicted_number)

    # print(predicted_numbers)

    # reshape the list 
    board_num = np.array(predicted_numbers).astype('uint8').reshape(9, 9)

    # convert numpy array to list
    board_num = board_num.tolist()

    print(board_num)

    # solve the sudoku
    solve(board_num)

    print(board_num)

    auto(board_num, pya, sys)

# create a tkinter window
root = tk.Tk()
root.title("Sudoku Solver")
canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()
if sys.platform == 'win32':
    button1 = tk.Button(text="Solve Sudoku", command=main, bg='green',fg='white', width=25, height=5)
elif sys.platform == 'darwin':
    button1 = Button(text="Solve Sudoku", command=main, bg='#ADEFD1',fg='#00203F', width=250, height=100)
canvas1.create_window(150, 150, window=button1)

root.mainloop()