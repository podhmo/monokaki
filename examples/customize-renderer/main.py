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
