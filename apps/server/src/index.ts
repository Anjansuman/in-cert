import express from "express";
import dotenv from 'dotenv';
import router from "./routes/route";

dotenv.config();

const app = express();
app.use(express.json());

app.use('/api/v1', router);

app.listen(8080, () => console.log('Server listening at PORT: ', 8080));