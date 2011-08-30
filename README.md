# SwiftGate v2.0.0

## Synopsis

Gateway for API management, rate limiting and billing.

## Dependencies

* [Apache HTTP Server](http://httpd.apache.org/)
* [Membase Server](http://www.couchbase.org/)
* [RabbitMQ](http://www.rabbitmq.com/)
* [Python 2.x](http://python.org/)
* [mod_wsgi](http://code.google.com/p/modwsgi/)
* [Flask](http://flask.pocoo.org/)
* [Pika](http://pika.github.com/)
* [python-memcached](http://www.tummy.com/Community/software/python-memcached/)

## Apache Configuration

    <VirtualHost *:80>
     WSGIDaemonProcess swiftgate user=swiftgate group=swiftgate threads=5
     WSGIScriptAlias / /var/www/swiftgate/api/wsgi.py
    </VirtualHost>

* If your application is installed in a different directory than `/var/www/swiftgate`, remember to modify the path accordingly.
* You need a user set up for the SwiftGate process to run as. In the above, we assume both the user and group will be `swiftgate`.

## Licenses

* All bundled source code is released under the [GNU Affero General Public License](http://www.gnu.org/licenses/agpl.html).
* All bundled documentation is released under the [GNU Free Documentation License](http://www.gnu.org/licenses/fdl.html).

## Support

* [SwiftRiver Mailing List](http://groups.google.com/group/swiftriver)
* [#ushahidi on Freenode](http://irc.lc/freenode/ushahidi)

## See Also

* [Ushahidi](http://ushahidi.com/)
