const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;


app.use(cors());               
app.use(express.json());       


app.post('/chat', async (req, res) => {
  try {
    const { query, session_id } = req.body;
    const chatEndpoint = 'https://drrobot9-doctor-robot-ai.hf.space/ask';
    
    const payload = {
      query: query || 'Hello, how are you?',
      session_id: session_id || `test-${Date.now()}`,
    };
    
    const start = Date.now();
    const response = await fetch(chatEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    
    const data = await response.json();
    
    res.json({
      success: true,
      endpoint: 'chat',
      responseTime: `${Date.now() - start}ms`,
      statusCode: response.status,
      data,
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});


app.post('/water', async (req, res) => {
  try {
    const { state, country } = req.body;
    const waterEndpoint = 'https://drrobot9-doctor-robot-waterborn-disease.hf.space/predict';
    
    const payload = {
      state: state || 'kaduna',
      country: country || 'nigeria',
    };
    
    const start = Date.now();
    const response = await fetch(waterEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    
    const data = await response.json();
    
    res.json({
      success: true,
      endpoint: 'water',
      responseTime: `${Date.now() - start}ms`,
      statusCode: response.status,
      data,
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});


app.post('/both', async (req, res) => {
  try {
    const chatEndpoint = 'https://drrobot9-doctor-robot-ai.hf.space/ask';
    const waterEndpoint = 'https://drrobot9-doctor-robot-waterborn-disease.hf.space/predict';
    
    const chatPayload = {
      query: 'Hello, test connection',
      session_id: `test-${Date.now()}`,
    };
    
    const waterPayload = {
      state: 'kaduna',
      country: 'nigeria',
    };
    
    const start = Date.now();
    
    const [chatRes, waterRes] = await Promise.allSettled([
      fetch(chatEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(chatPayload),
      }),
      fetch(waterEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(waterPayload),
      }),
    ]);
    
    const results = {
      chat: chatRes.status === 'fulfilled' ? await chatRes.value.json() : null,
      water: waterRes.status === 'fulfilled' ? await waterRes.value.json() : null,
    };
    
    res.json({
      success: true,
      responseTime: `${Date.now() - start}ms`,
      results,
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});


app.get('/test', async (req, res) => {
  const { type } = req.query;
  
  if (!type) {
    return res.json({
      message: 'Test endpoint',
      usage: '/test?type=chat or /test?type=water',
    });
  }
  
  try {
    if (type === 'chat') {
      const response = await fetch('https://drrobot9-doctor-robot-ai.hf.space/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: 'Hello',
          session_id: `get-${Date.now()}`,
        }),
      });
      const data = await response.json();
      return res.json(data);
    }
    
    if (type === 'water') {
      const response = await fetch('https://drrobot9-doctor-robot-waterborn-disease.hf.space/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          state: 'kaduna',
          country: 'nigeria',
        }),
      });
      const data = await response.json();
      return res.json(data);
    }
    
    res.status(400).json({ error: 'Invalid type. Use chat or water' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});


app.get('/', (req, res) => {
  res.json({ message: 'Doctor Robot Express Backend', endpoints: ['/chat', '/water', '/both', '/test'] });
});


app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});