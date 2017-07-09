class StatusSerializer < BaseSerializer

  def initialize(hosts)
    @hosts = hosts
  end

  def as_json
    Jbuilder.encode do |json|
      json.status :ok
      json.timestamp Time.now.in_time_zone("America/New_York")
      json.hosts @hosts do |host|
        json.hostname host.hostname
        json.health host.health
        json.replicas host.replicas.count
      end
    end
  end

end
