import json
from functools import partial


class JSONRenderer:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, d, record, formatter):
        d["logger"] = record.name
        d["time"] = formatter.formatTime(record)
        return json.dumps(d, **self.kwargs)


DEFAULT_RENDERER = JSONRenderer(sort_keys=True, ensure_ascii=False)


def create_renderer_class(
    fmt, style="%", dumps=partial(json.dumps, sort_keys=True, ensure_ascii=False)
):
    import logging
    from collections import defaultdict

    style_class, _ = logging._STYLES[style]
    style = style_class(fmt)

    class MockRecord:
        pass

    m = MockRecord()
    idmap = defaultdict(lambda: len(idmap))
    m.__dict__ = idmap
    style.format(m)
    names = [k for k, _ in sorted(idmap.items(), key=lambda p: p[1])]

    class Renderer:
        def __call__(self, d, record, formatter):
            row = {}
            formatter.format(record)
            row["logger"] = record.name
            for name in names:
                if name not in row:
                    row[name] = getattr(record, name, "")
            return dumps(row)

    return Renderer()
