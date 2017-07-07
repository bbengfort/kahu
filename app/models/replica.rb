class Replica < ApplicationRecord
  belongs_to :machine

  validates :precedence, presence: true, uniqueness: true
  validates :port,
    presence: true,
    numericality: { greater_than: 1024, less_than: 65537 }

  def name
    if machine.replicas.count > 1
      "#{machine.hostname}#{precedence}"
    else
      machine.hostname
    end
  end

  def address
    "#{machine.addressed_by}:#{port}"
  end

end
