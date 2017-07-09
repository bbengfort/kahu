class ApiController < ApplicationController

  before_action :require_api_authorization
  skip_before_action :verify_authenticity_token

  private

  def require_api_authorization
    key = request.headers['X-Api-Key']
    @machine = Machine.where(apikey: key).first if key
    unless @machine
      require_login
    end
  end

end
