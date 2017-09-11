module Api
  class HostsController < ApiController

    def index
      hosts = Machine.where({active: true})
      response = HostsSerializer.new(hosts)
      render json: response.as_json
    end

  end
end
