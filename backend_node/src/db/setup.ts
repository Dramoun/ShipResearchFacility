// backend_node/db/setup.ts
import db from './connections';

const createTable = () => {
  console.log('Creating users table...');
  db.serialize(() => {
    db.run(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
      )
    `, (err) => {
      if (err) {
        console.error('Error creating table:', err);
      } else {
        console.log('Users table created (if it did not exist).');
      }
    });
  });
};

createTable();
