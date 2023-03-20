class Todo < ApplicationRecord
  self.table_name = 'todos'

  belongs_to :todo_users, class_name: 'TodoUser', foreign_key: 'user_id'
  belongs_to :todo_lists, class_name: 'TodoList', foreign_key: 'todo_list_id'

  validates :title, presence: true, length: { maximum: 255 }
  validates :description, presence: true
  attribute :completed, default: false
end
