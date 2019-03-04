"""
This is required when the package is installed via garden,
because garden copies the entire repository to e.g. `~/.kivy/garden/`.
Therefore we turn `~/.kivy/garden/garden.zbarcam/` to a package,
so it can imported via:
```python
from kivy.garden.zbarcam import ZBarCam
```
"""
from .zbarcam import ZBarCam  # noqa
