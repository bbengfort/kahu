class StatusSerializer < BaseSerializer

    def as_json
        Jbuilder.encode do |json|
            json.status :ok
            json.timestamp Time.now.in_time_zone("America/New_York")
        end
    end

end
