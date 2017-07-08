class User < ApplicationRecord
  include Clearance::User
  include Pacecar

  def full_name_or_email
    if first_name.blank? || last_name.blank?
      email
    else
      "#{first_name} #{last_name}".chomp
    end
  end

  def admin?
    self.is_admin
  end

  def confirmed?
    self.email_confirmed_at.present?
  end

  def confirm_email
    self.email_confirmed_at = Time.current
    save
  end

end
