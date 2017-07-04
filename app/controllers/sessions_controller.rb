class SessionsController < Clearance::SessionsController

  def url_after_destroy
    login_url
  end

end
