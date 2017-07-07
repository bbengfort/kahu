class CreateReplicas < ActiveRecord::Migration[5.1]
  def change
    create_table :replicas do |t|
      t.integer :precedence, null: false
      t.integer :port, null: false
      t.references :machine, null:false, foreign_key: true

      t.timestamps
    end

    add_index :replicas, :precedence, unique: true
  end
end
