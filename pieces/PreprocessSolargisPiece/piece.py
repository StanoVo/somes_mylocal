from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import pandas as pd
import numpy as np
from pathlib import Path


class PreprocessSolargisPiece(BasePiece):
    
    def piece_function(self, input_data: InputModel):

        print(f"[INFO] Preprocessing {input_data.input_path} → {input_data.output_path}")
    
        # Load data
        df = pd.read_csv(input_data.input_path, sep=';', parse_dates={'datetime': ['Date', 'Time']}, dayfirst=True)
        df['datetime'] = pd.to_datetime(df['datetime'], format='%d.%m.%Y %H:%M')
    
        # Filter out night hours
        original_rows = len(df)
        df = df[df['GHI'] > 1].copy()
    
        # Feature engineering for CIS panels
        df['diffuse_fraction'] = np.where(df['GHI'] > 0, df['DIF'] / df['GHI'], 0)
        df['solar_elevation_sin'] = np.sin(np.radians(df['SE']))
        df['hour_of_day'] = df['datetime'].dt.hour
    
        # Save processed data
        output_data_file = Path(input_data.output_path) 
        df.to_csv(output_data_file, index=False)
        processed_rows = len(df)
    
        message = f"[SUCCESS] Preprocessed data saved to {input_data.output_path}"
        print(message)
        
        # Set display result
        self.display_result = {
            "file_type": "csv",
            "file_path": str(output_data_file)
        }
    
        return OutputModel(
            message = message,
            processed_rows = processed_rows,
            file_path = str(output_data_file)
        )

# import pandas as pd
# import numpy as np
# import os
# from models import InputModel, OutputModel

# def main(input_model: InputModel) -> OutputModel:
#     print(f"[INFO] Preprocessing {input_model.input_path} → {input_model.output_path}")
    
#     # Load data
#     df = pd.read_csv(input_model.input_path, sep=';', parse_dates={'datetime': ['Date', 'Time']}, dayfirst=True)
#     df['datetime'] = pd.to_datetime(df['datetime'], format='%d.%m.%Y %H:%M')
    
#     # Filter out night hours
#     original_rows = len(df)
#     df = df[df['GHI'] > 1].copy()
    
#     # Feature engineering for CIS panels
#     df['diffuse_fraction'] = np.where(df['GHI'] > 0, df['DIF'] / df['GHI'], 0)
#     df['solar_elevation_sin'] = np.sin(np.radians(df['SE']))
#     df['hour_of_day'] = df['datetime'].dt.hour
    
#     # Save processed data
#     os.makedirs(os.path.dirname(input_model.output_path), exist_ok=True)
#     df.to_csv(input_model.output_path, index=False)
#     processed_rows = len(df)
    
#     print(f"[SUCCESS] Preprocessed data saved to {input_model.output_path}")
    
#     return OutputModel(
#         message=f"Preprocessed {original_rows} rows to {processed_rows} rows",
#         processed_rows=processed_rows,
#         output_file=input_model.output_path
#     )

# if __name__ == "__main__":
#     # For testing purposes
#     input_data = InputModel(
#         input_path="/mnt/artifacts/raw_data.csv",
#         output_path="/mnt/artifacts/processed_data.csv"
#     )
#     result = main(input_data)
#     print(result)