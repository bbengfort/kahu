module Api
  class StatusController < ApiController

    def index
      machines = Machine.where(active: true)
      response = StatusSerializer.new(machines)
      render json: response.as_json
    end

  end
end
