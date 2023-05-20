import env from '../../env';
import bcrypt from 'bcrypt'
/**
   * isValidEmail helper method
   * @param {string} email
   * @returns {Boolean} True or False
   */
const isValidEmail = (email) => {
  const regEx = /\S+@\S+\.\S+/;
  return regEx.test(email);
};

/**
   * validatePassword helper method
   * @param {string} password
   * @returns {Boolean} True or False
   */
const validatePassword = (password) => {
  if (password.length <= 5 || password === '') {
    return false;
  } return true;
};
/**
   * isEmpty helper method
   * @param {string, integer} input
   * @returns {Boolean} True or False
   */
const isEmpty = (input) => {
  if (input === undefined || input === '') {
    return true;
  }
  if (input.replace(/\s/g, '').length) {
    return false;
  } return true;
};

/**
   * empty helper method
   * @param {string, integer} input
   * @returns {Boolean} True or False
   */
const empty = (input) => {
  if (input === undefined || input === '') {
    return true;
  }
};

/**
   * empty helper method
   * @param {string} input
   */

const hashPassword = (password) =>{
    bcrypt.hash(password, process.env.SALTROUNDS)
    .then(hash=>{
        userHash=hash;
        console.log(`Hash Password: ${hash}`);
        if(validateUser(password,hash)){return true;}
    })
    .catch(err=>{
        res.send({err: err.message});
    })
    
}

const validateUser=(password,hash)=>{
    bcrypt
    .compare(password, hash)
    .then(res => {
      console.log(res) 
      return true
    })
    .catch(err => { console.error({err:err.message}) });
}

const generateUserTokens = (email, id, is_admin, first_name, last_name)=>{
    const token = jwt.sign({
        email,
        user_id: id,
        is_admin,
        first_name,
        last_name
    },
    env.secret, {expiresIn: '3d'});
    return token;
}

export {
  isValidEmail,
  validatePassword,
  isEmpty,
  empty
};