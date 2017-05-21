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
  

