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
