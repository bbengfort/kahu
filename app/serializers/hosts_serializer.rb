class HostsSerializer < BaseSerializer

  def initialize(hosts)
    @hosts = hosts
  end

  def as_json
    Jbuilder.encode do |json|

      @hosts.each do |h|
        json.set! h.domain do
          json.instance h.hostname
          json.state h.health
          json.type :hardware
          json.public do
            json.dns h.domain
            json.addr h.ip_address.to_s
          end
          json.private do
            json.dns h.domain
            json.addr h.ip_address.to_s
          end
          json.tags do
            json.Name h.hostname
            json.Description h.description
          end
          json.procs h.procs
        end
      end
    end
  end

end
