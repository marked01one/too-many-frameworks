class TodoUser < ApplicationRecord
  self.table_name = "todo_users"

  validates :user_name, presence: true, uniqueness: true, length: { maximum: 31 }
  validates :user_password, presence: true, length: { maximum: 31 }, format: { with: /\A(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#\$%\^&\*()_+}{:;'?\/>,<])(?!.*\s).{6,31}\z/ }
  validates :user_email, presence: true, uniqueness: true, length: { maximum: 31 }, format: { with: URI::MailTo::EMAIL_REGEXP }
end
