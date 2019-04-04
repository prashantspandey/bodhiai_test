#!/bin/bash
DJANGODIR=/home/ubuntu/bodhiai
cd $DJANGODIR
source /home/ubuntu/bodhiai/env/bin/activate
celery -A bodhiai worker -l info -n worker1
