# SwiftGate Debian 6.0 (Squeeze) Installation Instructions

## Automatic

Run the following at the command line:

`wget -qO- --no-check-certificate https://raw.github.com/ushahidi/swiftgate/master/deploy/debian/install.sh | sudo bash`

## Manual

1. Update the sources.  
apt-get update

2. Upgrade the existing packages.  
apt-get upgrade -y

3. Download Membase.  
wget -o /tmp/membase-server-community_x86_64_1.7.1.deb http://packages.couchbase.com/releases/1.7.1/membase-server-community_x86_64_1.7.1.deb

4. Install Membase.  
dpkg -i /tmp/membase-server-community_x86_64_1.7.1.deb

5. Install the missing dependencies.  
apt-get install -fy

6. Remove the Membase installer.  
rm -f /tmp/membase-server-community_x86_64_1.7.1.deb

7. Install the other necessary Debian packages.  
apt-get install -y apache2 libapache2-mod-wsgi python-pip rabbitmq-server git

8. Install the necessary Python packages.  
pip install flask python-memcached

9. Create a user for SwiftGate processes to run as.  
adduser --disabled-password --gecos "" swiftgate

10. Create a local clone of the application.  
git clone https://github.com/ushahidi/swiftgate.git /var/www/swiftgate

11. Replace the default Apache configuration with the bundled one.  
cp /var/www/swiftgate/deploy/debian/apache.conf /etc/apache2/sites-enabled/000-default

12. Tell Apache to reload its configuration.  
/etc/init.d/apache2 reload