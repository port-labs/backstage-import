<img align="right" width="100" height="74" src="https://user-images.githubusercontent.com/8277210/183290025-d7b24277-dfb4-4ce1-bece-7fe0ecd5efd4.svg" />

# Backstage Import

This repository contains a simple script that can be used to import data from your Backstage instance right into Port in a single click.

## Prerequisites

- Docker
- Port organization
- Backstage instance

## Usage

1. Clone this repository `git clone https://github.com/port-labs/backstage-import.git`
2. Create a `.env` file with the following values
```bash
BACKSTAGE_URL=<your backstage url i.e https://demo.backstage.io>
PORT_CLIENT_ID=<your port client id>
PORT_CLIENT_SECRET=<your port secret>
```
3. Run
```bash
./import.sh
```

## Optional configurations

You can add the following to the `.env` file, but they are optional
```bash
MAX_CONCURRENCY=<change this to increase the number of concurrent requests default is 1>
UPSERT_BLUEPRINTS=<set to false if you want to skip blueprint upsertion>
```