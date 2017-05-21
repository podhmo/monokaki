import json


class JSONRenderer:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, record, data):
        return json.dumps(data, **self.kwargs)


DEFAULT_RENDERER = JSONRenderer(sort_keys=True, ensure_ascii=False)
