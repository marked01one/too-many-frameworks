class TodosController < ApplicationController

  def index 
    @todo_list_id = params[:list]
    @user_id = params[:user]
    @todo_id = params[:id]

    if params.has_key?(:user)
      if params.has_key?(:id)
        @todos = Todo.where(id: @todo_id, user_id: @user_id)
      elsif params.has_key?(:list)
        @todos = Todo.where(todo_list_id: @todo_list_id, user_id: @user_id)
      else
        @todos = Todo.where(user_id: @user_id)
      end
    end

    
    if not @todos
      render json: { error: 'Bad request error. User parameter is required' }, status: :bad_request
    else
      response = { statusCode: 200, content: @todos }
      render json: response.to_json, content_type: "application/json"
    end
  end

end