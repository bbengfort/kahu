require "rails_helper"

RSpec.describe SessionsController, type: :controller do

  describe "#new" do
    # Login form
    it "should render the login form" do
      get :new
      expect(response).to have_http_status(:ok)
      expect(response).to render_template("sessions/new")
    end
  end

  describe "#create" do
    # Login post
    context "with correct credentials" do

      context "but not confirmed" do
        it "should not allow login"
      end

      context "and confirmed" do
        it "should log the user in"
      end

    end

    context "with incorrect credentials" do
      it "should not log the user in"
    end
  end

  describe "#destroy" do
    context "when a user is logged in" do
      it "should log the user out"
    end

    context "when no user is logged in" do
      it "should redirect to the login page"
    end
  end

end
