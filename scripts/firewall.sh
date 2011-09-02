#!/bin/bash

# SwiftGate Firewall Startup Script
# =================================
#
# This file is part of SwiftGate.
#
# SwiftGate is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SwiftGate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SwiftGate.  If not, see <http://www.gnu.org/licenses/>.

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
