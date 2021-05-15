import PySimpleGUI as sg
import cv2 as cv
import numpy as np

def main():
    left_line = 300
    right_line = 340
    
    left_col = [
        [sg.Image(filename="", key="-IMAGE-")],
    ]

    right_col = [
        [sg.Text('rozstaw linii')],
        [
            sg.Button("-", key="-LINES_DEC-"),
            sg.Button("+", key="-LINES_INC-")
        ]
    ]

    layout = [
        [
            sg.Column(left_col),
            sg.Column(right_col)
        ]
    ]

    # Create the window and show it without the plot
    window = sg.Window("OpenCV Integration", layout)

    cap = cv.VideoCapture(0)

    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "-LINES_DEC-":
            left_line += 5
            if left_line >= 300:
                left_line = 300
            right_line -= 5
            if right_line <= 340:
                right_line = 340

        if event == "-LINES_INC-":
            left_line -= 5
            if left_line <= 100:
                left_line = 100
            right_line += 5
            if right_line >= 550:
                right_line = 550

        ret, frame = cap.read()

        blank = np.zeros(frame.shape[:2], dtype='uint8')
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        lower_green = np.array([40, 40, 40])
        upper_green = np.array([60, 255, 255])

        mask = cv.inRange(hsv,lower_green,upper_green)

        blur = cv.GaussianBlur(mask, (1,1), 0)

        res = cv.bitwise_and(frame, frame, mask=blur)

        added = cv.addWeighted(frame, 0.6, res, 0.4, 0)

        non_zero = np.transpose(np.nonzero(res))
        left_most = non_zero[non_zero[:,1].argmin()]
        right_most = non_zero[non_zero[:,1].argmax()]
        min_x = left_most[:][1]
        max_x = right_most[:][1]

        center_x = (max_x + min_x) / 2
        cv.line(added, (int(center_x-1), 100), (int(center_x-1), 400), (255,0,0), 3)
        cv.circle(added, (min_x, 267), 5, (0,0,255), -1)
        cv.circle(added, (max_x, 267), 5, (0,0,255), -1)

        cv.line(added, (left_line, 100), (left_line, 400),(0,0,255),2)
        cv.line(added, (right_line, 100), (right_line, 400),(0,0,255),2)

        font = cv.FONT_HERSHEY_SIMPLEX
        if min_x > left_line and max_x > right_line:
            cv.putText(added, 'w prawo', (200,50), font, 2, (0,0,255), 2, cv.LINE_AA)
        elif min_x < left_line and max_x < right_line:
            cv.putText(added, 'w lewo', (200,50), font, 2, (0,0,255), 2, cv.LINE_AA)
        elif min_x < left_line and max_x > right_line:
            cv.putText(added, 'error', (250, 50), font, 2, (0,0,255), 2, cv.LINE_AA )
        else:
            cv.putText(added, 'ok', (300,50), font, 2, (0,0,255), 2, cv.LINE_AA)

        imgbytes = cv.imencode(".png", added)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

    window.close()

main()