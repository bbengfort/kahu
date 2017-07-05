Rails.application.routes.draw do
  # Static Pages
  root 'static_pages#home'

  get '/help', to: 'static_pages#help'
  get '/about', to: 'static_pages#about'

  # Clearance Routes
  resources :passwords, controller: "clearance/passwords", only: [:create, :new]
  resource :session, controller: "sessions", only: [:create]

  resources :users, controller: "users", only: [:create] do
    resource :password,
      controller: "clearance/passwords",
      only: [:create, :edit, :update]
  end

  get "/login" => "sessions#new", as: "sign_in"
  delete "/logout" => "sessions#destroy", as: "sign_out"
  get "/register" => "users#new", as: "sign_up"

  # API Routes
  namespace :api do
      resources :status, only: :index
  end

end
