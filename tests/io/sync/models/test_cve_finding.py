import pytest
from pydantic import ValidationError

from tenable.io.sync.models import cve_finding as c


def test_cve_str():
    class M(c.BaseModel):
        f: c.CVEStr

    assert M(f="CVE-2000-0001").model_dump() == {"f": "CVE-2000-0001"}

    with pytest.raises(ValidationError):
        M(f="a")


def test_cve_risk_list():
    obj = c.CVERisk(cves=["CVE-2000-0001" for _ in range(555)])
    assert obj.model_dump(mode="json") == {"cves": ["CVE-2000-0001"]}

    with pytest.raises(ValidationError):
        c.CVERisk(cves=["a"])

    obj2 = c.CVERisk(cves=[f"CVE-2000-{i:04}" for i in range(55)]).model_dump(
        mode="json"
    )
    assert len(obj2["cves"]) == 55


def test_cve_severity_upper():
    assert c.CVESeverity(level="high").model_dump() == {"level": "HIGH"}
