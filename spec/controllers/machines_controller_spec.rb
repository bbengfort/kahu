require 'rails_helper'

RSpec.describe MachinesController, type: :controller do

  describe "GET index" do
      context "when logged out" do
          it "redirects to login page"
      end
  end

  describe "GET new" do
      context "when logged out" do
          it "redirects to login page" do
              get :new
              expect(response).to redirect_to(:sign_in)
          end
      end
  end

end