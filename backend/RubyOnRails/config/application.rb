require_relative "boot"

require "rails"
# Pick the frameworks you want:
require "active_model/railtie"
require "active_record/railtie"
require "action_controller/railtie"
require "rails/test_unit/railtie"

require "dotenv/load"

Bundler.require(*Rails.groups)

Dotenv::Railtie.load

module RubyOnRails
  class Application < Rails::Application
    config.load_defaults 7.0
    config.api_only = true
  end
end
