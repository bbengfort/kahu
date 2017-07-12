require_relative 'boot'

require 'rails/all'

# Require the gems listed in Gemfile, including any gems
# you've limited to :test, :development, or :production.
Bundler.require(*Rails.groups)

module Kahu
  class Application < Rails::Application
    # Set timezone to estern time
    config.time_zone = "America/New_York"

    # Initialize configuration defaults for originally generated Rails version.
    config.load_defaults 5.1

    config.autoload_paths += [
      "#{config.root}/app/serializers",
      "#{config.root}/app/validators",
    ]

    config.generators do |g|
        g.helper false
        g.routing_specs false
        g.stylesheets false
        g.test_framework :rspec
        g.view_specs false
        g.javascript_engine :js
    end
  end
end
