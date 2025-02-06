"""
test file for testing various scenarios in security center's scans functionality
"""

import pytest

from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception

from ..checker import check


def test_schedule_constructor_type_typeerror(security_center):
    """
    test schedule constructor for 'type' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._schedule_constructor({"type": 1})


def test_schedule_constructor_type_unexpected_value(security_center):
    """
    test schedule constructor for 'type' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        security_center.scans._schedule_constructor({"type": "nothing here"})


def test_schedule_constructor_start_typeerror(security_center):
    """
    test schedule constructor for 'start' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._schedule_constructor(
            {"type": "ical", "start": 1, "repeatRule": ""}
        )


def test_schedule_constructor_rrule_typeerror(security_center):
    """
    test schedule constructor for 'repeat rule' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._schedule_constructor(
            {"type": "ical", "start": "", "repeatRule": 1}
        )


def test_scans_constructor_name_typeerror(security_center):
    """
    test scans constructor for 'name' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(name=1)


def test_scans_constructor_type_typeerror(security_center):
    """
    test scans constructor for 'type' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(type=1)


def test_scans_constructor_type_unexpectedvalueerror(security_center):
    """
    test scans constructor for 'type' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        security_center.scans._constructor(type="something")


def test_scans_constructor_description_typeerror(security_center):
    """
    test scans constructor for 'description' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(description=1)


def test_scans_constructor_repo_typeerror(security_center):
    """
    test scans constructor for 'repo' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(repo="nope")


def test_scans_constructor_repo_success(security_center):
    """
    test scans constructor for 'repo' success
    """
    resp = security_center.scans._constructor(repo=1)
    assert resp == {"repository": {"id": 1}}


def test_scans_constructor_scan_zone_typeerror(security_center):
    """
    test scans constructor for 'scan_zone' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(scan_zone="nope")


def test_scans_constructor_scan_zone_success(security_center):
    """
    test scans constructor for 'scan_zone' success
    """
    resp = security_center.scans._constructor(scan_zone=1)
    assert resp == {"zone": {"id": 1}}


def test_scans_constructor_email_complete_typeerror(security_center):
    """
    test scans constructor for 'email complete' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(email_complete="nope")


def test_scans_constructor_email_complete_success(security_center):
    """
    test scans constructor for 'email complete' success
    """
    resp = security_center.scans._constructor(email_complete=True)
    assert resp == {"emailOnFinish": "true"}


def test_scans_constructor_email_launch_typeerror(security_center):
    """
    test scans constructor for 'email launch' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(email_launch="nope")


def test_scans_constructor_email_launch_success(security_center):
    """
    test scans constructor for 'email launch' success
    """
    resp = security_center.scans._constructor(email_launch=True)
    assert resp == {"emailOnLaunch": "true"}


def test_scans_constructor_timeout_typeerror(security_center):
    """
    test scans constructor for 'timeout' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(timeout=1)


def test_scans_constructor_inactivity_timeout(security_center):
    """
    Tests inactivity_timeout is mapped correctly in the constructor.
    """
    scan_params = {"inactivity_timeout": 3600, "policy_id": 1000001}

    scan = security_center.scans._constructor(**scan_params)

    assert "inactivity_timeout" not in scan
    assert scan["inactivityTimeout"] == "3600"


def test_scans_constructor_timeout_unexpectedvalueerror(security_center):
    """
    test scans constructor for 'timeout' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        security_center.scans._constructor(timeout="something")


def test_scans_constructor_timeout_success(security_center):
    """
    test scans constructor for 'timeout' success
    """
    resp = security_center.scans._constructor(timeout="rollover")
    assert resp == {"timeoutAction": "rollover"}


def test_scans_constructor_host_tracking_typeerror(security_center):
    """
    test scans constructor for 'host tracking' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(host_tracking="something")


def test_scans_constructor_host_tracking_success(security_center):
    """
    test scans constructor for 'host tracking' success
    """
    assert {"dhcpTracking": "true"} == security_center.scans._constructor(
        host_tracking=True
    )


def test_scans_constructor_vhosts_typeerror(security_center):
    """
    test scans constructor for 'vhosts' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(vhosts="nope")


def test_scans_constructor_vhosts_success(security_center):
    """
    test scans constructor for 'vhosts' success
    """
    resp = security_center.scans._constructor(vhosts=True)
    assert resp == {"scanningVirtualHosts": "true"}


def test_scans_constructor_rollover_typeerror(security_center):
    """
    test scans constructor for 'rollover' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(rollover=1)


def test_scans_constructor_rollover_unexpectedvalueerror(security_center):
    """
    test scans constructor for 'rollover' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        security_center.scans._constructor(rollover="something")


def test_scans_constructor_rollover_success(security_center):
    """
    test scans constructor for 'rollover' success
    """
    assert {"rolloverType": "nextDay"} == security_center.scans._constructor(
        rollover="nextDay"
    )


def test_scans_constructor_targets_typeerror(security_center):
    """
    test scans constructor for 'targets' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(targets="something")


def test_scans_constructor_targets_success(security_center):
    """
    test scans constructor for 'targets' success
    """
    resp = security_center.scans._constructor(targets=["127.0.0.1", "127.0.0.2"])
    assert resp == {"ipList": "127.0.0.1,127.0.0.2"}


def test_scans_constructor_max_time_typeerror(security_center):
    """
    test scans constructor for 'max time' type error
    """
    with pytest.raises(ValueError):
        security_center.scans._constructor(max_time="nope")


def test_scans_constructor_max_time_success(security_center):
    """
    test scans constructor for 'max time' success
    """
    resp = security_center.scans._constructor(max_time=3600)
    assert resp == {"maxScanTime": "3600"}


def test_scans_constructor_max_time_zero(security_center):
    """
    test scans constructor for 'max time' zero
    """
    resp = security_center.scans._constructor(max_time=0)
    assert resp == {"maxScanTime": "0"}


def test_scans_constructor_schedule_success(security_center):
    """
    test scans constructor for 'schedule' success
    """
    scan = security_center.scans._constructor(schedule={"type": "ical", "start": ""})
    assert {"schedule": {"type": "ical", "start": ""}} == scan


def test_scans_constructor_auto_mitigation_typeerror(security_center):
    """
    test scans constructor for 'auto mitigation' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(auto_mitigation="nope")


def test_scans_constructor_auto_mitigation_success(security_center):
    """
    test scans constructor for 'auto mitigation' success
    """
    resp = security_center.scans._constructor(auto_mitigation=True)
    assert resp == {"classifyMitigatedAge": "true"}


def test_scans_constructor_reports_typeerror_base(security_center):
    """
    test scans constructor for 'reports' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(reports="nope")


def test_scans_constructor_reports_typeerror_id(security_center):
    """
    test scans constructor reports for 'id' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(
            reports=[{"id": "nope", "reportSource": "cumulative"}]
        )


def test_scans_constructor_reports_typeerror_report_source(security_center):
    """
    test scans constructor reports for 'report source' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(reports=[{"id": 1, "reportSource": 1}])


def test_scans_constructor_reports_unexpectedvalueerror_reportsource(security_center):
    """
    test scans constructor reports for 'report source' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        security_center.scans._constructor(
            reports=[{"id": 1, "reportSource": "something"}]
        )


def test_scans_constructor_reports_success(security_center):
    """
    test scans constructor reports for success
    """
    resp = security_center.scans._constructor(
        reports=[{"id": 1, "reportSource": "cumulative"}]
    )
    assert resp == {"reports": [{"id": 1, "reportSource": "cumulative"}]}


def test_scans_constructor_asset_lists_typeerror(security_center):
    """
    test scans constructor for 'asset lists' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(asset_lists=1)


def test_scans_constructor_asset_list_id_typeerror(security_center):
    """
    test scans constructor for 'asset list id' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(
            asset_lists=[
                "nope",
            ]
        )


def test_scans_constructor_asset_lists_success(security_center):
    """
    test scans constructor for 'asset lists' success
    """
    resp = security_center.scans._constructor(asset_lists=[1, 2])
    assert resp == {"assets": [{"id": 1}, {"id": 2}]}


def test_scans_constructor_creds_typeerror(security_center):
    """
    test scans constructor for 'creds' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(creds=1)


def test_scans_constructor_creds_id_typeerror(security_center):
    """
    test scans constructor for 'creds id' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(creds=["nope"])


def test_scans_constructor_creds_success(security_center):
    """
    test scans constructor for creds success
    """
    resp = security_center.scans._constructor(creds=[1, 2])
    assert resp == {"credentials": [{"id": 1}, {"id": 2}]}


def test_scans_constructor_plugin_id_success(security_center):
    """
    test scans constructor for plugin id success
    """
    resp = security_center.scans._constructor(policy_id=19506)
    assert resp == {"type": "policy", "policy": {"id": 19506}}


def test_scans_constructor_policy_id_typeerror(security_center):
    """
    test scans constructor for 'policy id' type error
    """
    with pytest.raises(TypeError):
        security_center.scans._constructor(policy_id="nope")


def test_scans_constructor_policy_id_success(security_center):
    """
    test scans constructor for 'policy id' success
    """
    resp = security_center.scans._constructor(policy_id=1)
    assert resp == {"type": "policy", "policy": {"id": 1}}


@pytest.fixture
def scan(request, security_center, vcr):
    """
    test fixture for scan
    """
    with vcr.use_cassette("sc_scans_create"):
        scan = security_center.scans.create(
            "Example Scan",
            1,
            schedule_type="template",
            targets=["127.0.0.1"],
            policy_id=1000001,
        )

    def teardown():
        try:
            security_center.scans.delete(int(scan["id"]))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return scan


@pytest.mark.vcr()
def test_scans_list(security_center):
    """
    test scans list for success
    """
    scans = security_center.scans.list()
    for scan in scans["usable"]:
        assert isinstance(scan, dict)
        check(scan, "id", str)
        check(scan, "name", str)
        check(scan, "description", str)
        check(scan, "status", str)


@pytest.mark.vcr()
def test_scans_list_for_fields(security_center):
    """
    test scans list success for fields
    """
    scans = security_center.scans.list(fields=["id", "name"])
    for scan in scans["usable"]:
        assert isinstance(scan, dict)
        check(scan, "id", str)
        check(scan, "name", str)


@pytest.mark.vcr()
def test_scans_details(security_center, scan):
    """
    test scans details for success
    """
    scan = security_center.scans.details(int(scan["id"]))
    assert isinstance(scan, dict)
    check(scan, "id", str)
    check(scan, "name", str)
    check(scan, "description", str)
    check(scan, "ipList", str)
    check(scan, "type", str)
    check(scan, "dhcpTracking", str)
    check(scan, "classifyMitigatedAge", str)
    check(scan, "emailOnLaunch", str)
    check(scan, "emailOnFinish", str)
    check(scan, "timeoutAction", str)
    check(scan, "scanningVirtualHosts", str)
    check(scan, "rolloverType", str)
    check(scan, "status", str)
    check(scan, "createdTime", str)
    check(scan, "modifiedTime", str)
    check(scan, "reports", list)
    check(scan, "assets", list)
    check(scan, "numDependents", str)
    check(scan, "schedule", dict)
    check(scan["schedule"], "id", str)
    check(scan["schedule"], "type", str)
    check(scan["schedule"], "start", str)
    check(scan["schedule"], "repeatRule", str)
    check(scan["schedule"], "nextRun", int)
    check(scan, "policy", dict)
    check(scan["policy"], "id", str)
    check(scan["policy"], "name", str)
    check(scan["policy"], "description", str)
    check(scan, "policyPrefs", list)
    check(scan, "repository", dict)
    check(scan["repository"], "id", str)
    check(scan["repository"], "name", str)
    check(scan["repository"], "description", str)
    check(scan, "ownerGroup", dict)
    check(scan["ownerGroup"], "id", str)
    check(scan["ownerGroup"], "name", str)
    check(scan["ownerGroup"], "description", str)
    check(scan, "creator", dict)
    check(scan["creator"], "id", str)
    check(scan["creator"], "username", str)
    check(scan["creator"], "firstname", str)
    check(scan["creator"], "lastname", str)
    check(scan, "owner", dict)
    check(scan["owner"], "id", str)
    check(scan["owner"], "username", str)
    check(scan["owner"], "firstname", str)
    check(scan["owner"], "lastname", str)


@pytest.mark.vcr()
def test_scans_details_for_fields(security_center, scan):
    """
    test scans details success for fields
    """
    scan_details = security_center.scans.details(
        int(scan["id"]), fields=["id", "name", "description"]
    )
    assert isinstance(scan_details, dict)
    check(scan_details, "id", str)
    check(scan_details, "name", str)
    check(scan_details, "description", str)


@pytest.mark.vcr()
def test_scans_create(scan):
    """
    test scans create for success
    """
    assert isinstance(scan, dict)
    check(scan, "id", str)
    check(scan, "name", str)
    check(scan, "description", str)
    check(scan, "ipList", str)
    check(scan, "type", str)
    check(scan, "dhcpTracking", str)
    check(scan, "classifyMitigatedAge", str)
    check(scan, "emailOnLaunch", str)
    check(scan, "emailOnFinish", str)
    check(scan, "timeoutAction", str)
    check(scan, "scanningVirtualHosts", str)
    check(scan, "rolloverType", str)
    check(scan, "status", str)
    check(scan, "createdTime", str)
    check(scan, "modifiedTime", str)
    check(scan, "reports", list)
    check(scan, "assets", list)
    check(scan, "numDependents", str)
    check(scan, "schedule", dict)
    check(scan["schedule"], "id", str)
    check(scan["schedule"], "type", str)
    check(scan["schedule"], "start", str)
    check(scan["schedule"], "repeatRule", str)
    check(scan["schedule"], "nextRun", int)
    check(scan, "policy", dict)
    check(scan["policy"], "id", str)
    check(scan["policy"], "name", str)
    check(scan["policy"], "description", str)
    check(scan, "policyPrefs", list)
    check(scan, "repository", dict)
    check(scan["repository"], "id", str)
    check(scan["repository"], "name", str)
    check(scan["repository"], "description", str)
    check(scan, "ownerGroup", dict)
    check(scan["ownerGroup"], "id", str)
    check(scan["ownerGroup"], "name", str)
    check(scan["ownerGroup"], "description", str)
    check(scan, "creator", dict)
    check(scan["creator"], "id", str)
    check(scan["creator"], "username", str)
    check(scan["creator"], "firstname", str)
    check(scan["creator"], "lastname", str)
    check(scan, "owner", dict)
    check(scan["owner"], "id", str)
    check(scan["owner"], "username", str)
    check(scan["owner"], "firstname", str)
    check(scan["owner"], "lastname", str)


@pytest.mark.vcr()
def test_scans_create_plugin(security_center):
    """
    test scans create plugin for success
    """
    scan = security_center.scans.create(
        "Example Scan 9",
        9,
        schedule_type="template",
        targets=["127.0.0.1"],
        plugin_id=1000001,
    )
    assert isinstance(scan, dict)
    check(scan, "id", str)
    check(scan, "name", str)
    check(scan, "description", str)
    security_center.scans.delete(int(scan["id"]))


@pytest.mark.vcr()
def test_scans_edit(security_center, scan):
    """
    test scans edit for success
    """
    scan = security_center.scans.edit(int(scan["id"]), name="Edited Example Scan")
    assert isinstance(scan, dict)
    check(scan, "id", str)
    check(scan, "name", str)
    check(scan, "description", str)
    check(scan, "ipList", str)
    check(scan, "type", str)
    check(scan, "dhcpTracking", str)
    check(scan, "classifyMitigatedAge", str)
    check(scan, "emailOnLaunch", str)
    check(scan, "emailOnFinish", str)
    check(scan, "timeoutAction", str)
    check(scan, "scanningVirtualHosts", str)
    check(scan, "rolloverType", str)
    check(scan, "status", str)
    check(scan, "createdTime", str)
    check(scan, "modifiedTime", str)
    check(scan, "reports", list)
    check(scan, "assets", list)
    check(scan, "numDependents", str)
    check(scan, "schedule", dict)
    check(scan["schedule"], "id", str)
    check(scan["schedule"], "type", str)
    check(scan["schedule"], "start", str)
    check(scan["schedule"], "repeatRule", str)
    check(scan["schedule"], "nextRun", int)
    check(scan, "policy", dict)
    check(scan["policy"], "id", str)
    check(scan["policy"], "name", str)
    check(scan["policy"], "description", str)
    check(scan, "policyPrefs", list)
    check(scan, "repository", dict)
    check(scan["repository"], "id", str)
    check(scan["repository"], "name", str)
    check(scan["repository"], "description", str)
    check(scan, "ownerGroup", dict)
    check(scan["ownerGroup"], "id", str)
    check(scan["ownerGroup"], "name", str)
    check(scan["ownerGroup"], "description", str)
    check(scan, "creator", dict)
    check(scan["creator"], "id", str)
    check(scan["creator"], "username", str)
    check(scan["creator"], "firstname", str)
    check(scan["creator"], "lastname", str)
    check(scan, "owner", dict)
    check(scan["owner"], "id", str)
    check(scan["owner"], "username", str)
    check(scan["owner"], "firstname", str)
    check(scan["owner"], "lastname", str)


@pytest.mark.vcr()
def test_scans_delete(scan, security_center):
    """
    test scans delete for success
    """
    security_center.scans.delete(int(scan["id"]))


@pytest.mark.vcr()
def test_scans_copy(scan, security_center):
    """
    test scans copy for success
    """
    scan = security_center.scans.copy(int(scan["id"]), "scan_copy", 1)
    security_center.scans.delete(int(scan["id"]))
    assert isinstance(scan, dict)
    check(scan, "id", str)
    check(scan, "name", str)
    check(scan, "description", str)
    check(scan, "ipList", str)
    check(scan, "type", str)
    check(scan, "dhcpTracking", str)
    check(scan, "classifyMitigatedAge", str)
    check(scan, "emailOnLaunch", str)
    check(scan, "emailOnFinish", str)
    check(scan, "timeoutAction", str)
    check(scan, "scanningVirtualHosts", str)
    check(scan, "rolloverType", str)
    check(scan, "status", str)
    check(scan, "createdTime", str)
    check(scan, "modifiedTime", str)
    check(scan, "reports", list)
    check(scan, "assets", list)
    check(scan, "numDependents", str)
    check(scan, "schedule", dict)
    check(scan["schedule"], "id", str)
    check(scan["schedule"], "type", str)
    check(scan["schedule"], "start", str)
    check(scan["schedule"], "repeatRule", str)
    check(scan["schedule"], "nextRun", int)
    check(scan, "policy", dict)
    check(scan["policy"], "id", str)
    check(scan["policy"], "name", str)
    check(scan["policy"], "description", str)
    check(scan, "policyPrefs", list)
    check(scan, "repository", dict)
    check(scan["repository"], "id", str)
    check(scan["repository"], "name", str)
    check(scan["repository"], "description", str)
    check(scan, "ownerGroup", dict)
    check(scan["ownerGroup"], "id", str)
    check(scan["ownerGroup"], "name", str)
    check(scan["ownerGroup"], "description", str)
    check(scan, "creator", dict)
    check(scan["creator"], "id", str)
    check(scan["creator"], "username", str)
    check(scan["creator"], "firstname", str)
    check(scan["creator"], "lastname", str)
    check(scan, "owner", dict)
    check(scan["owner"], "id", str)
    check(scan["owner"], "username", str)
    check(scan["owner"], "firstname", str)
    check(scan["owner"], "lastname", str)


@pytest.mark.vcr()
def test_scans_launch(security_center, scan):
    """
    test scans launch for success
    """
    launch = security_center.scans.launch(
        int(scan["id"]), diagnostic_target="target", diagnostic_password="password"
    )
    assert isinstance(launch, dict)
    check(launch, "scanID", str)
    check(launch, "scanResult", dict)
    check(launch["scanResult"], "initiatorID", str)
    check(launch["scanResult"], "ownerID", str)
    check(launch["scanResult"], "scanID", str)
    check(launch["scanResult"], "repositoryID", str)
    check(launch["scanResult"], "jobID", str)
    check(launch["scanResult"], "name", str)
    check(launch["scanResult"], "description", str, allow_none=True)
    check(launch["scanResult"], "details", str)
    check(launch["scanResult"], "status", str)
    check(launch["scanResult"], "downloadFormat", str)
    check(launch["scanResult"], "dataFormat", str)
    check(launch["scanResult"], "id", str)
