module Api
  class LatencyController < ApiController

    def index
      # Return the source and target information to conduct latency measures.
      targets = Machine.where({active: true}).where.not({id: @machine.id})
      response = TargetsSerializer.new(@machine, targets)
      render json: response.as_json
    end

    def create
      @latency = find_latency
      @latency.update(latency_params)

      response = {
        source: @latency.source.hostname,
        target: @latency.target.hostname,
        success: true
      }
      render json: response.as_json
    end

    private

    def find_latency
      # Find or create the latency between the machine with the API key and
      # the hostname specified in the parameters.
      target = Machine.find_by! hostname: params.require(:target)
      Latency.find_or_create_by!(source: @machine, target: target)
    end

    def latency_params
      params.permit(
        :messages, :timeouts, :total, :mean, :stddev,
        :variance, :fastest, :slowest, :range
      )
    end

  end
end
