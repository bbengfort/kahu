class EmailConfirmationsController < ApplicationController

  def update
    user = User.find_by!(email_confirmation_token: params[:token])
    user.confirm_email

    # TODO: Redirect to users listing
    redirect_to users_path, notice: "#{user.email} confirmed"
  end

end
