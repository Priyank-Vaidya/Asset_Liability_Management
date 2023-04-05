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
   * @returns {}
   */
const createUser = async(req, res)=>{
    const {email, password, first_name, last_name} = req.body;
    const created_on = new Date();
    
}