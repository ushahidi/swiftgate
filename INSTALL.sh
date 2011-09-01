#!/bin/bash
#
# SwiftGate Deployment Script
# ===========================
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

# Remove the default Apache configuration.
rm /etc/apache2/sites-enabled/000-default

# Copy the SwiftGate Apache configuration.
cp /var/www/swiftgate/config/swiftgate.conf /etc/apache2/sites-enabled/

# Tell Apache to reload its configuration.
/etc/init.d/apache2 reload

# Install RabbitMQ management plugins.
wget -O /tmp/mochiweb-1.3-rmq2.5.1-git9a53dbd.ez http://www.rabbitmq.com/releases/plugins/v2.5.1/mochiweb-1.3-rmq2.5.1-git9a53dbd.ez
mv /tmp/mochiweb-1.3-rmq2.5.1-git9a53dbd.ez /usr/lib/rabbitmq/lib/rabbitmq_server-*/plugins/
wget -O /tmp/webmachine-1.7.0-rmq2.5.1-hg0c4b60a.ez http://www.rabbitmq.com/releases/plugins/v2.5.1/webmachine-1.7.0-rmq2.5.1-hg0c4b60a.ez
mv /tmp/webmachine-1.7.0-rmq2.5.1-hg0c4b60a.ez /usr/lib/rabbitmq/lib/rabbitmq_server-*/plugins/
wget -O /tmp/rabbitmq_mochiweb-2.5.1.ez http://www.rabbitmq.com/releases/plugins/v2.5.1/rabbitmq_mochiweb-2.5.1.ez
mv /tmp/rabbitmq_mochiweb-2.5.1.ez /usr/lib/rabbitmq/lib/rabbitmq_server-*/plugins/
wget -O /tmp/amqp_client-2.5.1.ez http://www.rabbitmq.com/releases/plugins/v2.5.1/amqp_client-2.5.1.ez
mv /tmp/amqp_client-2.5.1.ez /usr/lib/rabbitmq/lib/rabbitmq_server-*/plugins/
wget -O /tmp/rabbitmq_management_agent-2.5.1.ez http://www.rabbitmq.com/releases/plugins/v2.5.1/rabbitmq_management_agent-2.5.1.ez
mv /tmp/rabbitmq_management_agent-2.5.1.ez /usr/lib/rabbitmq/lib/rabbitmq_server-*/plugins/
wget -O /tmp/rabbitmq_management-2.5.1.ez http://www.rabbitmq.com/releases/plugins/v2.5.1/rabbitmq_management-2.5.1.ez
mv /tmp/rabbitmq_management-2.5.1.ez /usr/lib/rabbitmq/lib/rabbitmq_server-*/plugins/

# Create RabbitMQ administrative user.
rabbitmqctl add_user swiftgate swiftgate
rabbitmqctl set_user_tags swiftgate administrator

# Reload RabbitMQ.
/etc/init.d/rabbitmq-server reload

# Download Membase.
wget -O /tmp/membase-server-community_x86_64_1.7.1.deb http://packages.couchbase.com/releases/1.7.1/membase-server-community_x86_64_1.7.1.deb

# Install Membase.
dpkg -i /tmp/membase-server-community_x86_64_1.7.1.deb

# Remove the Membase installer.
rm -f /tmp/membase-server-community_x86_64_1.7.1.deb
