#!/bin/bash

case "$1" in
  start)
    echo "Starting Firewall"
    iptables-restore < /etc/firewall.conf
    ;;
  stop)
    echo "Stopping Firewall"
    iptables-save > /etc/firewall.conf
    ;;
  *)
    echo "Usage: /etc/init.d/firewall {start|stop}"
    exit 1
    ;;
esac

exit 0
