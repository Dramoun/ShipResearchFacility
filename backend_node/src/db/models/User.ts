// backend_node/db/models/User.ts
import db from '../connections';
import sqlite3 from 'sqlite3';

// Simple user model to interact with the "users" table
export const createUser = (name: string, email: string) => {
  return new Promise<number>((resolve, reject) => {
    const stmt = db.prepare('INSERT INTO users (name, email) VALUES (?, ?)');
    
    // Explicitly typing 'this' to be the correct type
    stmt.run(name, email, function (this: sqlite3.RunResult, err: Error | null) {
      if (err) reject(err);
      else resolve(this.lastID);  // 'this' now properly typed as RunResult
    });

    stmt.finalize();
  });
};

export const getUsers = () => {
  return new Promise<any[]>((resolve, reject) => {
    db.all('SELECT * FROM users', (err, rows) => {
      if (err) reject(err);
      else resolve(rows);
    });
  });
};

export const getUserById = (id: number) => {
  return new Promise<any>((resolve, reject) => {
    db.get('SELECT * FROM users WHERE id = ?', [id], (err, row) => {
      if (err) reject(err);
      else resolve(row);
    });
  });
};
