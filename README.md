# GoQuest

[Description]

## Development

OS: Linux or WSL

**Install Development Environment**

```bash
make install
```

**Upgrade Project Dependencies**

```bash
make upgrade
```

**Execute Checks**

```bash
make lint
make test

# or
make check
```

**Startup**

```bash
cp .env.local.example .env

# Starts a database and redis instance only
make start-infra

# Starts the application
app run

# to stop the database and redis
make stop-infra
```

**Docker Compose**

If you want to run the entire development environment containerized, you can use the following command:

```bash
docker compose up
```
