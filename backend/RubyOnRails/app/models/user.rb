class User < ApplicationRecord
  NAME_REGEX = "^[a-zA-Z0-9_]$"

  has_many :todo_lists, 
    depedent: :destroy
  
  has_many :assigned_todo_items, 
    class_name: 'TodoItem', 
    foreign_key: 'assigned_to_id', 
    dependent: :nullify,
  
  validates :name, 
    presence: true, 
    length: {minimum: 4, maximum: 16},
    format: { with: NAME_REGEX }
end