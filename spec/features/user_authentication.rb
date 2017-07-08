require "rails_helper"

RSpec.feature "Widget management", :type => :feature do

  scenario "Visitor signs up, tries to sign in, confirms email and signs out" do
    visit root_path
    expect(current_path).to eq(sign_in_path)

    click_link "Need an Account?"

    fill_in "Email", with: "clarence@example.com"
    fill_in "Password", with: "password"
    click_button "Sign up"

    expect(current_path).to eq(sign_in_path)

    fill_in "Email", with: "clarence@example.com"
    fill_in "Password", with: "password"
    click_button "Sign in"

    expect(page).to have_content "Access not yet confirmed by administrator."

    open_email "info@example.com"
    click_first_link_in_email

    expect(current_path).to eq(sign_in_path)

    fill_in "Email", with: "clarence@example.com"
    fill_in "Password", with: "password"
    click_button "Sign in"

    click_link "Log Out"

    expect(current_path).to eq(sign_in_path)

  end
end
