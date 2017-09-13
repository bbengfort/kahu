class TargetsSerializer < BaseSerializer

  def initialize(source, hosts)
    @source = source
    @hosts = hosts
  end

  def as_json
    Jbuilder.encode do |json|
      json.source @source.hostname
      json.targets @hosts do |h|
        json.hostname h.hostname
        json.state h.health
        json.addr h.ip_address.to_s
        json.dns h.domain
      end
    end
  end

end
