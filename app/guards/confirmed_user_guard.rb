class ConfirmedUserGuard < Clearance::SignInGuard
  def call
    if user_confirmed?
      next_guard
    else
      failure "Access not yet confirmed by administrator."
    end
  end

  def user_confirmed?
    signed_in? && current_user.email_confirmed_at.present?
  end
end
