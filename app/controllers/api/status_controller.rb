module Api
    class StatusController < ApiController

        def index
            response = StatusSerializer.new
            render json: response.as_json
        end

    end
end
