from pydantic import BaseModel, Field

class InputModel(BaseModel):
    data_path: str = Field(
        title="Path to data file",
        #default='/home/shared_storage/data/DataForComparison.csv',
        description="The path to data file for prediction"
    ) 
    model_path: str = Field(
        title="Path to model file",
        #default='/home/shared_storage/data/model.pkl',
        description="The path to forecast model file"
    ) 

class OutputModel(BaseModel):
    message: str= Field(
        default="",
        description="Output message to log"
    )
    metrics_file_path: str= Field(
        default="",
        description="The path to the metrics json file"
    )
    plot_file_path: str= Field(
        default="",
        description="The path to the graphical comparison output file"
    )
    mae: float
    r2: float