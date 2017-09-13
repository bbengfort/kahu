class Latency < ApplicationRecord
  belongs_to :source, :class_name => "Machine"
  belongs_to :target, :class_name => "Machine"
end
