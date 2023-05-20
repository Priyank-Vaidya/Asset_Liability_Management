import { Client, Pool } from "pg";

import dotenv from 'dotenv'

dotenv.config();

try{
const databaseConfig = {  user: 'priyank',
host: 'localhost',
database: 'gfghackathon',
password: process.env.PASSWORD,
PORT: process.env.PORT,
max: 20,
idleTimeoutMillis: 30000,
connectionTimeoutMillis: 2000,
};
const pool = new Client(databaseConfig);
pool.connect();
console.log("Database Connected Successfully");
}
catch(err){
    console.log("Error while connecting to database");
    console.log({err: err.message});
}

export default pool;