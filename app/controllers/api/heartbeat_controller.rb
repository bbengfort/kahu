module Api
  class HeartbeatController < ApiController

    def create
      # Update the last seen timestamp on the machine
      @machine.last_seen = Time.now

      # Permit an update to the IP address
      # Our version of DDNS
      params.permit(:ip_address)
      ipaddr = params[:ip_address]

      unless ipaddr.nil? || ipaddr.empty?
        @machine.ip_address = ipaddr
      end

      # Save the update to the machine
      @machine.save

      response = {
        machine: @machine.hostname,
        ipaddr: @machine.ip_address.to_s,
        success: true
      }
      render json: response.as_json
    end

  end
end
