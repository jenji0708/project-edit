// const express = require('express');
// const mongoose = require('mongoose');
// const bodyParser = require('body-parser');
// const cookieParser = require('cookie-parser');
// const path = require('path');
// const cors = require('cors');
// const jwt = require('jsonwebtoken');
// const multer = require('multer');
// const faceapi = require('face-api.js');
// const canvas = require('canvas');
// const fs = require('fs');
// require('dotenv').config();

// // Load face-api.js models
// const MODEL_URL = path.join(__dirname, 'models');
// Promise.all([
//     faceapi.nets.tinyFaceDetector.loadFromDisk(MODEL_URL),
//     faceapi.nets.faceLandmark68Net.loadFromDisk(MODEL_URL),
//     faceapi.nets.faceRecognitionNet.loadFromDisk(MODEL_URL)
// ]);
// // Set up multer for file uploads
// const storage = multer.memoryStorage();
// const upload = multer({ storage: storage });


// const app = express();
// const port = process.env.PORT || 5000;
// const authRoutes = require('./routes/auth');

// // Middleware
// app.use(cors());
// // app.use(bodyParser.urlencoded({ extended: false }));
// app.use(bodyParser.urlencoded({ extended: true }));
// app.use(bodyParser.json());
// app.use(cookieParser());
// app.use(express.static(path.join(__dirname, 'public')));


// // MongoDB connection
// mongoose.connect('mongodb://localhost:27017/regis-database', { useNewUrlParser: true, useUnifiedTopology: true })
//     .then(() => console.log('MongoDB connected...'))
//     .catch(err => console.error('MongoDB connection error:', err));

// // Authentication middleware
// const authenticate = (req, res, next) => {
//     const token = req.cookies['auth-token'];
//     if (!token) {
//         return res.redirect('/login');
//     }
//     jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
//         if (err) {
//             return res.redirect('/login');
//         }
//         req.user = user;
//         next();
//     });
// };

// const labeledDescriptors = [];
// const { Canvas, Image, ImageData } = canvas;
// faceapi.env.monkeyPatch({ Canvas, Image, ImageData });

// async function loadModels() {
//     await faceapi.nets.ssdMobilenetv1.loadFromDisk('./models');
//     await faceapi.nets.faceLandmark68Net.loadFromDisk('./models');
//     await faceapi.nets.faceRecognitionNet.loadFromDisk('./models');
//   }

//   app.post('/registerface', upload.single('image'), async (req, res) => {
//     try {
//         const { name } = req.body;
//         const imageBuffer = req.file.buffer;
//         const img = await canvas.loadImage(imageBuffer);
//         const detection = await faceapi.detectSingleFace(img, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceDescriptor();
//         if (!detection) return res.json({ message: 'No face detected' });

//         const descriptor = detection.descriptor;
//         const data = { name, descriptor };
//         fs.writeFileSync(path.join(__dirname, 'descriptors', `${name}.json`), JSON.stringify(data));
//         res.json({ message: 'Face registered successfully' });
//     } catch (error) {
//         console.error(error);
//         res.status(500).json({ message: 'Internal server error' });
//     }
// });

// app.post('/verifyface', upload.none(), async (req, res) => {
//     try {
//         const { descriptor } = req.body;
//         const inputDescriptor = new Float32Array(JSON.parse(descriptor));
//         const descriptorsPath = path.join(__dirname, 'descriptors');
//         const files = fs.readdirSync(descriptorsPath);
//         let match = null;

//         for (const file of files) {
//             const data = JSON.parse(fs.readFileSync(path.join(descriptorsPath, file)));
//             const referenceDescriptor = new Float32Array(data.descriptor);
//             const distance = faceapi.euclideanDistance(inputDescriptor, referenceDescriptor);
//             if (distance < 0.6) {
//                 match = data.name;
//                 break;
//             }
//         }

//         if (match) {
//             res.json({ message: `Face verified: ${match}` });
//         } else {
//             res.json({ message: 'Face not recognized' });
//         }
//     } catch (error) {
//         console.error(error);
//         res.status(500).json({ message: 'Internal server error' });
//     }
// });

// // Routes
// app.use('/auth', authRoutes);

// // app.get('/', (req, res) => {
// //     res.sendFile(path.join(__dirname, 'public', 'login.html'));
// // });

// app.get('/home', authenticate, (req, res) => {
//     res.sendFile(path.join(__dirname, 'public', 'home.html'));
// });

// app.get('/login', (req, res) => {
//     res.sendFile(path.join(__dirname, 'public', 'login.html'));
// });

// app.get('/register', (req, res) => {
//     res.sendFile(path.join(__dirname, 'public', 'register.html'));
// });

// app.get('/gra-Inv', (req, res) => {
//     res.sendFile(path.join(__dirname, 'public', 'gra-Inv.html'));
// });

// app.get('/input', (req, res) => {
//     res.sendFile(path.join(__dirname, 'public', 'input.html'));
// });

// app.get('/profile', (req, res) => {
//     res.sendFile(path.join(__dirname, 'public', 'showInformstion.html'));
// });

// app.get('/api/user', authenticate, async (req, res) => {
//     try {
//         const user = await User.findById(req.user.id).select('email');
//         if (!user) return res.status(404).json({ message: 'User not found.' });
//         res.json({ email: user.email });
//     } catch (error) {
//         res.status(500).json({ message: 'Server error, please try again later.' });
//     }
// });

// // Start server
// app.listen(port, () => {
//     console.log(`Server running on port ${port}`);
// });
const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const path = require('path');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const multer = require('multer');
const faceapi = require('face-api.js');
const canvas = require('canvas');
const fs = require('fs');
require('dotenv').config();

// Load face-api.js models
const MODEL_URL = path.join(__dirname, 'models');
Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromDisk(MODEL_URL),
    faceapi.nets.faceLandmark68Net.loadFromDisk(MODEL_URL),
    faceapi.nets.faceRecognitionNet.loadFromDisk(MODEL_URL)
]);

// Set up multer for file uploads
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

const app = express();
const port = process.env.PORT || 5000;
const authRoutes = require('./routes/auth');

// Middleware
app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/regis-database', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected...'))
    .catch(err => console.error('MongoDB connection error:', err));

// Authentication middleware
const authenticate = (req, res, next) => {
    const token = req.cookies['auth-token'];
    if (!token) {
        return res.redirect('/login');
    }
    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            return res.redirect('/login');
        }
        req.user = user;
        next();
    });
};

const { Canvas, Image, ImageData } = canvas;
faceapi.env.monkeyPatch({ Canvas, Image, ImageData });

app.post('/registerface', upload.single('image'), async (req, res) => {
    try {
        const { name } = req.body;
        const imageBuffer = req.file.buffer;
        const img = await canvas.loadImage(imageBuffer);
        const detection = await faceapi.detectSingleFace(img, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceDescriptor();
        if (!detection) return res.json({ message: 'No face detected' });

        const descriptor = detection.descriptor;
        const data = { name, descriptor };
        fs.writeFileSync(path.join(__dirname, 'descriptors', `${name}.json`), JSON.stringify(data));
        res.json({ message: 'Face registered successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

app.post('/verifyface', upload.none(), async (req, res) => {
    try {
        const { descriptor } = req.body;
        const inputDescriptor = new Float32Array(JSON.parse(descriptor));
        const descriptorsPath = path.join(__dirname, 'descriptors');
        const files = fs.readdirSync(descriptorsPath);
        let match = null;

        for (const file of files) {
            const data = JSON.parse(fs.readFileSync(path.join(descriptorsPath, file)));
            const referenceDescriptor = new Float32Array(data.descriptor);
            const distance = faceapi.euclideanDistance(inputDescriptor, referenceDescriptor);
            if (distance < 0.6) {
                match = data.name;
                break;
            }
        }

        if (match) {
            res.json({ message: `Face verified: ${match}` });
        } else {
            res.json({ message: 'Face not recognized' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

// Routes
app.use('/auth', authRoutes);

app.get('/home', authenticate, (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'home.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'register.html'));
});

app.get('/gra-Inv', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'gra-Inv.html'));
});

app.get('/input', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'input.html'));
});

app.get('/profile', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'showInformation.html'));
});

app.get('/api/user', authenticate, async (req, res) => {
    try {
        const user = await User.findById(req.user.id).select('email');
        if (!user) return res.status(404).json({ message: 'User not found.' });
        res.json({ email: user.email });
    } catch (error) {
        res.status(500).json({ message: 'Server error, please try again later.' });
    }
});

// Start server
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
