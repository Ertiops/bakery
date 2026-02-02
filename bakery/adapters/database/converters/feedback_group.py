from bakery.adapters.database.tables import FeedbackGroupTable
from bakery.domains.entities.feedback_group import FeedbackGroup


def convert_feedback_group(*, result: FeedbackGroupTable) -> FeedbackGroup:
    return FeedbackGroup(
        id=result.id,
        url=result.url,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
