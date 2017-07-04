Clearance.configure do |config|
  config.routes = false
  config.cookie_domain = ".kahu.bengfort.com"
  config.mailer_sender = "server@bengfort.com"
  config.rotate_csrf_on_sign_in = true
end
