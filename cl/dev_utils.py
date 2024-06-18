from __future__ import annotations as _annotations

import colex
from actus import LogSection, Style


dev = LogSection("Dev").disable_output().set_style(Style(
    label=colex.AZURE+colex.BOLD
))
