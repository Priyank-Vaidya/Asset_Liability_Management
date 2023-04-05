
import pool from './pool';

//This is used to create 2 arguments Text and Params which is required for querying in the database
//This Method will return the promise which will be used in controller for executing pool of queries


export default {
  /**
   * DB Query
   * @param {object} req
   * @param {object} res
   * @returns {object}
   */
  query(quertText, params) {
    return new Promise((resolve, reject) => {
      pool.query(quertText, params)
        .then((res) => {
          resolve(res);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
};