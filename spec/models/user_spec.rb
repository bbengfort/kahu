require 'rails_helper'

RSpec.describe User, type: :model do

  describe "create user" do

    it "should require an email" do
      user = User.create(password: "password")
      expect(user.valid?).to be(false)
    end

    it "should require a password" do
      user = User.create(email: "jane@example.com")
      expect(user.valid?).to be(false)
    end

    it "should create a default user with required params" do
      user = User.create(
        email: 'jane@example.com', password: 'password'
      )

      expect(user.valid?).to be(true)
      expect(user.is_admin).to be(false)
    end

  end

  describe "#full_name_or_email" do
    context "when user has name attributes" do

      it "display name is the full name" do
        user = User.new(email: 'joe@example.com', first_name: "John", last_name: "Doe")
        expect(user.full_name_or_email).to eq("John Doe")
      end

    end

    context "when user has partial name attributes" do

      it "missing last name should be email " do
        user = User.new(email: 'joe@example.com', first_name: "John")
        expect(user.full_name_or_email).to eq(user.email)
      end

      it "missing first name should be email" do
        user = User.new(email: 'joe@example.com', last_name: "Doe")
        expect(user.full_name_or_email).to eq(user.email)
      end

    end

    context "when user only has email" do
      it "display name is the email" do
        user = User.new(email: 'joe@example.com')
        expect(user.full_name_or_email).to eq(user.email)
      end
    end
  end

  describe "#admin?" do

    it "should identify aministrators" do
      user = User.new(email: "bob@example.com", password: "secret", is_admin: true)
      expect(user.admin?).to be(true)
    end

    it "should identify non-administrators" do
      user = User.new(email: "bob@example.com", password: "secret", is_admin: false)
      expect(user.admin?).to be(false)
    end

  end

  describe "#confirm_email" do
    it "sets email_confirmed_at value" do
      user = User.create(
        email: "joe@example.com", password:"password",
        email_confirmation_token: "token", email_confirmed_at: nil,
      )

      user.confirm_email
      expect(user.email_confirmed_at).to be_present
    end

    it "should identify a confirmed user" do
      user = User.new(email: "test@example.com", email_confirmed_at: Time.current)
      expect(user.confirmed?).to be(true)
    end

    it "should identify an unconfirmed user" do
      user = User.new(email: "test@example.com", email_confirmed_at: nil)
      expect(user.confirmed?).to be(false)
    end
  end
end
