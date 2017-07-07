class Machine < ApplicationRecord

  has_many :replicas, dependent: :destroy

  validates :hostname,
    presence: true,
    uniqueness: { case_sensitive: false },
    length: {maximum:255}

  validates :ip_address, ipaddr: true
  validates :mac_address, macaddr: true

  before_create do |m|
    m.apikey = m.generate_api_key
  end

  def addressed_by
    domain.nil? ? ip_address : domain
  end

  protected

  def generate_api_key
    salt = SecureRandom.base64
    time = Time.new
    key = Digest::SHA256.base64digest("#{id}#{hostname}#{time}#{salt}")
    key.tr('+/=', 'XpR')
  end

end
