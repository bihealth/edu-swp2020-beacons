Welcome to edu-swp2020-beacons's documentation!
===============================================

für Info field lists https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#info-field-lists

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Modules
-------

.. autosummary::
   :toctree: generated
   
   beacon.admin_cli
   beacon.admin_tools
   beacon.common
   beacon.database
   beacon.flask_app
   beacon.rest_api
   beacon.settings
   beacon.user_cli 

Functions...
------------

.. automodule:: beacon.admin_cli
   :members:

.. automodule:: beacon.admin_tools
   :members:

.. automodule:: beacon.common
   :members:

.. automodule:: beacon.database
   :members:

.. automodule:: beacon.settings
   :members:

.. automodule:: beacon.user_cli
   :members:

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
Examples
========

This a usage of :func:`beacon.admin_cli`:

	>>> python3 -m beacon.admin_cli -h 
	>>> DB Path: *give the working directory of data.db file* 

with ```-h``` or ```--help``` you can see which flag you can use.
