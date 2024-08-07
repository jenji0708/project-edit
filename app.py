from flask import Flask, request, jsonify, render_template
import face_recognition
import numpy as np
import os
import pymongo
app = Flask(__name__)

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
print(client.server_info())
db = client['face_recognition']
collection = db['registered_faces']

def store_face(name, face_encoding):
    face_data = {
        "name": name,
        "encoding": face_encoding.tolist()
    }
    collection.insert_one(face_data)

def load_registered_faces():
    registered_faces = {}
    for record in collection.find():
        registered_faces[record["name"]] = np.array(record["encoding"])
    return registered_faces

registered_faces = load_registered_faces()

@app.route('/')
def input():
    return render_template('input.html')

@app.route('/register_face', methods=['POST'])
def register_face():
    data = request.form
    name = data['name']
    image_file = request.files['image']
    image = face_recognition.load_image_file(image_file)
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) > 0:
        registered_faces[name] = face_encodings[0]
        store_face(name, face_encodings[0])
        return jsonify({"status": "success", "message": "Registration successful!"}), 200
    else:
        return jsonify({"status": "failure", "message": "No face found in the image."}), 400

@app.route('/verify_face', methods=['POST'])
def verify_face():
    image_file = request.files['image']
    image = face_recognition.load_image_file(image_file)
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) > 0:
        for name, registered_encoding in registered_faces.items():
            matches = face_recognition.compare_faces([registered_encoding], face_encodings[0])
            if matches[0]:
                return jsonify({"status": "success", "name": name}), 200

    return jsonify({"status": "failure", "message": "Face not recognized."}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
