class TodoList < ApplicationRecord
  belongs_to :user,
    class_name: 'TodoUser',
    foreign_key: 'todo_user_id'
  
  validates :name,
    presence: true,
    length: { maximum: 255 }
  
  self.table_name = 'todo_lists'

end