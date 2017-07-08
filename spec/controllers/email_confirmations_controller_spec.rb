require 'rails_helper'

RSpec.describe EmailConfirmationsController, type: :controller do

  describe "#update" do
    context "with invalid confirmation token" do
      it "raises RecordNotFound exception" do
        expect do
          get :update, params: {token: "nonexistent"}
        end.to raise_exception(ActiveRecord::RecordNotFound)
      end
    end

    context "with valid confirmation token" do

      it "confirms user" do

        user = User.create(
          email: "jane@example.com", password: "password",
          email_confirmation_token: "valid_token",
          email_confirmed_at: nil,
        )

        get :update, params: {token: "valid_token"}

        user.reload
        expect(user.email_confirmed_at).to be_present
        expect(response).to redirect_to(users_path)
      end
    end

  end

end
