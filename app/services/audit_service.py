from sqlalchemy.orm import Session
from app.models.audit import AuditEvent

def log_event(
    db: Session,
    action: str,
    actor_id: int = None,
    resource_type: str = None,
    resource_id: int = None,
    ip_address: str = None
):
    event = AuditEvent(
        actor_id=actor_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=ip_address
    )
    db.add(event)
    db.commit()