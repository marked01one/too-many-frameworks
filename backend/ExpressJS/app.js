const express = require('express');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = process.env.PORT;

// 
app.get('/api/getTodos', (req, res) => {
  res.send({hello: "world"});
});


app.post('/api/postTodos', (req, res) => {
  res.send({request: "POST"});
});


app.delete('/api/deleteTodos', (req, res) => {
  res.send({delete: 'successful'});
});






app.listen(port, () => {
  console.log(`[server]: Server is running at http://localhost:${port}`);
});