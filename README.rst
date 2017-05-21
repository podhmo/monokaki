nejimaki
========================================

.. image:: https://travis-ci.org/podhmo/nejimaki.svg?branch=master
    :target: https://travis-ci.org/podhmo/nejimaki


contextual logging library, no patch, no logging module replacement


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

main.py

.. code-block:: python

  import json
  from collections import OrderedDict
  from monokaki import get_logger, basic_config
  
  logger = get_logger(__name__)
  
  
  def ordered_json_render(data, record, formatter):
      kwargs = OrderedDict()
      kwargs["time"] = formatter.formatTime(record)
      kwargs["level"] = record.levelname
      kwargs["meg"] = record.msg
      kwargs["caller"] = "{}:{}".format(record.pathname, record.lineno)
      kwargs["source"] = record.name
      if "stack" in data:
          kwargs["stack"] = data["stack"]
      return json.dumps(kwargs, indent=2)
  
  
  def main():
      logger.bind(name="foo").info("hello", age=20)
      logger.bind(name="foo").info("bye", age=21)
  
  
  if __name__ == "__main__":
      import logging
      basic_config(level=logging.INFO, renderer=ordered_json_render)
      main()


.. code-block:: bash

  $ python examples/customize-renderer/main.py
  {
    "time": "2017-05-21 15:42:17,420",
    "level": "INFO",
    "meg": "hello",
    "caller": "examples/customize-renderer/main.py:21",
    "source": "__main__"
  }
  {
    "time": "2017-05-21 15:42:17,420",
    "level": "INFO",
    "meg": "bye",
    "caller": "examples/customize-renderer/main.py:22",
    "source": "__main__"
  }
  

