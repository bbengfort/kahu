class CreateMachines < ActiveRecord::Migration[5.1]
  def change
    create_table :machines do |t|
      t.boolean :active, default: true
      t.string :hostname, limit: 255, null:false
      t.string :description, limit: 4000
      t.string :domain, limit: 255
      t.inet :ip_address
      t.string :mac_address, limit: 20
      t.string :location, limit: 255
      t.decimal :latitude, precision: 10, scale: 6
      t.decimal :longitude, precision: 10, scale: 6
      t.timestamp :last_seen
      t.string :apikey, limit: 45
      t.timestamps
    end

    add_index :machines, :hostname, unique: true
    add_index :machines, :apikey, unique: true
  end
end
