import { createUser, getUsers, getUserById } from '../db/models/User';

const testDbFunctions = async () => {
  // Test createUser
  const userId = await createUser('John Doe', 'john@example.com');
  console.log(`Created user with ID: ${userId}`);

  // Test getUsers
  const users = await getUsers();
  console.log('Users in the database:', users);

  // Test getUserById
  const user = await getUserById(userId);
  console.log('User retrieved by ID:', user);

  // Check if data matches
  if (user && user.name === 'John Doe' && user.email === 'john@example.com') {
    console.log('Database test passed!');
  } else {
    console.log('Database test failed.');
  }
};

testDbFunctions().catch((error) => console.error('Error testing DB:', error));
