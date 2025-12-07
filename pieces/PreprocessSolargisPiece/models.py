from pydantic import BaseModel, Field

class InputModel(BaseModel):
    """
    Preprocess Solargis Data Piece Input Model
    """
    input_path: str = Field(
        title="Path to raw data file",
        default='/home/shared_storage/data/raw_solargis.csv',
        description="The path to the input Solargis raw data file "
    )    

    output_path: str = Field(
        title="Path to output data file",
        default='/home/shared_storage/data/processed_solargis.csv',
        description="The path to the output processed Solargis data file"
    )

class OutputModel(BaseModel):
    message: str = Field(
        default="",
        description="Output message to log"
    )
      
    file_path: str = Field(
        description="The path to the output CSV file"
    )
    
    processed_rows: int
    