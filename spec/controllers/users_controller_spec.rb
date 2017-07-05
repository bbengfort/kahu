require "rails_helper"

RSpec.describe UsersController, type: :controller do

    describe "GET new" do
        before do
            get :new
        end

        it "responds with success" do
            expect(response).to have_http_status(:ok)
        end

        it "renders register template" do
            expect(response).to render_template("users/new")
        end
    end

end
