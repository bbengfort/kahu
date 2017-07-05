# Gemfile for Kahu
# Sources
source 'https://rubygems.org'

git_source(:github) do |repo_name|
  repo_name = "#{repo_name}/#{repo_name}" unless repo_name.include?("/")
  "https://github.com/#{repo_name}.git"
end

# Global Dependencies
gem "clearance"
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

group :development, :test do
  gem 'byebug', platforms: [:mri, :mingw, :x64_mingw]
  gem 'capybara', '~> 2.13'
  gem "dotenv-rails"
  gem 'selenium-webdriver'
end

group :development do
  gem 'web-console', '>= 3.3.0'
  gem "letter_opener"
  gem 'listen', '>= 3.0.5', '< 3.2'
  gem 'spring'
  gem 'spring-watcher-listen', '~> 2.0.0'
end
