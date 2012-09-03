.. _install:

============
Installation
============

.. _install-requirements:

Requirements
============

This application requires

* `Django`_ 1.5 or newer
* `django-easysettings`_

.. _install-download:

Download
========

The latest release package can be downloaded from `the GitHub download page`_.

.. _`the GitHub download page`: https://github.com/tarak/django-change-email/downloads

.. _install-install:

Installing
==========

Once you've downloaded the package, unpack it (on most operating systems, simply
double-click; alternately, at a command line on Linux, Mac OS X or other
Unix-like systems, type)::

    $ tar zxvf django-change-email-<VERSION>.tar.gz

This will create the directory::

    django-change-email-<VERSION>

which contains
the ``setup.py`` installation script. From a command line in that directory,
type::

    python setup.py install

Note that on some systems you may need to execute this with
administrative privileges (e.g., ``sudo python setup.py install``).

Another possibility to install the application is to create a link to the app
inside the Python path::

    $ sudo ln -s django-change-email/change_email /path/to/python_site_packages/change_email


.. _`Django`: https://www.djangoproject.com/
.. _`django-easysettings`: https://github.com/SmileyChris/django-easysettings
