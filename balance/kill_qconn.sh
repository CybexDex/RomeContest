#!/bin/bash
kill `lsof -i:$1 | grep -w q| tail -1| awk '{print $2}'`

