// backend_node/db/connection.ts
import sqlite3 from 'sqlite3';

// Open a database in memory or a file-based one
const db = new sqlite3.Database('./database.sqlite', (err) => {
  if (err) {
    console.error('Failed to open the database:', err);
  } else {
    console.log('Connected to the SQLite database.');
  }
});

export default db;
