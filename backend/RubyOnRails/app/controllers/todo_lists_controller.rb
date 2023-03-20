class TodoListsController < ApplicationController

  def index 
    @todo_list_id = params[:id]
    @user_id = params[:user]

    
    if params.has_key?(:user)
      if params.has_key?(:id)
        @todo_lists = TodoList.where(id: @todo_list_id, user_id: @user_id)
      else
        @todo_lists = TodoList.where(user_id: @user_id)
      end
    end

    if not @todo_lists
      render json: { error: 'Bad request error. User parameters required' }, status: :bad_request
    else
      response = { statusCode: 200, content: @todo_lists }
      render json: response.to_json, content_type: "application/json"
    end
  end
end