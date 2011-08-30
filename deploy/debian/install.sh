#!/bin/bash
#
# SwiftGate Debian Deployment Script
# ==================================
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

# Add the RabbitMQ public key to the trusted key list.
wget -qO- http://www.rabbitmq.com/rabbitmq-signing-key-public.asc | apt-key add -
	 	
# Add the RabbitMQ repository to the sources.
echo deb http://www.rabbitmq.com/debian/ testing main >> /etc/apt/sources.list

# Update the sources.
apt-get update

# Upgrade the existing packages.
apt-get upgrade -y

# Install the other necessary Debian packages.
apt-get install -y apache2 libapache2-mod-wsgi python-pip rabbitmq-server git

# Install the necessary Python packages.
pip install flask python-memcached pika

# Create a user for SwiftGate processes to run as.
adduser --disabled-password --gecos "" swiftgate

# Create a local clone of the application.
git clone https://github.com/ushahidi/swiftgate.git /var/www/swiftgate

# Replace the default Apache configuration with the bundled one.
cp /var/www/swiftgate/deploy/debian/apache.conf /etc/apache2/sites-enabled/000-default

# Tell Apache to reload its configuration.
/etc/init.d/apache2 reload

# Download Membase.
wget -O /tmp/membase-server-community_x86_64_1.7.1.deb http://packages.couchbase.com/releases/1.7.1/membase-server-community_x86_64_1.7.1.deb

# Install Membase.
dpkg -i /tmp/membase-server-community_x86_64_1.7.1.deb

# Remove the Membase installer.
rm -f /tmp/membase-server-community_x86_64_1.7.1.deb

# Install the missing dependencies.
apt-get install -fy
