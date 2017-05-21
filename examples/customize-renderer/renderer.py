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
