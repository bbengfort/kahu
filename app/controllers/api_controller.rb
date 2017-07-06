class ApiController < ApplicationController

  before_action :require_api_authorization

  def show
    serializer = response_object_serializer_class.new(response_object)
    render json: serializer.as_json
  end

  private

  def require_api_authorization
    key = request.headers['X-Api-Key']
    @machine = Machine.where(apikey: key).first if key
    unless @machine
      require_login
    end
  end

  def response_object
      fail ABSTRACT_CLASS_EXCEPTION_MESSAGE
  end

  def response_object_serializer_class
    fail ABSTRACT_CLASS_EXCEPTION_MESSAGE
  end
end
