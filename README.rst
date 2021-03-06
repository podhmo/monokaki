monokaki
========================================

.. image:: https://travis-ci.org/podhmo/monokaki.svg?branch=master
    :target: https://travis-ci.org/podhmo/monokaki


contextual logging library, no patch, no logging module replacement


features
----------------------------------------

- structured logging
- contextual logging (via `logger.bind`)
- (no conflicts (stdlib's logging module))

example
----------------------------------------

main.py

.. code-block:: python

  from monokaki import basic_config, get_logger
  import logging
  
  logger = get_logger(__name__)
  
  
  def run(log):
      log.info("hello")
      log.debug("hmm..")
  
  
  def main():
      log = logger.bind(name="foo")
      run(log)
      logger.info("bye")
  
      # normal stdlib's logger
      normallogger = logging.getLogger("stdlib's")
      normallogger.info("hai")
  
  
  if __name__ == "__main__":
      import argparse
      parser = argparse.ArgumentParser()
      parser.add_argument(
          "--logging", choices=list(sorted(logging._nameToLevel.keys())), default="INFO"
      )
      args = parser.parse_args()
      basic_config(level=logging._nameToLevel[args.logging])
      main()


.. code-block:: bash

  $ python examples/readme/main.py
  {"level": "INFO", "logger": "__main__", "msg": "hello", "name": "foo", "time": "2017-05-21 16:12:01,992"}
  {"level": "INFO", "logger": "__main__", "msg": "bye", "time": "2017-05-21 16:12:01,993"}
  INFO:stdlib's:hai
  
  $ python examples/readme/main.py --logging=DEBUG
  {"level": "INFO", "logger": "__main__", "msg": "hello", "name": "foo", "time": "2017-05-21 16:12:02,101"}
  {"level": "DEBUG", "logger": "__main__", "msg": "hmm..", "name": "foo", "time": "2017-05-21 16:12:02,101"}
  {"level": "INFO", "logger": "__main__", "msg": "bye", "time": "2017-05-21 16:12:02,102"}
  INFO:stdlib's:hai
  


output customization
----------------------------------------

renderer.py

.. code-block:: python

  import json
  from collections import OrderedDict
  
  
  def ordered_json_render(data, record, formatter):
      kwargs = OrderedDict()
      # see: https://docs.python.org/3/library/logging.html#formatter-objects
      kwargs["time"] = formatter.formatTime(record)
  
      # see: https://docs.python.org/3/library/logging.html#logrecord-attributes
      kwargs["level"] = record.levelname
      kwargs["meg"] = record.msg
      kwargs["caller"] = "{}:{}".format(record.pathname, record.lineno)
      kwargs["source"] = record.name
  
      # support exc_info or stack_info
      if "stack" in data:
          kwargs["stack"] = data["stack"]
  
      # extra data
      kwargs.update(record.kwargs)
      return json.dumps(kwargs, indent=2)

main.py

.. code-block:: python

  from monokaki import get_logger, basic_config
  logger = get_logger(__name__)
  
  
  def main():
      logger.bind(name="foo").info("hello", age=20)
      logger.bind(name="foo").info("bye", age=21)
      try:
          1 / 0
      except:
          logger.info("1/0", exc_info=True)
  
  
  if __name__ == "__main__":
      import logging
      from renderer import ordered_json_render
      basic_config(level=logging.INFO, renderer=ordered_json_render)
      main()


.. code-block:: bash

  $ python examples/customize-renderer/main.py
  {
    "time": "2017-05-21 16:12:02,303",
    "level": "INFO",
    "meg": "hello",
    "caller": "examples/customize-renderer/main.py:6",
    "source": "__main__",
    "age": 20,
    "name": "foo"
  }
  {
    "time": "2017-05-21 16:12:02,303",
    "level": "INFO",
    "meg": "bye",
    "caller": "examples/customize-renderer/main.py:7",
    "source": "__main__",
    "age": 21,
    "name": "foo"
  }
  {
    "time": "2017-05-21 16:12:02,304",
    "level": "INFO",
    "meg": "1/0",
    "caller": "examples/customize-renderer/main.py:11",
    "source": "__main__",
    "stack": "Traceback (most recent call last):\n  File \"examples/customize-renderer/main.py\", line 9, in main\n    1 / 0\nZeroDivisionError: division by zero"
  }
  

