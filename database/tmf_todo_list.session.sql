-- @block Generate all tables
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(31) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(31) UNIQUE
);

CREATE TABLE todo_lists (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL DEFAULT 'none',
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE todos (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT false,
  todo_list_id INTEGER,
  FOREIGN KEY (todo_list_id) REFERENCES todo_lists(id),
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) 
);



-- @block Return all users
SELECT * FROM users

-- @block Create new test users
INSERT INTO users (name, password, email)
VALUES 
  ('alex1234', 'Pa$$w0rd', 'alex@test.com'),
  ('bob1234', 'Pa$$w0rd', 'bob@test.com'),
  ('christine1234', 'Pa$$w0rd', 'christine@test.com');



-- TODO1: Testing users. If query returns with error --> It's working properly

-- @block Test adding users with duplicate name
INSERT INTO users (name, password, email)
  VALUES ('alex1234', 'Pa$$w0rd', 'alex@faketest.com')

-- @block Test adding users with duplicate emails
INSERT INTO users (name, password, email)
  VALUES ('alex1234fake', 'Pa$$w0rd', 'alex@test.com')



-- ! WARNING: THESE QUERY BLOCKS WILL DELETE DATA, READ CAREFULLY BEFORE RUNNING

-- @block Delete user with specific name
DELETE FROM users
WHERE (name='alex1234')


-- @block Delete all tables 
DROP TABLE todos;
DROP TABLE todo_lists;
DROP TABLE users;