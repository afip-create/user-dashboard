// user-dashboard.js
const express = require('express');
const app = express();
const mongoose = require('mongoose');
const cors = require('cors');
const userRoutes = require('./routes/user');
const dataRoutes = require('./routes/data');
const progressRoutes = require('./routes/progress');
const notificationRoutes = require('./routes/notification');

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/user-dashboard', { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;
db.on('error', (err) => console.error(err));
db.once('open', () => console.log('Connected to MongoDB'));

// Routes
app.use('/api/users', userRoutes);
app.use('/api/data', dataRoutes);
app.use('/api/progress', progressRoutes);
app.use('/api/notifications', notificationRoutes);

// API Documentation
app.get('/api/docs', (req, res) => {
  res.send('API documentation is available at /api/docs');
});

// Start server
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server started on port ${port}`));

// Export app
module.exports = app;
```

```javascript
// user.js
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  name: String,
  email: String,
  password: String,
  customFields: [{ type: String }],
  attachments: [{ type: String }]
});

userSchema.pre('save', async function(next) {
  if (this.isModified('password')) {
    this.password = await bcrypt.hash(this.password, 8);
  }
  next();
});

const User = mongoose.model('User', userSchema);

module.exports = User;
```

```javascript
// data.js
const mongoose = require('mongoose');

const dataSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  customFields: [{ type: String }],
  attachments: [{ type: String }]
});

const Data = mongoose.model('Data', dataSchema);

module.exports = Data;
```

```javascript
// progress.js
const mongoose = require('mongoose');

const progressSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  milestones: [{ type: String }],
  deadlines: [{ type: String }]
});

const Progress = mongoose.model('Progress', progressSchema);

module.exports = Progress;
```

```javascript
// notification.js
const mongoose = require('mongoose');

const notificationSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  message: String,
  type: String
});

const Notification = mongoose.model('Notification', notificationSchema);

module.exports = Notification;
```

```javascript
// routes/user.js
const express = require('express');
const router = express.Router();
const User = require('../models/user');

router.post('/register', async (req, res) => {
  try {
    const user = new User(req.body);
    await user.save();
    res.send(user);
  } catch (err) {
    res.status(400).send(err);
  }
});

router.post('/login', async (req, res) => {
  try {
    const user = await User.findOne({ email: req.body.email });
    if (!user) {
      res.status(401).send({ message: 'Invalid email or password' });
    } else {
      const isValidPassword = await bcrypt.compare(req.body.password, user.password);
      if (!isValidPassword) {
        res.status(401).send({ message: 'Invalid email or password' });
      } else {
        res.send(user);
      }
    }
  } catch (err) {
    res.status(400).send(err);
  }
});

module.exports = router;
```

```javascript
// routes/data.js
const express = require('express');
const router = express.Router();
const Data = require('../models/data');

router.get('/get', async (req, res) => {
  try {
    const data = await Data.find({ userId: req.query.userId });
    res.send(data);
  } catch (err) {
    res.status(400).send(err);
  }
});

router.post('/create', async (req, res) => {
  try {
    const data = new Data(req.body);
    await data.save();
    res.send(data);
  } catch (err) {
    res.status(400).send(err);
  }
});

module.exports = router;
```

```javascript
// routes/progress.js
const express = require('express');
const router = express.Router();
const Progress = require('../models/progress');

router.get('/get', async (req, res) => {
  try {
    const progress = await Progress.find({ userId: req.query.userId });
    res.send(progress);
  } catch (err) {
    res.status(400).send(err);
  }
});

router.post('/create', async (req, res) => {
  try {
    const progress = new Progress(req.body);
    await progress.save();
    res.send(progress);
  } catch (err) {
    res.status(400).send(err);
  }
});

module.exports = router;
```

```javascript
// routes/notification.js
const express = require('express');
const router = express.Router();
const Notification = require('../models/notification');

router.get('/get', async (req, res) => {
  try {
    const notification = await Notification.find({ userId: req.query.userId });
    res.send(notification);
  } catch (err) {
    res.status(400).send(err);
  }
});

router.post('/create', async (req, res) => {
  try {
    const notification = new Notification(req.body);
    await notification.save();
    res.send(notification);
  } catch (err) {
    res.status(400).send(err);
  }
});

module.exports = router;