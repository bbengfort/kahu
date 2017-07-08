class AdminMailer < ApplicationMailer

  default to: Rails.application.secrets.kahu_admin_email
  default from: Clearance.configuration.mailer_sender

  def registration_confirmation(user)
    @user = user
    mail(subject: 'User Requesting Access to Kahu')
  end

end
