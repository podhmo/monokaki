```console
$ python main.py
{"level": "INFO", "msg": "hello", "name": "foo"}
{"level": "INFO", "msg": "bye", "name": "foo"}

$ python main.py --logging=DEBUG
{"level": "INFO", "msg": "hello", "name": "foo"}
{"level": "DEBUG", "msg": "hmm..", "name": "foo"}
{"level": "INFO", "msg": "bye", "name": "foo"}
```
