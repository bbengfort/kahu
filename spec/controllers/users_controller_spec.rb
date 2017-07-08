require "rails_helper"

RSpec.describe UsersController, type: :controller do

  describe "#index" do

    context "when administrator signed in" do
      it "should render users index" do
        user = User.new(email_confirmed_at: Time.current, is_admin:true)
        sign_in_as(user)

        get :index
        expect(response).to have_http_status(:ok)
        expect(response).to render_template("users/index")
      end
    end

    context "when regular user signed in" do
      it "should require admin access" do
        user = User.new(email_confirmed_at: Time.current)
        sign_in_as(user)

        get :index
        expect(response).to redirect_to(:root)
      end
    end

    context "when no user signed in" do
      it "should require admin access" do
        get :index
        expect(response).to redirect_to(:sign_in)
      end

    end

  end

    describe "#new" do
      it "should render the registration template" do
        get :new
        expect(response).to have_http_status(:ok)
        expect(response).to render_template("users/new")
      end
    end

    describe "#create" do
      context "without valid attribues" do
        it "should validate email uniqueness"
        it "should require a strong password"
      end

      context "with valid attributes" do
        it "creates user and sends confirmation email" do
          email = "user@example.com"

          post :create, params: {user: { email: email, password: "password" }}
          expect(controller.send :current_user).to be_nil
          expect(last_email_confirmation_token).to be_present
          should_deliver_email(
            to: Rails.application.secrets.kahu_admin_email,
            subject: "User Requesting Access to Kahu"
          )
        end
      end
    end

    private

    def should_deliver_email(to:, subject:)
      expect(ActionMailer::Base.deliveries).not_to be_empty
      email = ActionMailer::Base.deliveries.last
      expect(email).to deliver_to(to)
      expect(email).to have_subject(subject)
    end

    def last_email_confirmation_token
      User.last.email_confirmation_token
    end

end
