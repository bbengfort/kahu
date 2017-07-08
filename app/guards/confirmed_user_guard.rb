class ConfirmedUserGuard < Clearance::SignInGuard
  def call
    if user_confirmed? || current_user.nil?
      # A nil user (e.g. the user could not be looked up in the database)
      # will cause user_confirmed? to return False. Therefore do not guard
      # against nil users, only those who are not confirmed.
      next_guard
    else
      failure "Access not yet confirmed by administrator."
    end
  end

  def user_confirmed?
    signed_in? && current_user.confirmed?
  end
end
