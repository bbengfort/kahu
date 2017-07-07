# Gemfile for Kahu
# frozen_string_literal: true

# Read the Ruby version
RUBY_VERSION = File.read(".ruby-version").chomp.freeze
ruby RUBY_VERSION

# Sources
source 'https://rubygems.org'

git_source(:github) do |repo_name|
  repo_name = "#{repo_name}/#{repo_name}" unless repo_name.include?("/")
  "https://github.com/#{repo_name}.git"
end

# Global Dependencies
gem "clearance"
gem "httparty"
gem "ipaddress"
gem 'jbuilder', '~> 2.5'
gem 'rails', '~> 5.1.2'
gem "pacecar"
gem 'pg'
gem 'puma', '~> 3.7'
gem 'turbolinks', '~> 5'

# Assets
gem 'bootstrap-sass'
gem 'coffee-rails', '~> 4.2'
gem 'font-awesome-sass'
gem "jquery-rails"
gem 'sass-rails', '~> 5.0'
gem 'uglifier', '>= 1.3.0'

# Development and Test Dependencies
group :development, :test do
  gem 'byebug', platforms: [:mri, :mingw, :x64_mingw]
  gem 'capybara', '~> 2.13'
  gem "dotenv-rails"
  gem "rspec-rails"
  gem 'rails-controller-testing'
  gem 'selenium-webdriver'
end

# Development Dependencies
group :development do
  gem 'web-console', '>= 3.3.0'
  gem "letter_opener"
  gem 'listen', '>= 3.0.5', '< 3.2'
  gem 'spring'
  gem 'spring-watcher-listen', '~> 2.0.0'
  gem "spring-commands-rspec"
end

# Test Dependencies
group :test do
  gem "rspec-collection_matchers"
  gem "shoulda-matchers", require: false
  gem "webmock"
end
