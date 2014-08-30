#!/bin/bash
URL="http://192.168.0.12:8080/api/control/pi"
#URL= "http://securipi.roscorcoran.com/api/control/pi"

while true
do
	curl -XGET $URL
done
