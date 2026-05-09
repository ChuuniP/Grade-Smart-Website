require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const authRoutes = require('./routes/auth.routes');
const templateRoutes = require('./routes/template.routes');
const batchRoutes = require('./routes/batch.routes');
const omrRoutes = require('./routes/omr.routes');

const app = express();

app.use(cors());
app.use(express.json());

app.use('/templates', express.static(path.join(__dirname, '../templates')));

app.use('/api/auth', authRoutes);
app.use('/api/templates', templateRoutes);
app.use('/api/batches', batchRoutes);
app.use('/api/omr', omrRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
