require "rails_helper"

RSpec.describe Api::StatusController, type: :controller do

  before do
    @machine = Machine.create(hostname: "foo")
    @headers = {
      "X-Api-Key" => @machine.apikey,
      "Accept" => "application/json",
    }
  end

  describe "#index" do

    before do
      request.headers.merge(@headers)
      get :index
    end

    it "should respond with status data" do
      expect(response).to have_http_status(:ok)
      data = JSON.parse(response.body)
      expect(data).to have_key("status")
      expect(data).to have_key("timestamp")
      expect(data["status"]).to eq("ok")
    end

  end

end
