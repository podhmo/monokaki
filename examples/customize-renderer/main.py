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
