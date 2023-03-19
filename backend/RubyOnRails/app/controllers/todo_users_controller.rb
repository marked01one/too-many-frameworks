class TodoUsersController < ApplicationController
  
  def index 
    @user_id = params[:id]

    if params.has_key?(:id)
      @users = TodoUser.where(id: @user_id)[0]
    else
      @users = TodoUser.all()
    end

    response = { statusCode: 200, content: @users }
    render json: response.to_json, content_type: "application/json"
  end


  def create

  end


  def destroy

  end
end