-- SQL script to create a database and a users table
CREATE DATABASE database_name;

-- SQL script to create a database and a users table
CREATE DATABASE IF NOT EXISTS database_name;

-- SQL script to use created database
USE database_name;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
