from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import pandas as pd
import joblib
import json
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, r2_score

class EvaluateAndPlotPiece(BasePiece):
    
    def piece_function(self, input_data: InputModel):

        print(f"[INFO] Evaluating model: {input_data.model_path}")
        
        # Load data and model
        df = pd.read_csv(input_data.data_path)
        model = joblib.load(input_data.model_path)
        
        # Prepare features and target
        features = ['GHI', 'DIF', 'TEMP', 'diffuse_fraction', 'solar_elevation_sin', 'hour_of_day']
        X = df[features]
        y_true = df['PVOUT']
        
        # Predict
        y_pred = model.predict(X)
        
        # Calculate metrics
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        # Save metrics
        metrics = {
            "MAE_kW": round(mae, 4),
            "R2": round(r2, 4),
            "samples": len(y_true)            
        }
        
        with open(input_data.metrics_out, "w") as f:
            json.dump(metrics, f, indent=2)
        
        # Plot comparison        
        plt.figure(figsize=(12, 5))
        plt.plot(y_true.values, label="Solargis PVOUT", color="steelblue")
        plt.plot(y_pred, '--', label="XGBoost prediction", color="crimson")
        plt.title(f"XGBoost vs Solargis (MAE={mae:.3f} kW, R²={r2:.3f})")
        plt.xlabel("Time index (15-min steps)")
        plt.ylabel("Power (kW)")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(input_data.plot_out, dpi=150)
        plt.close()
        
        print(f"[SUCCESS] Evaluation complete. Metrics: MAE={mae:.4f}, R²={r2:.4f}")
        
        return OutputModel(
            message=f"Evaluation completed successfully",
            metrics_file=input_data.metrics_out,
            plot_file=input_data.plot_out,
            mae=mae,
            r2=r2
        )


# import pandas as pd
# import joblib
# import json
# import matplotlib.pyplot as plt
# import os
# from sklearn.metrics import mean_absolute_error, r2_score
# from models import InputModel, OutputModel

# def main(input_data: InputModel) -> OutputModel:
#     print(f"[INFO] Evaluating model: {input_data.model_path}")
    
#     # Load data and model
#     df = pd.read_csv(input_data.data_path)
#     model = joblib.load(input_data.model_path)
    
#     # Prepare features and target
#     features = ['GHI', 'DIF', 'TEMP', 'diffuse_fraction', 'solar_elevation_sin', 'hour_of_day']
#     X = df[features]
#     y_true = df['PVOUT']
    
#     # Predict
#     y_pred = model.predict(X)
    
#     # Calculate metrics
#     mae = mean_absolute_error(y_true, y_pred)
#     r2 = r2_score(y_true, y_pred)
    
#     # Save metrics
#     metrics = {
#         "MAE_kW": round(mae, 4),
#         "R2": round(r2, 4),
#         "samples": len(y_true)
#     }
#     os.makedirs(os.path.dirname(input_data.metrics_out), exist_ok=True)
#     with open(input_data.metrics_out, "w") as f:
#         json.dump(metrics, f, indent=2)
    
#     # Plot comparison
#     os.makedirs(os.path.dirname(input_data.plot_out), exist_ok=True)
#     plt.figure(figsize=(12, 5))
#     plt.plot(y_true.values, label="Solargis PVOUT", color="steelblue")
#     plt.plot(y_pred, '--', label="XGBoost prediction", color="crimson")
#     plt.title(f"XGBoost vs Solargis (MAE={mae:.3f} kW, R²={r2:.3f})")
#     plt.xlabel("Time index (15-min steps)")
#     plt.ylabel("Power (kW)")
#     plt.legend()
#     plt.grid(alpha=0.3)
#     plt.tight_layout()
#     plt.savefig(input_data.plot_out, dpi=150)
#     plt.close()
    
#     print(f"[SUCCESS] Evaluation complete. Metrics: MAE={mae:.4f}, R²={r2:.4f}")
    
#     return OutputModel(
#         message=f"Evaluation completed successfully",
#         metrics_file=input_data.metrics_out,
#         plot_file=input_data.plot_out,
#         mae=mae,
#         r2=r2
#     )

# if __name__ == "__main__":
#     # For testing purposes
#     input_data = InputModel(
#         data_path="/mnt/artifacts/processed_data.csv",
#         model_path="/mnt/artifacts/model.pkl",
#         metrics_out="/mnt/artifacts/metrics.json",
#         plot_out="/mnt/artifacts/comparison.png"
#     )
#     result = main(input_data)
#     print(result)