const express = require('express');
const bodyParser = require('body-parser');
const app = express();
require('dotenv').config();
const cors = require('cors');
const router = require('./routes/routes');
const pool = require('./db/dbConnection')


app.use(express.json());
app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));


app.get('/api/v1',router);

try{
app.listen(process.env.PORT, ()=>{
    console.log(`Server Running at port ${process.env.PORT}`);
})
}
catch(err){
    console.log("Error in listening to port");
}

//End all the clients from the pool
process.on('SIGINT', () => {
    pool.end(() => {
      console.log('Database pool has ended');
      process.exit(0);
    });
  });