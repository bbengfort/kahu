require 'rails_helper'

RSpec.describe Replica, type: :model do

  before do
    @m = Machine.create(hostname: "foo", ip_address: "192.168.1.1")
  end

  it "should correctly be created" do
    r = Replica.create(precedence: 10, port: 3264, machine: @m)
    expect(r.valid?).to be(true)
  end

  it "should require a precedence" do
    r = Replica.new(port: 3264, machine: @m)
    expect(r.valid?).to be(false)
  end

  it "should require a port" do
    r = Replica.new(precedence: 10, machine: @m)
    expect(r.valid?).to be(false)
  end

  it "should require a machine" do
    r = Replica.new(precedence: 10, port: 3264)
    expect(r.valid?).to be(false)
  end

  it "should constrain the port range" do
    r1 = Replica.new(precedence: 10, machine: @m, port: 22)
    expect(r1.valid?).to be(false)

    r2 = Replica.new(precedence: 10, machine: @m, port: 9999999)
    expect(r2.valid?).to be(false)
  end

  it "should be correctly addressed" do
    r = Replica.new(precedence: 10, port: 3264, machine: @m)
    expect(r.address).to eq("192.168.1.1:3264")
  end

end
