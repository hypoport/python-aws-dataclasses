import json

import pkg_resources


def get_event_dict(file):
    return json.loads(pkg_resources.resource_string(f"{__package__}.resources", file))
