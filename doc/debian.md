# SwiftGate Debian 6.0 (Squeeze) Installation Instructions

## Automatic

Run the following at the command line:

`wget -qO- --no-check-certificate https://raw.github.com/ushahidi/swiftgate/master/deploy/debian/install.sh | sudo bash`

## Manual

1. Install the necessary Debian packages.  
`apt-get install apache2 libapache2-mod-wsgi python-pip rabbitmq-server git`

2. Install the necessary Python packages.  
`pip install flask pika`

3. Create a user for SwiftGate processes to run as.  
`adduser --disabled-password --gecos "" swiftgate`

4. Create a local clone of the application.  
`git clone https://github.com/ushahidi/swiftgate.git /var/www/swiftgate`

5. Replace the default Apache configuration with the bundled one.  
`cp /var/www/swiftgate/deploy/debian/apache.conf /etc/apache2/sites-enabled/000-default`

6. Tell Apache to reload its configuration.  
`/etc/init.d/apache2 reload`

7. Copy the example SwiftGate configuration file for customisation.  
`cp /var/www/swiftgate/api/config.example.py /var/www/swiftgate/api/config.py`
