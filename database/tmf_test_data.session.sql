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



-- @block Create new test todos
INSERT INTO todos (user_id, todo_list_id, title, description)
VALUES 
  (1, 1, 'Breakfast', 'Breakfast for Alex - 7:00 AM'), (1, 1, 'Lunch', 'Lunch for Alex - 12:00 PM'), (1, 1, 'Dinner', 'Dinner for Alex - 5:00 PM'),
  (2, 4, 'Breakfast', 'Breakfast for Bob - 7:00 AM'), (2, 4, 'Lunch', 'Lunch for Bob - 12:00 PM'), (2, 4, 'Dinner', 'Dinner for Bob - 5:00 PM'),
  (3, 7, 'Breakfast', 'Breakfast for Christine - 7:00 AM'), (3, 7, 'Lunch', 'Lunch for Christine - 12:00 PM'), (3, 7, 'Dinner', 'Dinner for Christine - 5:00 PM'),

  (1, 2, 'Do Laundry', 'Laundry for Alex'), (1, 2, 'Buy Groceries', 'Groceries for Alex'), (1, 2, 'Get Gas', 'Gas for Alex'),
  (2, 5, 'Do Laundry', 'Laundry for Bob'), (2, 5, 'Buy Groceries', 'Groceries for Bob'), (2, 5, 'Get Gas', 'Gas for Bob'),
  (3, 8, 'Do Laundry', 'Laundry for Christine'), (3, 8, 'Buy Groceries', 'Groceries for Christine'), (3, 8, 'Get Gas', 'Gas for Christine'),
  
  (1, 3, 'Homework', 'Homework for Alex'), (1, 3, 'Midterm', 'Midterm for Alex'), (1, 3, 'Interview', 'Interview for Alex'),
  (2, 6, 'Homework', 'Homework for Alex'), (2, 6, 'Midterm', 'Midterm for Alex'), (2, 6, 'Interview', 'Interview for Alex'),
  (3, 9, 'Homework', 'Homework for Christine'), (3, 9, 'Midterm', 'Midterm for Christine'), (3, 9, 'Interview', 'Interview for Christine');


-- @block Get all `todo_lists`
SELECT * FROM todos;


-- @block Test the new user todo lists
SELECT todo_users.user_name, todo_lists.name, todos.title, todos.description 
FROM todo_users INNER JOIN todos
ON todos.user_id = todo_users.id
AND todo_users.id = 2
INNER JOIN todo_lists
ON todos.todo_list_id = todo_lists.id;

