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
