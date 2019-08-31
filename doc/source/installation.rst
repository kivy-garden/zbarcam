.. _install:

************
Installation
************

Supported versions
------------------

* Python 3.5+

Dependencies
------------

#. `Kivy <https://kivy.org/#download>`_


Installation
------------

Please see the `garden docs <https://kivy-garden.github.io/>`_ for full installation instructions.

You can install flower master directly from github with::

    python -m pip install https://github.com/kivy-garden/flower/archive/master.zip

Look under the repository's releases tab if you'd like to install a specific
release or a pre-compiled wheel, if the flower has any. Then use the url with
`pip`.

Or you can automatically install it using garden's pypi server with::

    python -m pip install kivy_garden.flower --extra-index-url https://kivy-garden.github.io/simple/

To permanently add our garden server to your pip configuration so that you
don't have to specify it with `--extra-index-url`, add::

    [global]
    timeout = 60
    index-url = https://kivy-garden.github.io/simple/

to your `pip.conf <https://pip.pypa.io/en/stable/user_guide/#config-file>`_.

If the flower maintainer has uploaded the flower to
`pypi <https://pypi.org/>`_, you can just install it with
`pip install kivy_garden.flower`.
