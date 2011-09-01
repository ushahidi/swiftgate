apt-get install libboost-dev libevent-dev python-dev automake pkg-config libtool flex bison ant openjdk-6-jdk bjam libboost-all-dev build-essential psmisc

git clone git://git.apache.org/thrift.git /tmp/thrift
cd /tmp/thrift

./bootstrap.sh
./configure
make
make install

cd /tmp/thrift/lib/py
python setup.py install

cd /tmp/thrift/contrib/fb303
./bootstrap.sh
./configure
make
make install

rm -rf /tmp/thrift

git clone http://github.com/facebook/scribe.git /tmp/scribe
cd /tmp/scribe

./bootstrap.sh
make
make install
cd /tmp/scribe/lib/py
python setup.py install

rm -rf /tmp/scribe

ldconfig