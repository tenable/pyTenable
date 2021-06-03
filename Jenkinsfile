@Library('tenable.common')

import com.tenable.jenkins.builds.*
import com.tenable.jenkins.common.*
import com.tenable.jenkins.Constants

pythonVersion = [ '3.6', '3.7', '3.8', '3.9' ]

bparams = new BuildParams(this, 1083)
bparams.channels = '#jenkins-devel'

common = new Common(this)
buildsCommon = new BuildsCommon(this)

void unittests(String version) {
    echo "Version: version"

    node(Constants.DOCKERNODE) {
        buildsCommon.buildInit(bparams)        

        withContainer(image: "${version}-buster", registry: '') {
            sh 'python --version'
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
