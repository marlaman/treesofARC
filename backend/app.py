from flask import Flask, request, jsonify, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
from llm_stuff import ARC_answer
from demo_framework import demo_framework
import pandas as pd
import numpy as np
import time
import uuid
import os
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3040"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Serve image from the backend folder
@app.route('/backend-image/<filename>', methods=['POST','GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def serve_backend_image(filename):
    file_path = f"/Users/pranavmarla/ARCAssist/backend/{filename}"  # Path to your backend folder
    return send_file(file_path, mimetype='image/jpeg')  # Serve the image directly
    

def get_random_file(folder_path):
    try:
        # Get a list of files in the specified folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        # Check if there are any files in the folder
        if not files:
            return "No files found in the folder."
        
        # Get a random file and return its full path
        random_file = random.choice(files)
        print("Random File: ",  os.path.join(folder_path, random_file))
        return os.path.join(folder_path, random_file)
    
    except FileNotFoundError:
        return "Folder not found."

    


@app.route('/solve_arc', methods=['POST','GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def solve_arc():
    arc_puzzle_name = get_random_file("/Users/pranavmarla/Downloads/ARC-800-tasks/evaluation/")
    demo_framework(arc_puzzle_name,socketio)
    return jsonify({"status": "completed"})





if __name__ == '__main__':
    socketio.run(app,port=5020, debug=True)
