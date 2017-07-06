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

end
