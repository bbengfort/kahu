class IpaddrValidator < ActiveModel::EachValidator
  def validate_each(record, attribute, value)
    # TODO: Rails is converting to a nil IPAddr object so this doesn't work.
    # Converting to a string here just to show how it would work if possible. 
    value = value.to_s

    # Allow null values
    return true if value.empty?

    # Ensure a valid IP address is given
    unless IPAddress.valid? value
      record.errors[attribute] << (options[:message] || "is not an ip address")
      return false
    end
  end
end
