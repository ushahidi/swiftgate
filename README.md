# SwiftGate v2.0.0

## Synopsis

Gateway for API management, rate limiting and billing.

## Supported Operating Systems

* [Debian 6.0](http://www.debian.org/)
* [Ubuntu 11.04](http://www.ubuntu.com/)

## Dependencies

* [Apache HTTP Server](http://httpd.apache.org/)
* [Membase Server](http://www.couchbase.org/)
* [RabbitMQ](http://www.rabbitmq.com/)
* [Python 2.x](http://python.org/)
* [mod_wsgi](http://code.google.com/p/modwsgi/)
* [Flask](http://flask.pocoo.org/)
* [Pika](http://pika.github.com/)
* [python-memcached](http://www.tummy.com/Community/software/python-memcached/)

## Installation

`wget -qO- --no-check-certificate https://raw.github.com/ushahidi/swiftgate/master/scripts/install.sh | sudo bash`

## Configuration

* Membase
    * URL: `http://localhost:8091/`
* RabbitMQ
    * URL: `http://localhost:55672/mgmt/`
    * Username: `swiftgate`
    * Password: `swiftgate`

## License

* [GNU Affero General Public License](http://www.gnu.org/licenses/agpl.html)

## Support

* [SwiftRiver Mailing List](http://groups.google.com/group/swiftriver)

## See Also

* [Ushahidi](http://www.ushahidi.com/)
