class StaticPagesController < BaseController

  def home
    @machines = Machine.all
    @maphash = Gmaps4rails.build_markers(@machines) do |machine, marker|
      marker.lat machine.latitude
      marker.lng machine.longitude
      marker.infowindow machine.hostname.capitalize
    end
  end

  def help
  end

  def about
  end

end
