Rails.application.routes.draw do
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Defines the root path route ("/")
  # root "articles#index"
  resources :users, controller: "todo_users", model_name: "TodoUserApi", only: [:index, :create, :destroy]
end
