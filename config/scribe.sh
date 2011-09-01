#!/bin/bash

case "$1" in
  start)
    echo "Starting Scribe"
    scribed -p 1463 -c /var/www/swiftgate/config/scribe.conf &
    ;;
  stop)
    echo "Stopping Scribe"
    killall scribed
    ;;
  *)
    echo "Usage: /etc/init.d/scribe {start|stop}"
    exit 1
    ;;
esac

exit 0
