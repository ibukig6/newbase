# app.py
from flask import Flask, render_template, request, url_for, redirect

import cv2
import numpy as np
import os

app = Flask(__name__)

# 預設首頁
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/input")
def input():
    return render_template("input.html")

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        video = request.form["video"]


        cap = cv2.VideoCapture(video)
        detect=0
        cut = None

        while True:
            ret, frame = cap.read()
            if not ret:
                print("影片讀取完畢")
                break
            frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            newF = frame[150:450, 730:740]  # 偵測範圍
            cv2.rectangle(frame, (730, 150), (740, 450), (0, 0, 255), 2)

            mask = (newF >= [200, 200, 200]).all(axis=2)
            if detect == 0:
                if np.any(mask):
                    cut = frame
                    print("偵測到球了")
                    detect = 1
        
            if detect == 1:
                cv2.putText(frame, "detect", (100, 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)
            # cv2.imshow('Frame', frame)
            # out.write(frame)

        # output = os.path.join("video", "detected_frame.jpg")
        # cv2.imwrite(output, cut)

        if cut is not None:
            output = os.path.join("video", "detected_frame.jpg")
            cv2.imwrite(output, cut)
            print(f"圖片已保存至: {output}")
        else:
            print("未偵測到球，無法保存圖片")
        
        cap.release()
        # out.release()
        cv2.destroyAllWindows()

        return redirect(url_for("video"))
    
@app.route("/video")
def video():
    return render_template("video.html")

@app.route("/v2")
def v2():
    return render_template("v2.html")

if __name__ == '__main__':
    app.run(debug=True)
