# SwiftGate Generic Installation Instructions

## Dependencies

* [Apache HTTP Server](http://httpd.apache.org/)
* [mod_wsgi](http://code.google.com/p/modwsgi/)
* [RabbitMQ](http://www.rabbitmq.com/)
* [Python 2.x](http://python.org/)
* [python-memcached](http://www.tummy.com/Community/software/python-memcached/)
* [Flask](http://flask.pocoo.org/)
* [Pika](http://pika.github.com/)

## Apache Configuration

    <VirtualHost *:80>
     WSGIDaemonProcess swiftgate user=swiftgate group=swiftgate threads=5
     WSGIScriptAlias / /var/www/swiftgate/api/wsgi.py
    </VirtualHost>

* If your application is installed in a different directory than `/var/www/swiftgate`, remember to modify the path accordingly.
* You need a user set up for the SwiftGate process to run as. In the above, we assume both the user and group will be `swiftgate`.
