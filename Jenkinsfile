@Library('tenable.common')

pythonVersion = [ '3.6', '3.7', '3.8', '3.9' ]

BuildParams bparams = new BuildParams(this, 1083)
bparams.channels = '#jenkins-devel'

Common common = new Common(this)
BuildsCommon buildsCommon = new BuildsCommon(this)

void unittests(String version) {
    echo "Version: version"
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
