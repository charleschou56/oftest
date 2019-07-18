#! /bin/bash

HOST=${MARS_IP}
INTERFACE=${OFTEST_INTERFACE}
DEBUG=info

# check dependencies
package=`apt list --installed 2>/dev/null | grep scapy | awk 'BEGIN {FS="/"} {print $1}'`
if [[ ${package} == *'scapy'* ]]; then
  echo "scapy is installed"
else
  echo "scapy not found"
  echo "install scapy"
  sudo apt-get install -y scapy
fi
# install python dependencies
pip2 install --user -r requirements.txt

echo "Start testing `date +%Y/%m/%d-%H:%M:%S`"

# run test in mars/
sudo ./oft --host=${HOST} -i 1@${INTERFACE} --of-version=1.3 --mars=MARS --test-dir=mars --disable-ipv6 --debug=${DEBUG} $@

echo "End testing `date +%Y/%m/%d-%H:%M:%S`"