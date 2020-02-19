export TESTING_PYTHON_VERSIONS="2.7.15 3.4.9 3.5.6 3.6.7 3.7.5"

function perform_cleanup {
    echo "Cleaning up the Nessus Reports."
    rm -f *.nessus
}

function run_tests {
    echo -e "--- Code Complexity Report ---"
    radon cc --total-average -n D tenable

    echo -e "\n\n-- Code Maintainability Report ---"
    radon mi tenable

    echo -en "\n\n"
    if [ "${1}" == "record" ];then
        pytest --cov=tenable tests
    elif [ "${1}" == "integration" ];then
        pytest --disable-vcr --cov=tenable tests
    else
        pytest --vcr-record=none --cov=tenable tests
    fi
    return $?
}