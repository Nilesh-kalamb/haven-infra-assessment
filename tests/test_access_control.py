
from app.access_control import can_access_screening_report


def test_pm_cannot_access_other_property_report(
    property_managers, properties, tenants, screening_reports
):
    pm = next(pm for pm in property_managers if pm.id == "pm-001")
    report = next(r for r in screening_reports if r.id == "rep-002")

    assert can_access_screening_report(
        pm, report, properties=properties, tenants=tenants
    ) is False


def test_pm_can_access_own_property_report(
    property_managers, properties, tenants, screening_reports
):
    pm = next(pm for pm in property_managers if pm.id == "pm-001")
    report = next(r for r in screening_reports if r.id == "rep-001")

    assert can_access_screening_report(
        pm, report, properties=properties, tenants=tenants
    ) is True
