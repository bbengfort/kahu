require 'rails_helper'

RSpec.describe Machine, type: :model do

  it "should require a hostname" do
    m = Machine.create
    expect(m.valid?).to be(false)
  end

  it "should require a unique hostname" do
    m1 = Machine.create(hostname: "foo")
    expect(m1.valid?).to be(true)

    m2 = Machine.create(hostname: "foo")
    expect(m2.valid?).to be(false)
  end

  it "should validate mac addresses" do
    m = Machine.create(hostname: "foo", mac_address: "notamacaddress")
    expect(m.valid?).to be(false)

    m = Machine.create(hostname: "foo", mac_address: "aa:bb:cc:11:22:33")
    expect(m.valid?).to be(true)
  end

  it "should be active when created" do
    m = Machine.create(hostname: "foo")
    expect(m.active).to be(true)
  end

  it "should generate an api key on create" do
    m = Machine.create(hostname: "foo")
    expect(m.apikey).not_to be_empty
  end

  it "should lookup latitude and longitude on create" do
    m = Machine.create(hostname: "foo", ip_address: "192.168.1.1")
    expect(m.latitude).not_to be_nil
    expect(m.longitude).not_to be_nil
  end

  it "should not lookup latitude and longitude without IP address"
  it "should lookup latitude and longitude on save if IP address changed"

  it "should be addressed by ip address" do
    m = Machine.new(hostname: "foo", ip_address: "192.168.1.1")
    expect(m.addressed_by).to eq(m.ip_address)
  end

  it "should be addressed by domain" do
    m = Machine.new(hostname: "foo", domain: "test.example.com")
    expect(m.addressed_by).to eq(m.domain)
  end

  it "should be addressed by domain even if ip address exists" do
    m = Machine.new(hostname: "foo", ip_address: "192.168.1.1", domain: "test.example.com")
    expect(m.addressed_by).to eq(m.domain)
  end

end
