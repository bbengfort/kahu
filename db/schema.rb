# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20170708175021) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "machines", force: :cascade do |t|
    t.boolean "active", default: true
    t.string "hostname", limit: 255, null: false
    t.string "description", limit: 4000
    t.string "domain", limit: 255
    t.inet "ip_address"
    t.string "mac_address", limit: 20
    t.string "location", limit: 255
    t.decimal "latitude", precision: 10, scale: 6
    t.decimal "longitude", precision: 10, scale: 6
    t.datetime "last_seen"
    t.string "apikey", limit: 45
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["apikey"], name: "index_machines_on_apikey", unique: true
    t.index ["hostname"], name: "index_machines_on_hostname", unique: true
  end

  create_table "replicas", force: :cascade do |t|
    t.integer "precedence", null: false
    t.integer "port", null: false
    t.bigint "machine_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["machine_id"], name: "index_replicas_on_machine_id"
    t.index ["precedence"], name: "index_replicas_on_precedence", unique: true
  end

  create_table "users", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "email", null: false
    t.string "encrypted_password", limit: 128, null: false
    t.string "confirmation_token", limit: 128
    t.string "remember_token", limit: 128, null: false
    t.string "first_name"
    t.string "last_name"
    t.boolean "administrator", default: false
    t.string "email_confirmation_token", default: "", null: false
    t.datetime "email_confirmed_at"
    t.boolean "is_admin", default: false
    t.index ["email"], name: "index_users_on_email"
    t.index ["remember_token"], name: "index_users_on_remember_token"
  end

  add_foreign_key "replicas", "machines"
end
