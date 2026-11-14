
from app.models import PropertyManager, ScreeningReport, Property, Tenant


def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:
    """
    Check whether a PropertyManager can access a screening report.

    Access is allowed only when the report's tenant belongs to a
    property under the manager's landlord account.
    """

    tenant = next(
        (t for t in tenants if t.id == report.tenant_id),
        None
    )

    if tenant is None:
        return False

    property_record = next(
        (p for p in properties if p.id == tenant.property_id),
        None
    )

    if property_record is None:
        return False

    return property_record.landlord_account_id == actor.landlord_account_id
