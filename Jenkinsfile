@Library('tenable.common')

import com.tenable.jenkins.builds.*
import com.tenable.jenkins.common.*
import com.tenable.jenkins.Constants
import com.tenable.jenkins.builds.snyk.*

//pythonVersion = [ '3.6', '3.7', '3.8', '3.9' ]
pythonVersion = [ '3.6' ]

bparams = new BuildParams(this, 1083)
bparams.channels = '#jenkins-devel'
bparams.snykContainer = 'python:3.6-buster'

common = new Common(this)
buildsCommon = new BuildsCommon(this)

void unittests(String version) {
    echo "Version: ${version}"

    stage("unittest${version}") {
        node(Constants.DOCKERNODE) {
            buildsCommon.cleanup()
            checkout scm

            withContainer(image: "python:${version}-buster", registry: '', inside: '-u root') {
                sh 'python --version'
                sh """
                    python -m pip install --upgrade pip
                    pip install -r test-requirements.txt
                    pip install -r requirements.txt

                    pytest --vcr-record=none --cov-report term-missing --cov=tenable tests
                    find .
                """
            }
        }
    }
}

try {
    Map tasks = [ : ]

    pythonVersion.each {
        version ->
            echo "Version: ${version}"
            tasks[version] = { unittests(version) }
    }

    tasks['snyk'] = {
        stage('snyk') {
            Snyk snyk = new Snyk(script, parameters)
            snyk.execute()
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
