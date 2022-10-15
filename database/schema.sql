CREATE DATABASE simple_accounts;
USE simple_accounts;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  hashed_password BLOB
);
