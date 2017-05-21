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
