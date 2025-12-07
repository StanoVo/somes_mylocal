from pydantic import BaseModel, Field

class InputModel(BaseModel):
    """
    Train XGBoost Piece Input Model
    """
    data_path: str = Field(
        title="Path to preprocessed data file",
        default='/home/shared_storage/data/processed_solargis.csv',
        description="The path to preprocessed Solargis data file"
    )   
    model_out: str = Field(
        title="Path to model file",
        default='/home/shared_storage/data/model.pkl',
        description="The path to Model file"
    )
    log_out: str = Field(
        title="Path to model training log file",
        default='/home/shared_storage/data/training_log.txt',
        description="The path to training log file"
    )

class OutputModel(BaseModel):
    """
    Train XGBoost Piece Output Model
    """
    message: str = Field(
        default="",
        description="Output message to log"
    )
    model_file_path: str = Field(
        description="The path to the model file"
    )
    train_log_path: str= Field(
        description="The path to the training log file"
    )