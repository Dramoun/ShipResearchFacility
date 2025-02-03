// backend_node/routes/userRoutes.ts
import express from 'express';
import { createUser, getUsers, getUserById } from '../db/models/User';

const router = express.Router();

// Route to get all users
router.get('/users', async (req, res) => {
  try {
    const users = await getUsers();
    res.json(users);
  } catch (error) {
    res.status(500).send('Error fetching users');
  }
});

// Route to get a user by ID
router.get('/users/:id', async (req, res) => {
  try {
    const user = await getUserById(parseInt(req.params.id));
    if (user) {
      res.json(user);
    } else {
      res.status(404).send('User not found');
    }
  } catch (error) {
    res.status(500).send('Error fetching user');
  }
});

// Route to create a new user
router.post('/users', async (req, res) => {
  const { name, email } = req.body;
  try {
    const userId = await createUser(name, email);
    res.status(201).json({ id: userId });
  } catch (error) {
    res.status(500).send('Error creating user');
  }
});

export default router;
