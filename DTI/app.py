from flask import Flask, render_template, Response, redirect, url_for, jsonify
from pose_detector import generate_frames, get_score, TRIGGER_PATH
import os
import random

app = Flask(__name__)
current_score = 0

@app.route('/check_trigger')
def check_trigger():
    try:
        with open(TRIGGER_PATH, "r") as f:
            content = f.read()
            if "done" in content:
                return jsonify({"status": "done"})
    except FileNotFoundError:
        pass
    return jsonify({"status": "waiting"})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/breathing')
def breathing():
    affirmations = [
        "✨ You are calm, grounded, and enough.",
        "🌿 In this moment, you are exactly where you need to be.",
        "🧘 Breathe in strength, breathe out tension.",
        "💫 You are capable, you are peaceful, you are strong."
    ]
    chosen = random.choice(affirmations)
    return render_template('breathing.html', random_affirmation=chosen)

@app.route('/choice')
def choice():
    return render_template('choice.html')

@app.route('/live-detector')
def live_detector():
    return render_template('detector_live.html')

@app.route('/video_feed')
def video_feed():
    global current_score
    current_score = 0  # reset for each session
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/result')
def result():
    global current_score
    current_score = get_score()
    try:
        with open(TRIGGER_PATH, "w") as f:
            f.write("")  # Clear the trigger file
    except:
        pass
    return render_template('detector_game_result.html', score=current_score)

if __name__ == '__main__':
    app.run(debug=True)



