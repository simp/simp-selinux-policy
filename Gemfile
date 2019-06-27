gem_sources = ENV.fetch('GEM_SERVERS','https://rubygems.org').split(/[, ]+/)

gem_sources.each { |gem_source| source gem_source }

group :test do
  gem 'rake'
  gem 'rspec'
  gem 'simp-rake-helpers', ENV.fetch('SIMP_RAKE_HELPERS_VERSION', ['>= 5.5', '<= 6.0.0'])

  gem 'pry'
  gem 'pry-doc'
end
