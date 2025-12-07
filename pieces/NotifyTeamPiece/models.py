from pydantic import BaseModel, Field
from typing import Optional

class InputModel(BaseModel):
    metrics_path: str = Field(
        title="Path to metrics file",
        default='/home/shared_storage/data/metrics.json',
        description="The path to metrics file"
    )
    webhook_url: Optional[str] = Field(
        title="Path to webhook url",
        default='',
        description="The path to webhook url for Slack notifications"
    )

class OutputModel(BaseModel):
    message: str= Field(
        default="",
        description="Output message to log"
    )
    notification_sent: bool
    recipients: str

# from pydantic import BaseModel
# from typing import Optional

# class InputModel(BaseModel):
#     metrics_path: str
#     webhook_url: Optional[str] = None

# class OutputModel(BaseModel):
#     message: str
#     notification_sent: bool
#     recipients: str