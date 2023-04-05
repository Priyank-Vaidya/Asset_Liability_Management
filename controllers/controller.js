
require('dotenv').config();
const Pool = require('pg').Pool

Pool.on('connect', ()=>{
    console.log("Connected to Database");
})

//Pool Configuration.
const pool = new Pool({
    user: 'priyank',
    host: 'localhost',
    database: 'gfghackathon',
    password: process.env.PASSWORD,
    PORT: process.env.PORT,
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
})


const createUsers = async (req, res)=>{
    const {name, email, phone, address, pan} = req.body
    try{
        const client = await pool.connect();
        client.query('INSERT INTO USERS(NAME, EMAIL, PHONE, ADDRESS, PAN ) VALUES ($1, $2, $3, $4, $5)', [name, email, phone, address, pan]);
        res.status(201).send("User Created Successfully");
    }
    catch(err){
        res.status(500).send({err: err.message});
        console.log("Error in Inserting Values");
    }
}

const getUserbyID = async (req, res)=>{
    const id = req.params.id;
    await pool.query('SELECT * FROM USERS WHERE id = $1', [id], (err, res)=>{
        if(err){
            res.status(500).send({err: err.message});
        console.log("Invalid ID");
        }
        else{
            res.status(200).send("Data successfully fetched");
        }
    })   
}

module.exports = async(req, res)=>{
    te
}

//End all the clients in the pool
pool.end(()=>{
    console.log("Pool has ended, No query will run now")
});

module.exports = {createUsers, getUserbyID};
