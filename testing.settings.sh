export TESTING_PYTHON_VERSIONS="2.7.15 3.4.9 3.5.6 3.6.7 3.7.1"

export TIO_TEST_ADMIN_ACCESS=""
export TIO_TEST_ADMIN_SECRET=""
export TIO_TEST_STD_ACCESS=""
export TIO_TEST_STD_SECRET=""
export NESSUS_LICENSE=""
export TIO_REG_ACCESS_KEY=""
export TIO_REG_SECRET_KEY=""
export SC_TEST_HOST=""
export SC_TEST_PORT=""
export SC_TEST_USER=""
export SC_TEST_PASS=""

function perform_cleanup {
    echo "Cleaning up the Nessus Reports."
    rm -f *.nessus
}

function run_tests {
    if [ "${1}" == "record" ];then
        pytest --cov=tenable tests
    elif [ "${1}" == "integration" ];then
        pytest --disable-vcr --cov=tenable tests
    else
        pytest --vcr-record=none --cov=tenable tests
    fi
    return $?
}