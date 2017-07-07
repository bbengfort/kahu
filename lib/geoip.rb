# frozen_string_literal: true
require 'httparty'

# Lightweight implementation of the geoip client
class GeoIP
    include HTTParty
    base_uri "https://geoip.maxmind.com"
    format :json

    def initialize(username, password)
        @auth = {
          username: username,
          password: password
        }
    end

    def location(ipaddr, options={})
        options.merge!({basic_auth: @auth})
        response = self.class.get("/geoip/v2.1/city/#{ipaddr}", options)
        response.parsed_response['location']
    end

    attr_reader :auth

end
