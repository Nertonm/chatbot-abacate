-- Create database and a dedicated user for the application
CREATE DATABASE IF NOT EXISTS chatbot_db;

-- Create application user if it doesn't exist and grant privileges
CREATE USER IF NOT EXISTS 'chatbot_user'@'%' IDENTIFIED BY 'chatbot_password';
GRANT ALL PRIVILEGES ON chatbot_db.* TO 'chatbot_user'@'%';
FLUSH PRIVILEGES;

USE chatbot_db;

CREATE TABLE IF NOT EXISTS chat_response (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(500) UNIQUE NOT NULL,
    answer TEXT NOT NULL
);