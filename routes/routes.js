const {createUsers, getUserbyID} = require('../controllers/controller');
const express= require('express');
const router = express.Router();

router.get('/users/:id', getUserbyID);
router.post('/createUser', createUsers);

module.exports =  router;