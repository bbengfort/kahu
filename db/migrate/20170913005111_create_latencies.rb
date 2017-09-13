class CreateLatencies < ActiveRecord::Migration[5.1]
  def change
    create_table :latencies do |t|
      t.references :source, null: false
      t.references :target, null: false
      t.integer :messages, default: 0
      t.integer :timeouts, default: 0
      t.float :total, default: 0.0
      t.float :mean, default: 0.0
      t.float :stddev, default: 0.0
      t.float :variance, default: 0.0
      t.float :fastest, default: 0.0
      t.float :slowest, default: 0.0
      t.float :range, default: 0.0

      t.timestamps
    end

    add_foreign_key :latencies, :machines, column: :source_id, primary_key: :id
    add_foreign_key :latencies, :machines, column: :target_id, primary_key: :id
  end
end
