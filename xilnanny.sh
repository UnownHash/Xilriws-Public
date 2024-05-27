#!/bin/bash

# xilnanny.sh
# monitors 'xilriws' container logs for successful auths
# if no successful auth detected in lookback window - force container recreation
# option(new): randomize proxies.txt before recreating
# option(new): specify log file besides cron log
## caution ## kiss. tune and monitor early use. misconfiguration can lead to runaway restarts, hammering ips...
# not designed for multireplicant deployments

# usage:
# 1. DOCKER_COMMAND - your docker binary path (`which docker`)
# 2. SUCCESS_CHECK_PERIOD - timeframe in seconds for checking successful auths
# 3. LOG_PATH (optional) - custom log file location
# 4. PROXY_FILE (optional) - xilriws "proxies.txt" path for randomization on xilriws recreate
# 5. DOCKER_COMPOSE_FILE with the path to your docker-compose.yml
# 6. Add this script to your crontab to run at the desired interval (e.g., every 5 minutes):
#    `*/5 * * * * /path/to/xilnanny.sh`

# configuration
SUCCESS_CHECK_PERIOD=30  # lookback time in seconds to check for success
DOCKER_COMPOSE_FILE="/path/to/your/docker-compose.yml"
DOCKER_COMMAND="/usr/bin/docker"
PROXY_FILE="/path/to/your/proxies.txt"  # set "" (empty string) to disable
LOG_PATH="/path/to/your/logfile.txt"  # set to "" (empty string) for cron log only

# message logger function
log_message() {
    message="$1"
    if [[ -n "$LOG_PATH" ]]; then
        # ensure the log file exists
        [[ ! -f "$LOG_PATH" ]] && touch "$LOG_PATH"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - $message" | tee -a $LOG_PATH
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - $message"
    fi
}

# log initialization
log_message "checking docker log for good auth in the last $SUCCESS_CHECK_PERIOD secs"

# count occurrences of "200 ok: successful auth" in the specified time frame (case-insensitive)
AUTH_SUCCESS_COUNT=$($DOCKER_COMMAND compose -f $DOCKER_COMPOSE_FILE logs --since ${SUCCESS_CHECK_PERIOD}s xilriws | grep -ci "200 ok: successful auth")

# check if the last message is exactly "cookie storage at 2/2" (case-insensitive)
LAST_LOG_MESSAGE=$($DOCKER_COMMAND logs xilriws | tail -1 | grep -ci "cookie storage at 2/2")

if [[ $LAST_LOG_MESSAGE -gt 0 ]]; then
    log_message "last log message indicates full cookie storage. no need for recreation."
elif [[ $AUTH_SUCCESS_COUNT -gt 0 ]]; then
    log_message "successful auth detected $AUTH_SUCCESS_COUNT times. no need for recreation."
else
    log_message "conditions for recreation met. proceeding with '--force-recreate' of xilriws."
    # randomize the proxy list before recreating the container, only if PROXY_FILE is not an empty string
    if [[ -n "$PROXY_FILE" && -f "$PROXY_FILE" ]]; then
        shuf "$PROXY_FILE" > "$PROXY_FILE.tmp" && mv "$PROXY_FILE.tmp" "$PROXY_FILE"
        log_message "proxy list randomized"
    elif [[ -n "$PROXY_FILE" ]]; then
        log_message "error: proxy file does not exist"
    fi
    # force recreate xilriws using docker compose
    $DOCKER_COMMAND compose -f $DOCKER_COMPOSE_FILE up -d --force-recreate xilriws
    log_message "xilriws has been recreated"
fi