-- @block Generate all tables
CREATE TABLE todo_users (
  id SERIAL PRIMARY KEY,
  user_name VARCHAR(31) NOT NULL UNIQUE,
  user_password VARCHAR(31) NOT NULL,
  user_email VARCHAR(31) UNIQUE NOT NULL
);

CREATE TABLE todo_lists (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES todo_users(id) ON DELETE CASCADE
);

CREATE TABLE todos (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  completed BOOLEAN DEFAULT false,
  todo_list_id INTEGER,
  FOREIGN KEY (todo_list_id) REFERENCES todo_lists(id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES todo_users(id) ON DELETE CASCADE
);




-- @block Return all users



-- ? Testing users. If query returns with error --> It's working properly

-- @block Test adding users with duplicate name
INSERT INTO todo_users (user_name, user_password, user_email)
  VALUES ('alex1234', 'Pa$$w0rd', 'alex@faketest.com')

-- @block Test adding users with duplicate emails
INSERT INTO todo_users (user_name, user_password, user_email)
  VALUES ('alex1234fake', 'Pa$$w0rd', 'alex@test.com')


-- ? Testing users. If query returns with error --> It's working properly




-- ! WARNING: THESE QUERY BLOCKS WILL DELETE DATA, READ CAREFULLY BEFORE RUNNING

-- @block Delete user with specific name
DELETE FROM users
WHERE (name='alex1234')


-- @block Delete all tables 
DROP TABLE todos;
DROP TABLE todo_lists;
DROP TABLE todo_users;