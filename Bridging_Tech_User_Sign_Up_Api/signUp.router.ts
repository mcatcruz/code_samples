import { Router, Request, Response } from 'express';
import { pool } from '../dbconfig';
import Logger from '../logger';
import bcrypt from 'bcrypt';

import { UserSignUp } from './signUp.interface';

export const userSignUpRouter = Router();

/* POST NEW USER
Creates a new row in users table. Upon creation of a new user, a new row in users_points_history is created. 

Endpoint: /signup
Method: POST
Response: Returns message indicating that a new user has been created.
*/

userSignUpRouter.post('/signup', async (req: Request, res: Response) => {
  try {
    const newUser: UserSignUp = {
      ...req.body,
      parent_email: req.body.parent_email ?? null, // Ensure parent_email is null if not provided
      date_of_birth: new Date(req.body.date_of_birth)
        .toISOString()
        .split('T')[0], // Convert date_of_birth to YYYY-MM-DD
      agreed_to_terms: req.body.agreed_to_terms ?? false,
    };

    // Check for existing username
    const usernameInUseQuery = 'SELECT 1 FROM users WHERE username=$1';
    const usernameInUseResult = await pool.query(usernameInUseQuery, [
      newUser.username,
    ]);

    if (usernameInUseResult.rowCount) {
      return res.status(409).send('Username already in use.');
    }

    // Check for existing user email
    const emailInUseQuery = 'SELECT 1 FROM users WHERE user_email=$1';
    const emailInUseQueryResult = await pool.query(emailInUseQuery, [
      newUser.user_email,
    ]);

    if (emailInUseQueryResult.rowCount) {
      return res.status(409).send('Email already in use.');
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(newUser.password, 10);

    const initializeUserQuery = `
            INSERT INTO users (username, password, user_email, parent_email, date_of_birth, agreed_to_terms) 
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *;`;

    const initializeUserResult = await pool.query(initializeUserQuery, [
      newUser.username,
      hashedPassword,
      newUser.user_email,
      newUser.parent_email,
      newUser.date_of_birth,
      newUser.agreed_to_terms,
    ]);

    if (initializeUserResult.rowCount === 0) {
      return res.status(500).send('New user was not created.');
    }

    // Create new row in user_points_history
    const userId = initializeUserResult.rows[0].user_id;

    const initializeUserPointsHistoryQuery = `
        INSERT INTO users_points_history (user_id, points_total, points_earned, login_streak) 
        VALUES ($1, $2, $3, $4)
        RETURNING *;`;

    const initializeUserPointsHistory = await pool.query(
      initializeUserPointsHistoryQuery,
      [userId, 0, 0, 0]
    );

    return res.status(201).send({
      message: 'New user created successfully.',
      user: {
        id: userId,
        username: newUser.username,
        pointsHistory: initializeUserPointsHistory.rows[0],
      },
    });
  } catch (e) {
    if (e instanceof Error) {
      Logger.error(`Error in creating new user: ${e.message}`);
    } else {
      Logger.error('An unexpected error occurred.');
    }

    res.status(500).send('An error occurred while creating new user.');
  }
});
