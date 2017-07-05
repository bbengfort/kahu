class User < ApplicationRecord
  include Clearance::User
  include Pacecar

  def full_name_or_email
    if first_name.blank? || last_name.blank?
      email
    else
      "#{first_name} #{last_name}"
    end
  end
end
