
# Configuration Parameters
[Home](https://miniflux.app/index.html) > [Documentation](https://miniflux.app/docs/index.html)

Miniflux can use a configuration file and environment variables.

The configuration file is loaded first if specified. Environment variables take precedence over the options defined in the configuration file.

Boolean options accept the following values \(case\-insensitive\): 1/0, yes/no, true/false, on/off. For variables ending in `\_FILE`, the value is a path to a file that contains the corresponding secret value.
- [Configuration Options](https://miniflux.app/docs/configuration.html#options)
- [Configuration File](https://miniflux.app/docs/configuration.html#config-file)

## Configuration Options [¶](https://miniflux.app/docs/configuration.html#options)
[`ADMIN\_PASSWORD`](https://miniflux.app/docs/configuration.html#admin-password)

Admin user password, it's used only if `CREATE\_ADMIN` is enabled.

*Default is empty.*
[`ADMIN\_PASSWORD\_FILE`](https://miniflux.app/docs/configuration.html#admin-password-file)

Path to a secret key exposed as a file, it should contain `$ADMIN\_PASSWORD` value.

*Default is empty.*
[`ADMIN\_USERNAME`](https://miniflux.app/docs/configuration.html#admin-username)

Admin user login, it's used only if `CREATE\_ADMIN` is enabled.

*Default is empty.*
[`ADMIN\_USERNAME\_FILE`](https://miniflux.app/docs/configuration.html#admin-username-file)

Path to a secret key exposed as a file, it should contain `$ADMIN\_USERNAME` value.

*Default is empty.*
[`AUTH\_PROXY\_HEADER`](https://miniflux.app/docs/configuration.html#auth-proxy-header)

Proxy authentication HTTP header.

The option `TRUSTED\_REVERSE\_PROXY\_NETWORKS` must be configured to allow the proxy to authenticate users.

*Default is empty.*
[`AUTH\_PROXY\_USER\_CREATION`](https://miniflux.app/docs/configuration.html#auth-proxy-user-creation)

Set to 1 to create users based on proxy authentication information.

*Disabled by default.*
[`BASE\_URL`](https://miniflux.app/docs/configuration.html#base-url)

Base URL to generate HTML links and base path for cookies.

*Default is `http://localhost`.*
[`BATCH\_SIZE`](https://miniflux.app/docs/configuration.html#batch-size)

Number of feeds to send to the queue for each interval.

*Default is 100 feeds.*
[`CERT\_DOMAIN`](https://miniflux.app/docs/configuration.html#cert-domain)

Use [Let's Encrypt](https://letsencrypt.org/) to get automatically a certificate for the domain specified in `$CERT\_DOMAIN`.

*Default is empty.*
[`CERT\_FILE`](https://miniflux.app/docs/configuration.html#cert-file)

Path to SSL certificate.

*Default is empty.*
[`CLEANUP\_ARCHIVE\_BATCH\_SIZE`](https://miniflux.app/docs/configuration.html#cleanup-archive-batch-size)

Number of entries to archive for each job interval.

*Default is 10000 entries.*
[`CLEANUP\_ARCHIVE\_READ\_DAYS`](https://miniflux.app/docs/configuration.html#cleanup-archive-read-days)

Number of days after marking read entries as removed. Set to `\-1` to keep all read entries.

*Default is 60 days.*
[`CLEANUP\_ARCHIVE\_UNREAD\_DAYS`](https://miniflux.app/docs/configuration.html#cleanup-archive-unread-days)

Number of days after marking unread entries as removed. Set to `\-1` to keep all unread entries.

*Default is 180 days.*
[`CLEANUP\_FREQUENCY\_HOURS`](https://miniflux.app/docs/configuration.html#cleanup-frequency-hours)

Cleanup job frequency. Remove old sessions and archive entries.

*Default is 24 hours.*
[`CLEANUP\_REMOVE\_SESSIONS\_DAYS`](https://miniflux.app/docs/configuration.html#cleanup-remove-sessions-days)

Number of days after removing old user sessions from the database.

*Default is 30 days.*
[`CREATE\_ADMIN`](https://miniflux.app/docs/configuration.html#create-admin)

Set to 1 to create an admin user from environment variables.

*Disabled by default.*
[`DATABASE\_CONNECTION\_LIFETIME`](https://miniflux.app/docs/configuration.html#database-connection-lifetime)

Set the maximum amount of time in minutes a connection may be reused.

*Default is 5 minutes.*
[`DATABASE\_MAX\_CONNS`](https://miniflux.app/docs/configuration.html#database-max-conns)

Maximum number of database connections.

*Default is `20`.*
[`DATABASE\_MIN\_CONNS`](https://miniflux.app/docs/configuration.html#database-min-conns)

Minimum number of database connections.

*Default is `1`.*
[`DATABASE\_URL`](https://miniflux.app/docs/configuration.html#database-url)

PostgreSQL connection parameters.

*Default is "`user=postgres password=postgres dbname=miniflux2 sslmode=disable`".*
[`DATABASE\_URL\_FILE`](https://miniflux.app/docs/configuration.html#database-url-file)

Path to a secret key exposed as a file, it should contain `$DATABASE\_URL` value.

*Default is empty.*
[`DISABLE\_API`](https://miniflux.app/docs/configuration.html#disable-api)

Disable miniflux's API.

*Default is false \(The API is enabled\).*
[`DISABLE\_HSTS`](https://miniflux.app/docs/configuration.html#disable-hsts)

Disable HTTP Strict Transport Security header if `HTTPS` is set.

*Default is false \(The HSTS is enabled\).*
[`DISABLE\_HTTP\_SERVICE`](https://miniflux.app/docs/configuration.html#disable-http-service)

Set the value to 1 to disable the HTTP service.

*Default is false \(The HTTP service is enabled\).*
[`DISABLE\_LOCAL\_AUTH`](https://miniflux.app/docs/configuration.html#disable-local-auth)

Disable local authentication.

When set to true, the username/password form is hidden from the login screen, and the options to change username/password or unlink OAuth2 account are hidden from the settings page.

*Default is false.*
[`DISABLE\_SCHEDULER\_SERVICE`](https://miniflux.app/docs/configuration.html#disable-scheduler-service)

Set the value to 1 to disable the internal scheduler service.

*Default is false \(The internal scheduler service is enabled\).*
[`FETCH\_BILIBILI\_WATCH\_TIME`](https://miniflux.app/docs/configuration.html#fetch-bilibili-watch-time)

Set the value to 1 to scrape video duration from Bilibili website and use it as a reading time.

*Disabled by default.*
[`FETCH\_NEBULA\_WATCH\_TIME`](https://miniflux.app/docs/configuration.html#fetch-nebula-watch-time)

Set the value to 1 to scrape video duration from Nebula website and use it as a reading time.

*Disabled by default.*
[`FETCH\_ODYSEE\_WATCH\_TIME`](https://miniflux.app/docs/configuration.html#fetch-odysee-watch-time)

Set the value to 1 to scrape video duration from Odysee website and use it as a reading time.

*Disabled by default.*
[`FETCH\_YOUTUBE\_WATCH\_TIME`](https://miniflux.app/docs/configuration.html#fetch-youtube-watch-time)

Set the value to 1 to scrape video duration from YouTube website and use it as a reading time.

*Disabled by default.*
[`FETCHER\_ALLOW\_PRIVATE\_NETWORKS`](https://miniflux.app/docs/configuration.html#fetcher-allow-private-networks)

Set to 1 to allow outgoing fetcher requests to private or loopback networks.

*Disabled by default, private networks are refused.*
[`FORCE\_REFRESH\_INTERVAL`](https://miniflux.app/docs/configuration.html#force-refresh-interval)

The minimum interval in minutes for manual refresh.

*Default is 30 minutes.*
[`HTTP\_CLIENT\_MAX\_BODY\_SIZE`](https://miniflux.app/docs/configuration.html#http-client-max-body-size)

Maximum body size for HTTP requests in Mebibyte \(MiB\).

*Default is 15 MiB.*
[`HTTP\_CLIENT\_PROXIES`](https://miniflux.app/docs/configuration.html#http-client-proxies)

Enable proxy rotation for outgoing requests by providing a comma\-separated list of proxy URLs.

*Default is empty.*
[`HTTP\_CLIENT\_PROXY`](https://miniflux.app/docs/configuration.html#http-client-proxy)

Proxy URL to use when the "Fetch via proxy" feed option is enabled. For example: `http://127.0.0.1:8888`.

If you prefer to have a proxy for all outgoing requests, use the environment variables `HTTP\_PROXY` or `HTTPS\_PROXY`, look at the official [Golang documentation](https://golang.org/pkg/net/http/#ProxyFromEnvironment) for more details.

*Default is empty.*
[`HTTP\_CLIENT\_TIMEOUT`](https://miniflux.app/docs/configuration.html#http-client-timeout)

Time limit in seconds before the HTTP client cancels the request.

*Default is 20 seconds.*
[`HTTP\_CLIENT\_USER\_AGENT`](https://miniflux.app/docs/configuration.html#http-client-user-agent)

The default User\-Agent header to use for the HTTP client. Can be overridden in per\-feed settings. When empty, Miniflux uses a default User\-Agent that includes the Miniflux version.

*Default is empty.*
[`HTTP\_SERVER\_TIMEOUT`](https://miniflux.app/docs/configuration.html#http-server-timeout)

Read, write, and idle timeout in seconds for the HTTP server.

*Default is 300 seconds.*
[`HTTPS`](https://miniflux.app/docs/configuration.html#https)

Forces cookies to use secure flag and send HSTS header.

*Default is disabled.*
[`INTEGRATION\_ALLOW\_PRIVATE\_NETWORKS`](https://miniflux.app/docs/configuration.html#integration-allow-private-networks)

Set to 1 to allow outgoing integration requests to private or loopback networks.

*Disabled by default, private networks are refused.*
[`INVIDIOUS\_INSTANCE`](https://miniflux.app/docs/configuration.html#invidious-instance)

Set a custom invidious instance to use.

*Default is yewtu.be.*
[`KEY\_FILE`](https://miniflux.app/docs/configuration.html#key-file)

Path to SSL private key.

*Default is empty.*
[`LISTEN\_ADDR`](https://miniflux.app/docs/configuration.html#listen-addr)

Address to listen on. Use absolute path to listen on Unix socket \(`/var/run/miniflux.sock`\).

Multiple addresses can be specified, separated by commas. For example: `127.0.0.1:8080, 127.0.0.1:8081`.

*Default is `127.0.0.1:8080`.*
[`LOG\_DATE\_TIME`](https://miniflux.app/docs/configuration.html#log-date-time)

Display the date and time in log messages.

*Disabled by default.*
[`LOG\_FILE`](https://miniflux.app/docs/configuration.html#log-file)

Supported values are `stderr`, `stdout`, or a file name.

*Default is `stderr`.*
[`LOG\_FORMAT`](https://miniflux.app/docs/configuration.html#log-format)

Supported log formats are `text` or `json`.

*Default is `text`.*
[`LOG\_LEVEL`](https://miniflux.app/docs/configuration.html#log-level)

Supported values are `debug`, `info`, `warning`, or `error`.

*Default is `info`.*
[`MAINTENANCE\_MESSAGE`](https://miniflux.app/docs/configuration.html#maintenance-message)

Define a custom maintenance message.

*Default is "Miniflux is currently under maintenance".*
[`MAINTENANCE\_MODE`](https://miniflux.app/docs/configuration.html#maintenance-mode)

Set to 1 to enable maintenance mode.

*Disabled by default.*
[`MEDIA\_PROXY\_CUSTOM\_URL`](https://miniflux.app/docs/configuration.html#media-proxy-custom-url)

Sets an external server to proxy media through.

Default is empty, Miniflux does the proxying.
[`MEDIA\_PROXY\_HTTP\_CLIENT\_TIMEOUT`](https://miniflux.app/docs/configuration.html#media-proxy-http-client-timeout)

Time limit in seconds before the media proxy HTTP client cancels the request.

*Default is 120 seconds.*
[`MEDIA\_PROXY\_MODE`](https://miniflux.app/docs/configuration.html#media-proxy-mode)

Possible values: `http\-only`, `all`, or `none`.

*Default is `http\-only`.*
[`MEDIA\_PROXY\_PRIVATE\_KEY`](https://miniflux.app/docs/configuration.html#media-proxy-private-key)

Set a custom private key used to sign proxified media URLs.

By default, a secret key is randomly generated during startup.
[`MEDIA\_PROXY\_RESOURCE\_TYPES`](https://miniflux.app/docs/configuration.html#media-proxy-resource-types)

A comma\-separated list of media types to proxify. Supported values are: `image`, `audio`, `video`.

*Default is `image`.*
[`METRICS\_ALLOWED\_NETWORKS`](https://miniflux.app/docs/configuration.html#metrics-allowed-networks)

List of networks allowed to access the `/metrics` endpoint \(comma\-separated values\).

*Default is `127.0.0.1/8`.*
[`METRICS\_COLLECTOR`](https://miniflux.app/docs/configuration.html#metrics-collector)

Set to 1 to enable metrics collector. Expose a `/metrics` endpoint for Prometheus.

*Disabled by default.*
[`METRICS\_PASSWORD`](https://miniflux.app/docs/configuration.html#metrics-password)

Metrics endpoint password for basic HTTP authentication.

*Default is empty.*
[`METRICS\_PASSWORD\_FILE`](https://miniflux.app/docs/configuration.html#metrics-password-file)

Path to a file that contains the password for the metrics endpoint HTTP authentication.

*Default is empty.*
[`METRICS\_REFRESH\_INTERVAL`](https://miniflux.app/docs/configuration.html#metrics-refresh-interval)

Refresh interval in seconds to collect database metrics.

*Default is 60 seconds.*
[`METRICS\_USERNAME`](https://miniflux.app/docs/configuration.html#metrics-username)

Metrics endpoint username for basic HTTP authentication.

*Default is empty.*
[`METRICS\_USERNAME\_FILE`](https://miniflux.app/docs/configuration.html#metrics-username-file)

Path to a file that contains the username for the metrics endpoint HTTP authentication.

*Default is empty.*
[`OAUTH2\_CLIENT\_ID`](https://miniflux.app/docs/configuration.html#oauth2-client-id)

OAuth2 client ID.

*Default is empty.*
[`OAUTH2\_CLIENT\_ID\_FILE`](https://miniflux.app/docs/configuration.html#oauth2-client-id-file)

Path to a client ID exposed as a file, it should contain `$OAUTH2\_CLIENT\_ID` value.

*Default is empty.*
[`OAUTH2\_CLIENT\_SECRET`](https://miniflux.app/docs/configuration.html#oauth2-client-secret)

OAuth2 client secret.

*Default is empty.*
[`OAUTH2\_CLIENT\_SECRET\_FILE`](https://miniflux.app/docs/configuration.html#oauth2-client-secret-file)

Path to a secret key exposed as a file, it should contain `$OAUTH2\_CLIENT\_SECRET` value.

*Default is empty.*
[`OAUTH2\_OIDC\_DISCOVERY\_ENDPOINT`](https://miniflux.app/docs/configuration.html#oauth2-oidc-discovery-endpoint)

OpenID Connect discovery endpoint.

Note that the OIDC library automatically appends the `.well\-known/openid\-configuration`, this part has to be removed from the URL when setting `OAUTH2\_OIDC\_DISCOVERY\_ENDPOINT`.

*Default is empty.*
[`OAUTH2\_OIDC\_PROVIDER\_NAME`](https://miniflux.app/docs/configuration.html#oauth2-oidc-provider-name)

Name to display for the OIDC provider.

*Default is "OpenID Connect".*
[`OAUTH2\_PROVIDER`](https://miniflux.app/docs/configuration.html#oauth2-provider)

OAuth2 provider. Possible values are `google` or `oidc` for a generic OpenID Connect provider.

*Default is empty.*
[`OAUTH2\_REDIRECT\_URL`](https://miniflux.app/docs/configuration.html#oauth2-redirect-url)

OAuth2 redirect URL.

This URL must be registered with the provider and is something like `https://miniflux.example.org/oauth2/oidc/callback`.

*Default is empty.*
[`OAUTH2\_USER\_CREATION`](https://miniflux.app/docs/configuration.html#oauth2-user-creation)

Set to 1 to authorize OAuth2 user creation.

*Disabled by default.*
[`POLLING\_FREQUENCY`](https://miniflux.app/docs/configuration.html#polling-frequency)

Interval for the background job scheduler.

Determines how often a batch of feeds is selected for refresh, based on their last refresh time.

*Default is 60 minutes.*
[`POLLING\_LIMIT\_PER\_HOST`](https://miniflux.app/docs/configuration.html#polling-limit-per-host)

Limits the number of concurrent requests to the same hostname when polling feeds.

This helps prevent overwhelming a single server during batch processing by the worker pool.

*Default is 0 \(disabled\).*
[`POLLING\_PARSING\_ERROR\_LIMIT`](https://miniflux.app/docs/configuration.html#polling-parsing-error-limit)

The maximum number of parsing errors that the program will try before stopping polling a feed. Once the limit is reached, the user must refresh the feed manually. Set to 0 for unlimited.

*Default is 3.*
[`POLLING\_SCHEDULER`](https://miniflux.app/docs/configuration.html#polling-scheduler)

Determines the strategy used to schedule feed polling. Supported values are `round\_robin` and `entry\_frequency`.

\- `round\_robin`: Feeds are polled in a fixed, rotating order.

\- `entry\_frequency`: The polling interval for each feed is based on the average update frequency over the past week.

The number of feeds polled in a given period is limited by the `POLLING\_FREQUENCY` and `BATCH\_SIZE` settings. Regardless of the scheduler used, the total number of polled feeds will not exceed the maximum allowed per polling cycle.

*Default is `round\_robin`.*
[`PORT`](https://miniflux.app/docs/configuration.html#port)

Override `LISTEN\_ADDR` to `0.0.0.0:$PORT` \(Automatic configuration for PaaS\).

*Default is empty.*
[`RUN\_MIGRATIONS`](https://miniflux.app/docs/configuration.html#run-migrations)

Set to 1 to run database migrations.

*Disabled by default.*
[`SCHEDULER\_ENTRY\_FREQUENCY\_FACTOR`](https://miniflux.app/docs/configuration.html#scheduler-entry-frequency-factor)

Factor to increase refresh frequency for the entry frequency scheduler.

*Default is 1.*
[`SCHEDULER\_ENTRY\_FREQUENCY\_MAX\_INTERVAL`](https://miniflux.app/docs/configuration.html#scheduler-entry-frequency-max-interval)

Maximum interval in minutes for the entry frequency scheduler.

*Default is 1440 minutes \(24 hours\).*
[`SCHEDULER\_ENTRY\_FREQUENCY\_MIN\_INTERVAL`](https://miniflux.app/docs/configuration.html#scheduler-entry-frequency-min-interval)

Minimum interval in minutes for the entry frequency scheduler.

*Default is 5 minutes.*
[`SCHEDULER\_ROUND\_ROBIN\_MAX\_INTERVAL`](https://miniflux.app/docs/configuration.html#scheduler-round-robin-max-interval)

Maximum interval in minutes for the round robin scheduler. This option is used when the values of the `Cache\-Control` max\-age and `Expires` headers are excessively high.

*Default is 1440 minutes \(24 hours\).*
[`SCHEDULER\_ROUND\_ROBIN\_MIN\_INTERVAL`](https://miniflux.app/docs/configuration.html#scheduler-round-robin-min-interval)

Minimum interval in minutes for the round robin scheduler.

*Default is 60 minutes.*
[`TRUSTED\_REVERSE\_PROXY\_NETWORKS`](https://miniflux.app/docs/configuration.html#trusted-reverse-proxy-networks)

List of networks \(CIDR notation\) allowed to use the proxy authentication header, `X\-Forwarded\-For`, `X\-Forwarded\-Proto`, and `X\-Real\-Ip` headers.

*Default is empty.*
[`WATCHDOG`](https://miniflux.app/docs/configuration.html#watchdog)

Enable or disable Systemd watchdog.

*Enabled by default.*
[`WEBAUTHN`](https://miniflux.app/docs/configuration.html#webauthn)

Enable or disable WebAuthn/Passkey authentication.

You must provide a username on the login page if you are using non\-residential keys. However, this is not required for discoverable credentials.

*Default is disabled.*
[`WORKER\_POOL\_SIZE`](https://miniflux.app/docs/configuration.html#worker-pool-size)

Number of background workers.

*Default is 16 workers.*
[`YOUTUBE\_API\_KEY`](https://miniflux.app/docs/configuration.html#youtube-api-key)

YouTube API key for use with `FETCH\_YOUTUBE\_WATCH\_TIME`. If nonempty, the duration will be fetched from the YouTube API. Otherwise, the duration will be fetched from the YouTube website.

*Default is empty.*
[`YOUTUBE\_EMBED\_URL\_OVERRIDE`](https://miniflux.app/docs/configuration.html#youtube-embed-url-override)

YouTube URL which will be used for embeds.

*Default is `https://www.youtube\-nocookie.com/embed/`.*

## Configuration File [¶](https://miniflux.app/docs/configuration.html#config-file)

The configuration file is optional. It’s a text file that follow these rules:
- Miniflux expects each line to be in `KEY=VALUE` format.
- Lines beginning with `\#` are processed as comments and ignored.
- Blank lines are ignored.
- There is no variable interpolation.

Keys are the same as the environment variables described above.

Example:

```
LOG_LEVEL=debug
WORKER_POOL_SIZE=20
```

Environment variables override the values defined in the config file.

To specify a configuration file, use the command line argument `\-config\-file` or `\-c`.

You can also dump interpreted values with the flag `\-config\-dump` for debugging.

Systemd uses the file `/etc/miniflux.conf` to populate environment variables.
[Edit this page](https://github.com/miniflux/website/edit/main/content/docs/configuration.md)
