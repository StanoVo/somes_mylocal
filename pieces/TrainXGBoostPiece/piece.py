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
        model_path = str(Path(self.results_path) / "model.pkl")
        joblib.dump(model, model_path)

        print(f"[SUCCESS] Model saved to {model_path}")
        
        # Save training log
        log_path = str(Path(self.results_path) / "training.log")
        with open(log_path, "w") as f:
            f.write(f"Model trained at {pd.Timestamp.now()}")
        
        message=f"Model trained and saved successfully to {model_path} and log to {log_path}"
        print(message)

        return OutputModel(
            message=message,
            model_file_path=model_path,
            train_log_path=log_path
        )
