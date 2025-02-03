import express, { Request, Response } from 'express';
import bodyParser from 'body-parser';
import userRoutes from './routes/userRoutes';
import './../db/setup';

const app = express();
const port = process.env.PORT || 3001;

app.use(express.json());  // Middleware to parse JSON bodies

app.get('/', (req: Request, res: Response) => {
  res.send('Hello, world!');
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});




app.use(bodyParser.json());
app.use('/api', userRoutes); // API routes start with /api

