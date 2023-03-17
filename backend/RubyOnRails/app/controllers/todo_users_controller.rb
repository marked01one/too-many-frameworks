class TodoUsersController < ApplicationController
  def index 
    @todo_users = TodoUser.all
    render json: @todo_users
  end
end