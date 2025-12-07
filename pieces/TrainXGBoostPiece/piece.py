from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import pandas as pd
from pathlib import Path
import joblib
import os
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

class TrainXGBoostPiece(BasePiece):
    
    def piece_function(self, input_data: InputModel):

        print(f"[INFO] Training model using data: {input_data.data_path}")
        
        # Load data
        df = pd.read_csv(input_data.data_path)
        features = ['GHI', 'DIF', 'TEMP', 'diffuse_fraction', 'solar_elevation_sin', 'hour_of_day']
        X = df[features]
        y = df['PVOUT']
        
        # Train model
        model = XGBRegressor(
            objective='reg:squarederror',
            learning_rate=0.05,
            max_depth=3,
            n_estimators=250
        )
        model.fit(X, y)
        
        # Save model
        joblib.dump(model, input_data.model_out)

        print(f"[SUCCESS] Model saved to {input_data.model_out}")
        
        # Save training log
        with open(input_data.log_out, "w") as f:
            f.write(f"Model trained at {pd.Timestamp.now()}")
        
        message=f"Model trained and saved successfully to {input_data.model_out}"
        print(message)

        return OutputModel(
            message=message,
            model_file_path=input_data.model_out,
            train_log_path=input_data.log_out
        )

# import pandas as pd
# import joblib
# import os
# from sklearn.metrics import mean_absolute_error, r2_score
# from xgboost import XGBRegressor
# from models import InputModel, OutputModel

# def evaluate(model_path, test_data_path):
#     model = joblib.load(model_path)
#     df = pd.read_csv(test_data_path)
#     X_test = df.drop(columns=['PVOUT'])
#     y_test = df['PVOUT']
    
#     pred = model.predict(X_test)
#     mae = mean_absolute_error(y_test, pred)
#     r2 = r2_score(y_test, pred)
    
#     return {"MAE": mae, "R2": r2}

# def main(input_model: InputModel) -> OutputModel:
#     print(f"[INFO] Training model using data: {input_model.data_path}")
    
#     # Load data
#     df = pd.read_csv(input_model.data_path)
#     features = ['GHI', 'DIF', 'TEMP', 'diffuse_fraction', 'solar_elevation_sin', 'hour_of_day']
#     X = df[features]
#     y = df['PVOUT']
    
#     # Train model
#     model = XGBRegressor(
#         objective='reg:squarederror',
#         learning_rate=0.05,
#         max_depth=3,
#         n_estimators=250
#     )
#     model.fit(X, y)
    
#     # Save model
#     os.makedirs(os.path.dirname(input_model.model_out), exist_ok=True)
#     joblib.dump(model, input_model.model_out)
    
#     # Save training log
#     os.makedirs(os.path.dirname(input_model.log_out), exist_ok=True)
#     with open(input_model.log_out, "w") as f:
#         f.write(f"Model trained at {pd.Timestamp.now()}")
    
#     print(f"[SUCCESS] Model saved to {input_model.model_out}")
    
#     return OutputModel(
#         message=f"Model trained and saved successfully",
#         model_file=input_model.model_out,
#         training_log=input_model.log_out
#     )

# if __name__ == "__main__":
#     # For testing purposes
#     input_data = InputModel(
#         data_path="/mnt/artifacts/processed_data.csv",
#         model_out="/mnt/artifacts/model.pkl",
#         log_out="/mnt/artifacts/training.log"
#     )
#     result = main(input_data)
#     print(result)