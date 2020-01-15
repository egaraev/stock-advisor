#!/bin/bash

SERVICE0='neural_prediction.py'

if ps ax | grep -v grep | grep $SERVICE0 > /dev/null
then
    echo "$SERVICE0 service running "
else
    echo there is no such "$SERVICE0 service, starting"
    cd /root/PycharmProjects/stock-advisor
    /usr/bin/python3.6 neural_prediction.py &
fi
