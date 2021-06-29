@Library('tenable.common')

import com.tenable.jenkins.builds.*
import com.tenable.jenkins.common.*
import com.tenable.jenkins.Constants
import com.tenable.jenkins.builds.snyk.*
import com.tenable.jenkins.builds.nexusiq.*

pythonVersion = [ '3.6', '3.7', '3.8', '3.9' ]

bparams = new BuildParams(this, 1083)
bparams.channels = '#jenkins-devel'
bparams.snykContainer = 'python:3.6-buster'
bparams.snykRegistry = ''
bparams.snykType = 'PYTHON'
bparams.nexusiqtype = 'PREQUIREMENT'

GlobalContext.put('appid', bparams.appid)

common = new Common(this)
buildsCommon = new BuildsCommon(this)

void unittests(String version) {
    stage("unittest${version}") {
        node(Constants.DOCKERNODE) {
            buildsCommon.cleanup()
            checkout scm

            withContainer(image: "python:${version}-buster", registry: '', inside: '-u root --privileged -v /var/run/docker.sock:/var/run/docker.sock') {
                try {
                    sh """
                        python -m pip install --upgrade pip
                        pip install -r test-requirements.txt
                        pip install -r requirements.txt

                        pytest --vcr-record=none --cov-report html:test-reports/coverage --junitxml=test-reports/junit/results.xml --junit-prefix=${version} --cov=tenable tests
                        find . -name *.html
                        find . -name *.xml
                    """
                }
                catch(ex) {
                    throw ex
                }
                finally {
                    if (fileExists ('test-reports/coverage/index.html')) {
                        publishHTML(
                            [allowMissing: true,
                             alwaysLinkToLastBuild: true,
                             keepAll     : true,
                             reportDir   : 'test-reports/coverage/',
                             reportFiles : 'index.html',
                             reportName  : "Coverage${version}",
                             reportTitles: "Coverage${version}"])
                    }
                    step([$class: 'JUnitResultArchiver', testResults: 'test-reports/junit/*.xml'])
                }
            }
        }
    }
}

try {
    Map tasks = [ : ]

    pythonVersion.each {
        version ->
            tasks[version] = { unittests(version) }
    }

    tasks['runPyPi'] = {
        stage('runPyPi')
        {
            try {
              step('runPyPi') {
                  String prodOrTest = env.BRANCH_NAME == 'master' ?  'prod' : 'test'
                  withCredentials([[$class : 'UsernamePasswordMultiBinding',
                  credentialsId : "PYP${prodOrTest}", usernameVariable : 'PYPIUSERNAME',
                  passwordVariable : 'PYPIPASSWORD']]) {
                  sh """
                    rm -rf dist
                    python setup.py sdist
                    twine upload --repository-url https://upload.pypi.org/legacy/ --skip-existing dist/* -u ${PYPIUSERNAME} -p ${PYPIPASSWORD}
                  """
                  }
                }
            } catch(ex) {
            throw ex
            }
        }`
    }

    tasks['runPylint'] = {
        stage('runPylint')
        {
            try {
              step('runPylint') {
              try {
                sh """
                   pylint --exit-zero --output-format=parseable --reports=n tenable > reports/pylint_tenable.log
                   pylint --exit-zero --output-format=parseable --reports=n tests > reports/pylint_tests.log
                   cat reports/pylint_tenable.log
                   cat reports/pylint_tests.log
                """
              }
            } catch(ex) {
                throw ex
                }
            finally {
                if (fileExists ('reports/pylint_tenable.log')) {
                       //result needs to outpyt, will test
                       result =  recordIssues(
                            enabledForFailure: true,
                            tool: pyLint(pattern: '**/pylint.log'),
                            unstableTotalAll: 20,
                            failedTotalAll: 30,
                    )
                }
                if (fileExists ('reports/pylint_test.log')) {
                       //result needs to outpyt, will test
                       result =  recordIssues(
                            enabledForFailure: true,
                            tool: pyLint(pattern: 'reports/pylint_*.log'),
                            unstableTotalAll: 20,
                            failedTotalAll: 30,
                    )
                }
            }
        }
    }

    tasks['snyk'] = {
        stage('snyk') {
            Snyk snyk = new Snyk(this, bparams)
            snyk.execute()
        }
    }

    tasks['sonarqube'] = {
        stage('sonarqube') {
            SonarQube.execute(this, bparams)
        }
    }

    tasks['nexusiq'] = {
        stage('nexusiq') {
            Nexusiq.execute(this, bparams)
        }
    }

    parallel(tasks)

    common.setResultIfNotSet(Constants.JSUCCESS)
} 
catch (ex) {
    common.logException(ex)
    common.setResultAbortedOrFailure()
    throw ex
} 
finally {
    common.setResultIfNotSet(Constants.JFAILURE)
    buildsCommon.notifyPostBuild(bparams)
}
