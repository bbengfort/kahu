require 'geoip'

class Machine < ApplicationRecord

  has_many :replicas, dependent: :destroy

  validates :hostname,
    presence: true,
    uniqueness: { case_sensitive: false },
    length: {maximum:255}

  validates :ip_address, ipaddr: true
  validates :mac_address, macaddr: true

  before_create :generate_api_key
  before_save :lookup_geoip_location


  def addressed_by
    domain.nil? ? ip_address : domain
  end

  private

  def generate_api_key
    salt = SecureRandom.base64
    time = Time.new
    key = Digest::SHA256.base64digest("#{id}#{hostname}#{time}#{salt}")
    self.apikey = key.tr('+/=', 'XpR')
  end

  def lookup_geoip_location
    if self.ip_address && self.ip_address_changed?
      geoip = GeoIP.new(
        Rails.application.secrets.geoip2_api_user,
        Rails.application.secrets.geoip2_api_key
      )

      loc = geoip.location(ip_address.to_s)
      self.latitude = loc["latitude"]
      self.longitude = loc["longitude"]
    end
  end

end
