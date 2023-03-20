class TodoList < ApplicationRecord
  self.table_name = "todo_lists"

  belongs_to :todo_users, class_name: 'TodoUser', foreign_key: 'user_id'
  has_many :todos, class_name: 'Todo', dependent: :destroy
  
  validates :name, presence: true, length: { maximum: 255, minimum: 4 }, format: { with: /\A[a-z0-9]+(?:-[a-z0-9]+)*\z/ }
end
