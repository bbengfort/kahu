require 'rails_helper'

class InheritsFromApiController < ApiController
  def show
    data = {success: true}
    render json: data.to_json
  end
end

RSpec.describe InheritsFromApiController, type: :controller do

  before do
    Rails.application.routes.draw do
      # add the test route
      get '/foo' => "inherits_from_api#show"

      # re-drawing routes means that you lose any routes you defined in routes.rb
      # so you have to add those back here if your controller references them
      get "/login" => "sessions#new", as: "sign_in"
    end
  end

  after do
    # be sure to reload routes after the tests run, otherwise all your
    # other controller specs will fail
    Rails.application.reload_routes!
  end

  context "when no authentication is present" do
    it "requires login" do
      get :show
      expect(response).to redirect_to(:sign_in)
    end
  end

  context "when an api key is provided" do
    before do
      @machine = Machine.create(hostname: "foo")
    end

    it "returns ok on correct key" do
      request.headers["X-Api-Key"] = @machine.apikey
      get :show
      expect(response).to have_http_status(:ok)
    end

    it "returns not authorized on incorrect key" do
      request.headers["Accept"] = "application/json"
      request.headers["X-Api-Key"] = @machine.apikey + "badkey"
      get :show
      expect(response).to have_http_status(:unauthorized)
    end
  end

  context "when a user is logged in" do
    before do
        user = User.new
        sign_in_as(user)
    end

    it "does not require an apikey" do
      get :show
      expect(response).to have_http_status(:ok)
    end
  end

end
