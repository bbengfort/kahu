class BaseController < ApplicationController
  before_action :require_login

  def require_admin
    unless signed_in? && current_user.admin?
      deny_access("Administrator access required")
    end
  end
end
