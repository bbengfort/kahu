require 'rails_helper'

RSpec.describe User, type: :model do

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

  describe "#confirm_email" do
    it "sets email_confirmed_at value" do
      user = User.create(
        email: "joe@example.com",
        email_confirmation_token: "token", email_confirmed_at: nil,
      )

      user.confirm_email
      expect(user.email_confirmed_at).to be_present
    end
  end
end
