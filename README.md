# prepare

1. install all the dependecies according to official version: https://github.com/oxarbitrage/bitshares-explorer-api, install kdbq:
```
cd libs/kdbq
python setup.py `pwd`

```

2. cybex explorer remove postgres db part ant related apis, so when you install the deps, you can ignore that part.

3. remeber set your URL/address in config.py
# run

run 
```
# cd <to your path>
# ./start.sh > log.log 2>&1 &
```
check with logs or use ps -ef| grep flask to check your flask service.


start.sh use 8081 as default, you can change it.

# check restful api

```
http://<address>:<port>/apidocs
```

