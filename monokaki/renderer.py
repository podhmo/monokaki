from functools import partial

json_renderer = partial(json.dumps, sort_keys=True, ensure_ascii=False)

DEFAULT_RENDERER = json_renderer
