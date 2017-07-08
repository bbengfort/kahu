class EmailConfirmationsController < ApplicationController

  def update
    user = User.find_by!(email_confirmation_token: params[:token])
    user.confirm_email

    # TODO: Redirect to users listing 
    redirect_to root_path, notice: t("flashes.confirmed_email")
  end

end
