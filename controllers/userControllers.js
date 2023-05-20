import {
    hashPassword,
    isValidEmail,
    validatePassword,
    isEmpty,
    generateUserToken,
  } from '../helpers/validations';

  import {
    errorMessage, successMessage, status,
  } from '../helpers/status';

import pool from '../db/dbConnection';


  /**
   * @param {object} req
   * @param {object} res
   * @returns {string} 
   */
module.exports = createUser = async(req, res)=>{
    const {email, password, first_name, last_name, pan} = req.body;
    const created_on = new Date();
    if(isEmpty(email) || isEmpty(first_name) || isEmpty(last_name) || isEmpty(password)){
        return res.status(status.bad).send(errorMessage);
    }
    if (!isValidEmail(email)) {
  errorMessage.error = 'Please enter a valid Email';
  return res.status(status.bad).send(errorMessage);
    }
    if (!validatePassword(password)) {
  errorMessage.error = 'Password must be more than five(5) characters';
  return res.status(status.bad).send(errorMessage);
    }

const HashedPassword = hashPassword(password);
// const createUserQuery = await client.query(`INSERT INTO USER (EMAIL, PASSWORD, FIRST_NAME, LAST_NAME, PAN ) VALUES($1, $2, $2, $4, $5)`, [email, hashPassword, first_name, last_name, pan]);

//Now Creating the 
try {
    const { rows } = await pool.query(`INSERT INTO USER (EMAIL, PASSWORD, FIRST_NAME, LAST_NAME, PAN ) VALUES($1, $2, $2, $4, $5)`, [email, hashPassword, first_name, last_name, pan]);
    const dbResponse = rows[0];
    delete dbResponse.password;
    //Generating the new user Token

    const token = generateUserToken(dbResponse.email, dbResponse.id, dbResponse.is_admin, dbResponse.first_name, dbResponse.last_name);
    successMessage.data = dbResponse;
    successMessage.data.token = token;
    return res.status(status.created).send(successMessage);
  } catch (error) {
    if (error.routine === '_bt_check_unique') {
      errorMessage.error = 'User with that EMAIL already exist';
      return res.status(status.conflict).send(errorMessage);
    }
    errorMessage.error = 'Operation was not successful';
    return res.status(status.error).send(errorMessage);
  }
};


module.exports = signInQuery = async(req, res)=>{
  const {email, password} = req.body

  try{
    const data = await pool.query("SELECT * FROM USER WHERE EMAIL = $1", [email]);
    if(data.rows==0){
      res.status(401).send("User Not found. Sign up First");
      res.redirect('/signup');

    }
    else{
      if(hashPassword(data[0].password)){
        const token = generateUserToken({
          email:email,
        }, process.env.JWT_SECRET);

        res.status(201).json({message: "User successfully Signed In", token: token})

      }

      else{
        res.send("Please enter the Correct Passeword")
      }


    }
  }
  catch(err){
    res.send({err:err.message});
    res.status(500).json({err: "Error Occured while Connection to Server: Status 500"});
  }
}


module.exports = getUserbyID = async (req, res)=>{
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
