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
releaseBuild = 'No'

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
                } catch(ex) {
                    throw ex
                } finally {
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

void uploadPackagePyPI() {
    node(Constants.DOCKERNODE) {
        buildsCommon.cleanup()
        checkout scm
        withContainer(image: "python:3.6-buster", registry: '', inside: '-u root') {
            try {
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: "PYPIPROD", usernameVariable: 'PYPIUSERNAME', passwordVariable: 'PYPIPASSWORD']]) {
                    sh
                    """
                    rm -rf dist
                    python setup.py sdist
                    pip install twine
                    twine upload --repository-url https://upload.pypi.org/legacy/ --skip-existing dist/* -u ${PYPIUSERNAME} -p ${PYPIPASSWORD}
                    """
                }
            } catch (ex) {
                throw ex
            } finally {
                print("Upload Done successfully")
            }
        }
    }
}


try {
    Map tasks = [: ]

    pythonVersion.each {
        version ->
            tasks[version] = {
                unittests(version)
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
    
    tasks['runLint'] = {
        stage('runLint') {
            node(Constants.DOCKERNODE) {
                buildsCommon.cleanup()
                checkout scm

                withContainer(image: "python:3.6-buster", registry: '', inside: '-u root') {
                    try {
                        sh """
                        mkdir reports
                        touch reports/pylint_tenable.log
                        pip install pylint
                        pylint --rcfile=.pylintrc --exit-zero --output-format=parseable --reports=n tenable tests > reports/pylint_tenable.log
                        touch reports/yamllint_tenable.log
                        pip install yamllint
                        yamllint -c .yamllint tests/io/cassettes tests/sc/cassettes tests/cs/cassettes > reports/yamllint_tenable.log
                       """
                    } catch (ex) {
                        throw ex
                    } finally {
                        resultPylint = recordIssues(
                            enabledForFailure: true, tool: pyLint(pattern: 'reports/pylint_tenable.log'), unstableTotalAll: 5000, failedTotalAll: 5000)
                        resultYamllint = recordIssues(
			                enabledForFailure: true, tool: yamlLint(pattern: 'reports/yamllint_tenable.log'), unstableTotalAll: 5000, failedTotalAll: 5000 )
                    }
                }
            }
        }
    }

    parallel(tasks)
    common.setResultIfNotSet(Constants.JSUCCESS)
    if (env.BRANCH_NAME == 'master' && releaseBuild == 'Yes') {
        uploadPackagePyPI()
    }

} catch (ex) {
    common.logException(ex)
    common.setResultAbortedOrFailure()
    throw ex
} finally {
    common.setResultIfNotSet(Constants.JFAILURE)
    buildsCommon.notifyPostBuild(bparams)
}
