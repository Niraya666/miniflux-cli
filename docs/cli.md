
# Command Line Usage
[Home](https://miniflux.app/index.html) > [Documentation](https://miniflux.app/docs/index.html)

## Show Interpreted Configuration Values [¶](https://miniflux.app/docs/cli.html#config-dump)

```
miniflux -config-dump
```

## Use a Configuration File [¶](https://miniflux.app/docs/cli.html#config-file)

```
miniflux -config-file /etc/miniflux.conf
```

or

```
miniflux -c /etc/miniflux.conf
```

## Create Admin User [¶](https://miniflux.app/docs/cli.html#create-admin)

```
miniflux -create-admin
Enter Username: root
Enter Password: ****
```

## Enable Debug Mode [¶](https://miniflux.app/docs/cli.html#debug)

```
miniflux -debug
[INFO] Debug mode enabled
[INFO] Starting Miniflux...
```

## Export Feeds [¶](https://miniflux.app/docs/cli.html#export-feeds)

```
miniflux -export-user-feeds username > feeds.opml
```

## Flush All Sessions [¶](https://miniflux.app/docs/cli.html#flush-sessions)

```
miniflux -flush-sessions
Flushing all sessions (disconnect users)
```

## Health Check [¶](https://miniflux.app/docs/cli.html#healthcheck)

Perform a health check on the specified endpoint. The value “auto” attempts to guess the health check endpoint.

```
miniflux -healthcheck https://miniflux.domain.tld/healthcheck
```

Returns 0 as the exit code if successful; otherwise, returns 1.

## Show Build Information [¶](https://miniflux.app/docs/cli.html#info)

```
miniflux -info # or -i
Version: 2.0.15
Build Date: 2019-03-16T18:26:30-0700
Go Version: go1.12
Compiler: gc
Arch: amd64
OS: darwin
```

## Run Database Migrations [¶](https://miniflux.app/docs/cli.html#migrate)

```
export DATABASE_URL=replace_me

miniflux -migrate
Current schema version: 0
Latest schema version: 12
Migrating to version: 1
Migrating to version: 2
Migrating to version: 3
Migrating to version: 4
Migrating to version: 5
Migrating to version: 6
Migrating to version: 7
Migrating to version: 8
Migrating to version: 9
Migrating to version: 10
Migrating to version: 11
Migrating to version: 12
```

## Refresh Feeds [¶](https://miniflux.app/docs/cli.html#refresh-feeds)

```
miniflux -refresh-feeds
```

## Reset All Feed Errors [¶](https://miniflux.app/docs/cli.html#reset-feed-errors)

```
miniflux -reset-feed-errors
```

## Reset the next check time for all feeds [¶](https://miniflux.app/docs/cli.html#reset-feed-next-check-at)

```
miniflux -reset-feed-next-check-at
```

## Reset User Password [¶](https://miniflux.app/docs/cli.html#reset-password)

```
miniflux -reset-password
Enter Username: myusername
Enter Password: ****
```

## Run Cleanup Tasks [¶](https://miniflux.app/docs/cli.html#run-cleanup-tasks)

Delete old sessions and archive old entries.

```
miniflux -run-cleanup-tasks
```

## Show Application Version [¶](https://miniflux.app/docs/cli.html#version)

```
miniflux -version # or -v
2.0.15
```
[Edit this page](https://github.com/miniflux/website/edit/main/content/docs/cli.md)
