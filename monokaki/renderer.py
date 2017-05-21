import json


class JSONRenderer:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, d, record, formatter):
        return json.dumps(d, **self.kwargs)


DEFAULT_RENDERER = JSONRenderer(sort_keys=True, ensure_ascii=False)
