class UsersController < Clearance::UsersController
  attr_reader :user

  def index
    require_admin
    @users = User.all
  end

  def create
    @user = user_from_params
    @user.email_confirmation_token = Clearance::Token.new

    if @user.save
      AdminMailer.registration_confirmation(@user).deliver_now
      redirect_back_or url_after_create
    else
      render template: "users/new"
    end
  end

  def destroy
    require_admin
    @user = User.find(params[:id])
    @user.destroy
    redirect_to users_path
  end

  # Redfined here since UsersController doesn't inherit from BaseController
  def require_admin
    unless signed_in? && current_user.admin?
      deny_access("Administrator access required")
    end
  end

end
