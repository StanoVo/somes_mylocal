from pydantic import BaseModel, Field
# from typing import Optional

class InputModel(BaseModel):
    model_path: str = Field(
        title="Path to model file",
        default='/home/shared_storage/data/model.pkl',
        description="The path to forecast model file"
    ) 
    metrics_path: str = Field(
        title="Path to metrics file",
        default='/home/shared_storage/data/metrics.json',
        description="The path to metrics file"
    )
    name: str = Field(
        title="Model name", 
        default="SolarForecastModel"
    ) 
    description: str = Field(
        title="Model description",
        default="XGBoost model for solar forecasting"
    )
class OutputModel(BaseModel):
    message: str = Field(
        default="",
        description="Output message to log"
    )
    model_version_id: str = Field(
        default="",
        description="Version ID of the registered model"
    )
    registry_url: str = Field(
        default="",
        description="The URL to the model registry entry"
    )