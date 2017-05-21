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
