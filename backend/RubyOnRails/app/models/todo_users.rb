class TodoUser < ApplicationRecord
  validates :user_name, 
    presence: true, 
    uniqueness: true, 
    length: { maximum: 31 }
  
  validates :user_password, 
    presence: true, 
    length: { in: 6..31 }, 
    format: { with: "/(?=^.{6,31}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&amp;*()_+}{&quot;:;'?\/&gt;.&lt;,])(?!.*\s).*\z/" }
  
  validates :user_email, 
    presence: true, 
    uniqueness: true, 
    length: { maximum: 31 }, 
    format: { with: URI::MailTo::EMAIL_REGEXP }
  
  self.table_name = 'todo_users'
end