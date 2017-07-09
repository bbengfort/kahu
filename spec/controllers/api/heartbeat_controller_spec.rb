require "rails_helper"

RSpec.describe Api::HeartbeatController, type: :controller do

  before do
    @machine = Machine.create(
      hostname: "foo", ip_address: "192.168.1.1"
    )
    @headers = {
      "X-Api-Key" => @machine.apikey,
      "Accept" => "application/json",
    }
  end

  describe "#create" do

    before do
      request.headers.merge(@headers)
    end

    it "should update last seen when it is nil " do

      expect(@machine.last_seen).to be_nil
      post :create

      @machine.reload
      expect(@machine.last_seen).to be_within(5.second).of(Time.now)

    end

    it "should update last seen when it is not nil" do
      @machine.update(last_seen: Time.now - 1.day)
      post :create

      @machine.reload
      expect(@machine.last_seen).to be_within(5.second).of(Time.now)
    end

    it "should change ip address on demand" do
      post :create, params: {"ip_address": "192.168.10.89"}
      @machine.reload
      expect(@machine.ip_address).to eq("192.168.10.89")
    end

    it "should not change ip address if not provided" do
      post :create, params: {"ip_address": ""}
      expect(@machine.ip_address).to eq("192.168.1.1")
    end

  end

end
