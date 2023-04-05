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

  /**
   * @param {object} req
   * @param {object} res
   * @returns {string} 
   */
const createUser = async(req, res)=>{
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
const createUserQuery = await client.query(`INSERT INTO USER (EMAIL, PASSWORD, FIRST_NAME, LAST_NAME, PAN ) VALUES($1, $2, $2, $4, $5)`, [email, hashPassword, first_name, last_name, pan]);

//Now Creating the 
try {
    const { rows } = await dbQuery.query(createUserQuery, [email, hashPassword, first_name, last_name, pan]);
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


const signInQuery = async(req, res)