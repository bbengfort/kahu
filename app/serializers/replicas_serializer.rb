class ReplicasSerializer < BaseSerializer

  def initialize(replicas)
    @replicas = replicas
  end

  def as_json
    Jbuilder.encode do |json|
      json.info do
        json.num_replicas @replicas.size
        json.updated Time.now.in_time_zone("UTC")
      end

      json.replicas @replicas do |r|
        json.pid r.precedence
        json.name r.name
        json.address r.address
        json.host r.machine.domain.present? ? r.machine.domain : r.machine.hostname
        json.ipaddr r.machine.ip_address.to_s
        json.port r.port
      end
    end
  end

end
