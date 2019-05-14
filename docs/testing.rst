Testing the Library
===================

To run through the test suite for pyTenable, we'll need to install a few 
pre-requisites first.  pyTenable uses py.test & VCRpy to run through the
pre-recorded API calls an validate that the code is performing as intended.

.. code-block:: bash

    pip install -r dev-requirements.txt

Once the pre-requisites are installed, it's simply a matter of running the
test suite:

.. code-block:: bash

    pytest --vcr-record=none --cov=tenable tests

If you would like to run through the test suite with a live Tenable.io
container, you'll want to perform the following actions:

.. code-block:: bash

    export TIO_TEST_ADMIN_ACCESS="ADMIN_API_ACCESS_KEY_HERE"
    export TIO_TEST_ADMIN_SECRET="ADMIN_API_SECRET_KEY_HERE"
    export TIO_TEST_STD_ACCESS="STANDARD_ACCOUNT_ACCESS_KEY_HERE"
    export TIO_TEST_STD_SECRET="STANDARD_ACCOUNT_SECRET_KEY_HERE"
    pytest --disable-vcr --cov=tenable.io tests/io

For Tenable.sc, you would run the following:

.. code-block:: bash

    export SC_TEST_HOST="TENABLE_SC_IP_OR_FQDN"
    export SC_TEST_USER="TENABLE_SC_SECMANAGER_USER"
    export SC_TEST_PASS="TENABLE_SC_SECMANAGER_PASSWORD"
    export SC_TEST_ADMIN_USER="TENABLE_SC_ADMIN_USER"
    export SC_TEST_ADMIN_PASS="TENABLE_SC_ADMIN_PASSWORD"
    pytest --disable-vcr --cov=tenable.sc tests/sc