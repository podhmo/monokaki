nejimaki
========================================

.. image:: https://travis-ci.org/podhmo/nejimaki.svg?branch=master
    :target: https://travis-ci.org/podhmo/nejimaki


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
  
  logger = get_logger(__name__)
  
  
  def main():
      log = logger.bind(name="foo")
      log.info("hello")
      log.debug("hmm..")
      log.info("bye")
  
  
  if __name__ == "__main__":
      import logging
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
  {"level": "INFO", "msg": "hello", "name": "foo"}
  {"level": "INFO", "msg": "bye", "name": "foo"}
  
  $ python examples/readme/main.py --logging=DEBUG
  {"level": "INFO", "msg": "hello", "name": "foo"}
  {"level": "DEBUG", "msg": "hmm..", "name": "foo"}
  {"level": "INFO", "msg": "bye", "name": "foo"}
  


output customization
----------------------------------------

renderer.py

.. code-block:: python

  import json
  from collections import OrderedDict
  
  
  def ordered_json_render(data, record, formatter):
      kwargs = OrderedDict()
      kwargs["time"] = formatter.formatTime(record)
      kwargs["level"] = record.levelname
      kwargs["meg"] = record.msg
      kwargs["caller"] = "{}:{}".format(record.pathname, record.lineno)
      kwargs["source"] = record.name
      if "stack" in data:
          kwargs["stack"] = data["stack"]
      kwargs.update(record.kwargs)
      return json.dumps(kwargs, indent=2)

main.py

.. code-block:: python

  from monokaki import get_logger, basic_config
  logger = get_logger(__name__)
  
  
  def main():
      logger.bind(name="foo").info("hello", age=20)
      logger.bind(name="foo").info("bye", age=21)
  
  
  if __name__ == "__main__":
      import logging
      from renderer import ordered_json_render
      basic_config(level=logging.INFO, renderer=ordered_json_render)
      main()


.. code-block:: bash

  $ python examples/customize-renderer/main.py
  {
    "time": "2017-05-21 15:48:49,121",
    "level": "INFO",
    "meg": "hello",
    "caller": "examples/customize-renderer/main.py:6",
    "source": "__main__",
    "age": 20,
    "name": "foo"
  }
  {
    "time": "2017-05-21 15:48:49,121",
    "level": "INFO",
    "meg": "bye",
    "caller": "examples/customize-renderer/main.py:7",
    "source": "__main__",
    "age": 21,
    "name": "foo"
  }
  

