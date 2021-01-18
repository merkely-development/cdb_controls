#!/bin/sh

set -e

# ${1} is set in Makefile.
# Defaults to tests/ (the dir name)
# To run an individual test file...
# $ make test TARGET=test_create_release.py
# which will result in ${1}==tests/test_release.py
readonly TARGET="${1}"

# According to https://github.com/approvals/ApprovalTests.Python
# you can setup the approval-test reporter with this option:
#
#   --approvaltests-use-reporter='PythonNative'
#
# Unfortunately this is currently broken with the latest release
# of pytest-approvals. For now you have to specify the reporter
# individually on each verify call. For example:
#
#    from approvaltests.approvals import verify
#    from approvaltests.reporters import PythonNativeReporter
#    verify(actual, PythonNativeReporter())
#
# If you don't do this you _lose_ output, eg for a new test the
# name of the missing approval file does not appear.

pytest \
       --capture=no \
       --cov=. \
       --cov-config=.coveragerc \
       --junitxml=htmlcov/junit.xml \
       -o junit_family=xunit1 \
       --pythonwarnings=ignore::pytest.PytestCollectionWarning \
       --verbose \
         "${TARGET}"

# Generate html results
coverage html

# Add json stats to htmlcov folder
coverage json -o htmlcov/coverage.json

# Add report
readonly REPORT_FILENAME=htmlcov/summary.txt
coverage report -m > "${REPORT_FILENAME}"

# Create a file containing the coverage percentage
cat "${REPORT_FILENAME}" | grep TOTAL | awk '{print "COVERAGE=\""$4"\""}' > htmlcov/test_coverage.txt

# Create a file containing the number of test cases
TEST_CASES=`pytest --collect-only -q  --ignore=integration_tests | head -n -2 | wc -l`
echo TEST_CASES=$TEST_CASES > htmlcov/test_cases.txt
