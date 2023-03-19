class TodoUser < ApplicationRecord
  self.table_name = "todo_users"

  has_many :todo_lists, class_name: 'TodoList', dependent: :destroy
  has_many :todos, class_name: 'Todo', dependent: :destroy

  validates :user_name, presence: true, uniqueness: true, length: { maximum: 31, minimum: 4 }, format: { with: /\A[a-z0-9]+(?:-[a-z0-9]+)*\z/ }
  validates :user_password, presence: true, length: { maximum: 31. minimum: 8 }, format: { with: /\A(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#\$%\^&\*()_+}{:;'?\/>,<])(?!.*\s).{6,31}\z/ }
  validates :user_email, presence: true, uniqueness: true, length: { maximum: 31 }, format: { with: URI::MailTo::EMAIL_REGEXP }
end
