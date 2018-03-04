.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/espona/ckanext-composite.svg?branch=master
    :target: https://travis-ci.org/espona/ckanext-composite
 
.. image:: https://coveralls.io/repos/espona/ckanext-composite/badge.svg
  :target: https://coveralls.io/r/espona/ckanext-composite

.. image:: https://img.shields.io/pypi/dm/ckanext-composite.svg
    :target: https://pypi.python.org/pypi//ckanext-composite/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/ckanext-composite.svg
    :target: https://pypi.python.org/pypi/ckanext-composite/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/ckanext-composite.svg
    :target: https://pypi.python.org/pypi/ckanext-composite/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/status/ckanext-composite.svg
    :target: https://pypi.python.org/pypi/ckanext-composite/
    :alt: Development Status

.. image:: https://img.shields.io/pypi/l/ckanext-composite.svg
    :target: https://pypi.python.org/pypi/ckanext-composite/
    :alt: License

=============
ckanext-composite
=============

.. Put a description of your extension here:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!
   
Allows to store structured dataset metadata, single or multiple fields. Only one level of subfields is possible. The subfields can be basic text, date type o choice dropboxes. Do not use dashes or numbers in the labels or values of fields.


------------
Requirements
------------

Developed for CKAn version 2.5.2. Requires the extensions ckanext-scheming and ckanext-repeating (using version from repository eawag-rdm).

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-composite:

0. Install the ckan extensions ckanext-scheming and ckanext-composite

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-composite Python package into your virtual environment::

     pip install ckanext-composite

3. Add ``composite`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Additional config settings::

     scheming.presets = ckanext.scheming:presets.json
                        ckanext.repeating:presets.json
                        ckanext.composite:presets.json

Add this to your schema.json file::

     # Composite Field
     {
      "field_name": "maintainer",
      "label": "Maintainer",
      "preset": "composite",
      "subfields":[
          {
            "field_name": "name",
            "label": "Name",
            "form_placeholder": "Joe Bloggs"
          },
          {
            "field_name": "email",
            "label": "Email",
            "form_placeholder": "joe@example.com"
           },
          {
            "field_name": "date",
            "label": "Date",
            "preset": "date",
            "form_placeholder": "yyyy-mm-mm"
           },
           {
            "field_name": "identifier_scheme",
            "label": "Scheme",
            "preset": "select",
            "choices": [
              {
                "value": "orcid",
                "label": "ORCID"
              },
              {
                "value": "isni",
                "label": "ISNI"
              }
           ]
         }
      ]
     }
     # Composite Repeating Field
     {
      "field_name": "author",
      "label": "Authors",
      "preset": "composite_repeating",
      "form_blanks": 1,
      "subfields": [
          {
            "field_name": "name",
            "label": "Name",
            "form_placeholder":"eg. John Smith"
          },
          {
            "field_name": "type",
            "label": "Type",
            choices = [
             {
                "value": "collaborator",
                "label": "Collaborator"
              },
              {
                "value": "editor",
                "label": "Editor"
              }
            ]
          }
       ]
      }
      
------------------------
Development Installation
------------------------

To install ckanext-composite for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/espona/ckanext-composite.git
    cd ckanext-composite
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.composite --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-composite on PyPI
---------------------------------

ckanext-composite should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-composite. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-composite
----------------------------------------

ckanext-composite is availabe on PyPI as https://pypi.python.org/pypi/ckanext-composite.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
