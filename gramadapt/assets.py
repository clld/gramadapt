from pathlib import Path

from clld.web.assets import environment

import gramadapt


environment.append_path(
    Path(gramadapt.__file__).parent.joinpath('static').as_posix(),
    url='/gramadapt:static/')
environment.load_path = list(reversed(environment.load_path))
