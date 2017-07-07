class ReplicasController < BaseController

  def create
    @machine = Machine.find(params[:machine_id])
    @replica = @machine.replicas.create(replica_params)
    redirect_to machine_path(@machine)
  end

  def destroy
    @machine = Machine.find(params[:machine_id])
    @replica = @machine.replicas.find(params[:id])
    @replica.destroy
    
    redirect_to machine_path(@machine)
  end

  private

  def replica_params
    params.require(:replica).permit(:precedence, :port)
  end

end
