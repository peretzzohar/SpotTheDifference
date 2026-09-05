const sqlite3 = require("sqlite3").verbose();

function createDatabase(databasePath) {
  return new sqlite3.Database(databasePath);
}

function initializeDatabase(database) {
  // TODO: Define application tables and migrations.
  return database;
}

module.exports = { createDatabase, initializeDatabase };
