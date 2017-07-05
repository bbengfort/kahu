class ApiController < BaseController

  def show
    serializer = response_object_serializer_class.new(response_object)
    render json: serializer.as_json
  end

  private

  def response_object
      fail ABSTRACT_CLASS_EXCEPTION_MESSAGE
  end

  def response_object_serializer_class
    fail ABSTRACT_CLASS_EXCEPTION_MESSAGE
  end
end
