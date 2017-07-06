class MachinesController < BaseController

  def index
    active_filter = params[:active] || true
    if active_filter == "both"
      @descriptor = "Registered"
      @machines = Machine.all
    else
      active_filter = ActiveRecord::Type::Boolean.new.deserialize(active_filter)
      @descriptor = active_filter ? "Available" : "Inactive"
      @machines = Machine.where(active: active_filter)
    end

    @machines.order(:location)
  end

  def show
    @machine = Machine.find(params[:id])
  end

  def new
    @machine = Machine.new
  end

  def edit
    @machine = Machine.find(params[:id])
  end

  def create
    @machine = Machine.new(machine_params)
    if @machine.save
      redirect_to @machine
    else
      render 'new'
    end
  end

  def update
    @machine = Machine.find(params[:id])

    if @machine.update(machine_params)
      redirect_to @machine
    else
      render 'edit'
    end
  end

  def destroy
    @machine = Machine.find(params[:id])
    @machine.destroy
    redirect_to machines_path
  end

  private

  def machine_params
    params.require(:machine).permit(:hostname, :location, :description, :ip_address, :mac_address, :domain, :active)
  end
end
