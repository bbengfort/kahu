# Kahu

**Replica management and monitoring service.**

## About

Kahu is a service that manages replica configurations for my research (and was also a good way to learn Ruby on Rails). Each replica has a small client that uses the Kahu API to report its status as well as receive configuration updates. The Kahu web interface is used to monitor the replicas and push configuration changes for various experiments or applications.

## Getting Started

Kahu is deployed as a free Heroku app. To get the application running on your local machine, follow these steps (which may not be complete).

### Software Dependencies

The following external software dependencies are required. Most of these can be installed with Homebrew, e.g. `brew install <name>`.

- [Ruby](https://www.ruby-lang.org/en/downloads/) version 2.3.3 or later
- [PostgreSQL](http://www.postgresql.org/) version 9.6 or later
- [Heroku Toolbelt](https://devcenter.heroku.com/articles/heroku-command-lin://devcenter.heroku.com/articles/heroku-command-line)

To install the Rails libraries and dependencies use `bundle`:

```
$ bundle install
```

This should fetch the latest gems with correct versions for the current environment.

### Setting up Postgres

I recommend using [Postgres.app](https://postgresapp.com/) to run and manage PostgreSQL. Create two databases locally:

- kahu_development
- kahu_test

I prefer to create a `rails` user to give them permissions over the database, e.g.:

```
=# CREATE USER rails WITH LOGIN;
=# CREATE DATABASE kahu_development WITH OWNER rails;
```

This tends to make things simpler for development. Finally, migrate the database schema and load the required tables:

```
$ bundle exec rake db:setup
```

The database should not be ready to go.

### Environment

Kahu uses [dotenv](https://github.com/bkeepers/dotenv) to load environment variables from the .env and .env.local files. Default and dummy values are in .env that can be overridden in .env.local if required. Do not commit any real environment variables!

### Running the app

After setting up, run the application locally:

```
$ bundle exec rails server
```

This should run the server and you can access the app at [http://localhost:3000/](http://localhost:3000/).
