class StaticPagesController < ApplicationController
  before_action :require_login

  def home
  end

  def help
  end

  def about
  end

end
