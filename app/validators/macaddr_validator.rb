class MacaddrValidator < ActiveModel::EachValidator
  def validate_each(record, attribute, value)
    # Allow null values
    return true if value.nil? || value.empty?

    # Perform regex comparison
    unless macaddr?(value)
      record.errors[attribute] << (options[:message] || "is not an mac address")
      return false
    end
  end

  def macaddr?(value)
    value =~ /^([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}$/i
  end

end
