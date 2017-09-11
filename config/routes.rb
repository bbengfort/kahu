Rails.application.routes.draw do
  # Static Pages
  root 'static_pages#home'

  get '/help', to: 'static_pages#help'
  get '/about', to: 'static_pages#about'

  # Clearance Routes
  resources :passwords, controller: "clearance/passwords", only: [:create, :new]
  resource :session, controller: "sessions", only: [:create]

  resources :users, controller: "users", only: [:index, :create, :destroy] do
    resource :password,
      controller: "clearance/passwords",
      only: [:create, :edit, :update]
  end

  get "/login" => "sessions#new", as: "sign_in"
  delete "/logout" => "sessions#destroy", as: "sign_out"
  get "/register" => "users#new", as: "sign_up"
  get "/confirm_email/:token" => "email_confirmations#update", as: "confirm_email"

  # Host and Replica Resources
  resources :machines do
    resources :replicas
  end

  # API Routes
  namespace :api do
      resources :status, only: :index
      resources :heartbeat, only: :create
      resources :replicas, only: :index
      resources :hosts, only: :index
  end

end
