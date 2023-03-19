-- @block Create new test users
INSERT INTO todo_users (user_name, user_password, user_email)
VALUES 
  ('alex1234', 'Pa$$w0rd', 'alex@test.com'),
  ('bob1234', 'Pa$$w0rd', 'bob@test.com'),
  ('christine1234', 'Pa$$w0rd', 'christine@test.com');
SELECT * FROM todo_users;


-- @block Create new test todo lists
INSERT INTO todo_lists (user_id, name)
VALUES 
  (1, 'Alex Daily Tasks'), (1, 'Alex Weekly Tasks'), (1, 'Alex Upcoming Tasks'),
  (2, 'Bob Daily Tasks'), (2, 'Bob Weekly Tasks'), (2, 'Bob Upcoming Tasks'),
  (3, 'Christine Daily Tasks'), (3, 'Christine Weekly Tasks'), (3, 'Christine Upcoming Tasks');
SELECT * FROM todo_lists;


-- @block Test the new user todo lists
SELECT todo_users.user_name, todo_users.user_email, todo_lists.name 
FROM todo_lists INNER JOIN todo_users
ON todo_lists.user_id = todo_users.id
AND todo_users.id = 2;

