import { createUsers, signInQuery, getUserbyID } from '../controllers/userControllers'
const { createUsers } = require('../controllers/controller');
const authorize = require('../helpers/verifyAuth');
const express= require('express');
const router = express.Router();

// SignIn and SignUp
router.post('/createUser', createUsers);
router.post('/signin', signInQuery)

// Operations on Users
router.get('/users/:id', authorize, getUserbyID);


module.exports =  router;