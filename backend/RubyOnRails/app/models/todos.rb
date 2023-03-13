class Todo < ApplicationRecord
  belongs_to :user,
    class_name: 'TodoUser',
    foreign_key: 'todo_user_id',
  
  belongs_to :todo_list,
    class_name: 'TodoList',
    foreign_key: "todo_list_id"
  
  validates :title,
    presence: true,
    length: { maximum: 255 }
  
  validates :description,
    presence: true
  
  validates :completed,
    inclusion: { in: [true, false] }
    attribute :completed, :boolean, default: false
  
  self.table_name = 'todos'
end