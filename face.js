const express = require('express');
const multer = require('multer');
const mongoose = require('mongoose');
const faceapi = require('face-api.js');
const canvas = require('canvas');
const { Canvas, Image, ImageData } = canvas;

faceapi.nets.tinyFaceDetector.loadFromDisk('./models');
faceapi.nets.faceLandmark68Net.loadFromDisk('./models');
faceapi.nets.faceRecognitionNet.loadFromDisk('./models');

const app = express();
const port = 5000;

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/student-db', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const StudentSchema = new mongoose.Schema({
  studentID: String,
  studentName: String,
  course: String,
  section: String,
  image: Buffer // Store image as binary data
});
const Student = mongoose.model('Student', StudentSchema);

// Middleware for file upload
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

app.use(express.json());
app.use(express.static('public'));

// Endpoint to handle face registration
app.post('/registerface', upload.single('image'), async (req, res) => {
  try {
    const { studentID, studentName, course, section } = req.body;
    const image = req.file.buffer;

    // Save image and student info to database
    const student = new Student({ studentID, studentName, course, section, image });
    await student.save();
    res.json({ message: 'Registration successful' });
  } catch (error) {
    res.status(500).json({ message: 'Error registering face' });
  }
});

// Endpoint to verify face
app.post('/verifyface', upload.single('image'), async (req, res) => {
  try {
    const image = req.file.buffer;

    // Load registered face descriptors from the database
    const students = await Student.find();
    const descriptors = students.map(student => ({ id: student._id, descriptor: student.descriptor }));

    // Detect face and compare with stored descriptors
    const img = await canvas.loadImage(image);
    const detections = await faceapi.detectSingleFace(img, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceDescriptor();

    if (!detections) {
      return res.json({ message: 'No face detected' });
    }

    const faceMatcher = new faceapi.FaceMatcher(descriptors.map(desc => new faceapi.LabeledFaceDescriptors(desc.id, [desc.descriptor])));
    const bestMatch = faceMatcher.findBestMatch(detections.descriptor);

    if (bestMatch && bestMatch.distance < 0.6) { // Adjust threshold as necessary
      res.json({ message: 'Face matched successfully' });
    } else {
      res.json({ message: 'Face not matched' });
    }
  } catch (error) {
    res.status(500).json({ message: 'Error verifying face' });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
