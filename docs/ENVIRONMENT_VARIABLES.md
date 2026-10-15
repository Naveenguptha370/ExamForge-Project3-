# ExamForge — Environment Configuration Guide

This document lists the environment variables required to run ExamForge locally
and in production. Do NOT commit real secret values. Copy values into your own
local deployment configuration that is ignored by version control.

## How to configure

1. Create your local deployment configuration from your platform's secret manager.
2. Fill each variable listed below with deployment-specific values.
3. Never paste production secrets into chat, tickets, or repositories.

## Required variables

| Variable | Purpose | Example shape |
|---|---|---|
| Django secret key | Signs sessions and tokens | long random string, unique per environment |
| Debug flag | Enables verbose error pages locally only | true on local, false in production |
| Allowed hosts | Hostnames the app will serve | comma-separated hostnames |
| Database engine | Django database backend identifier | postgres backend path |
| Database name | Database schema name | examforge_db |
| Database user | Database login role | service account name |
| Database password | Database credential | stored only in secret manager |
| Database host | Database hostname | localhost for local dev |
| Database port | Database port | 5432 |
| CORS origins | Frontend origins allowed to call the API | local dev URLs |
| JWT lifetimes | Access and refresh token lifetimes | 60 minutes / 7 days |
| Redis URLs | Cache and task queue endpoints | local redis URLs |
| Upload limits | Max upload size and media paths | 10 MB, media and static dirs |
| Log settings | Log level and file location | INFO level |
| Registration flags | Late registration and default status | false / registered |

Refer to `docker-compose.yml` and `backend/config/settings.py` for how each
variable is consumed. All values shown here are placeholders.

