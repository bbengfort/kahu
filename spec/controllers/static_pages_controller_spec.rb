require "rails_helper"

RSpec.describe StaticPagesController, type: :controller do

    before do
        base_title = "Kahu Replica Manager"
    end

    describe "#home" do
        context "when logged in" do
            before do
                user = User.new(email_confirmed_at: Time.current)
                sign_in_as(user)
                get :home
            end

            it "responds with success" do
                expect(response).to have_http_status(:ok)
            end

            it "should render the template" do
                expect(response).to render_template("static_pages/home")
            end

            it "should have correct title"
        end

        context "when logged out" do
            it "redirects to login page" do
                get :home
                expect(response).to redirect_to(:sign_in)
            end
        end
    end

    describe "#help" do
        context "when logged in" do
            before do
                user = User.new(email_confirmed_at: Time.current)
                sign_in_as(user)
                get :help
            end

            it "responds with success" do
                expect(response).to have_http_status(:ok)
            end

            it "should render the template" do
                expect(response).to render_template("static_pages/help")
            end

            it "should have correct title"
        end

        context "when logged out" do
            it "redirects to login page" do
                get :help
                expect(response).to redirect_to(:sign_in)
            end
        end
    end

    describe "#about" do
        context "when logged in" do
            before do
                user = User.new(email_confirmed_at: Time.current)
                sign_in_as(user)
                get :about
            end

            it "responds with success" do
                expect(response).to have_http_status(:ok)
            end

            it "should render the template" do
                expect(response).to render_template("static_pages/about")
            end

            it "should have correct title"
        end

        context "when logged out" do
            it "redirects to login page" do
                get :about
                expect(response).to redirect_to(:sign_in)
            end
        end
    end

end
