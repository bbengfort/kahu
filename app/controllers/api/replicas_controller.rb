module Api
  class ReplicasController < ApiController

    def index
      replicas = Replica.joins(:machine).where(machines: {active: true})
      response = ReplicasSerializer.new(replicas)
      render json: response.as_json
    end

  end
end
