import { Pool } from "pg";

import dotenv from 'dotenv'

dotenv.config();

try{
const databaseConfig = { connectionString: process.env.DATABASE_URL };
const pool = new Pool(databaseConfig);
console.log("Database Connected Successfully");
}
catch(err){
    console.log("Error while connecting to database");
    console.log({err: err.message});
}

export default pool;