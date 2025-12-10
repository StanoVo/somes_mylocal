from pydantic import BaseModel, Field

class InputModel(BaseModel):
    model_path: str = Field(
        title="Path to model file",
        #default='/home/shared_storage/data/model.pkl',
        description="The path to forecast model file"
    ) 
    features_csv: str = Field(
        title="Path to features CSV file",
        #default='/home/shared_storage/data/forecast_features.csv',
        description="The path to CSV file containing features for forecast"
    )

class OutputModel(BaseModel):
    message: str = Field(
        default="",
        description="Output message to log"
    )
    forecast_file: str = Field(
        default="",
        description="The path to the forecast CSV output file"
    )
    plot_file: str = Field(
        default="",
        description="The path to the graphical comparison output file"
    )