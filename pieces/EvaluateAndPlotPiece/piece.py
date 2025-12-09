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
        
        metrics_file_path = str(Path(self.results_path) / "metrics.json")
        with open(metrics_file_path, "w") as f:
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
        plot_file_path = str(Path(self.results_path) / "comparison.png")
        plt.savefig(plot_file_path, dpi=150)
        plt.close()
        
        print(f"[SUCCESS] Evaluation complete. Metrics: MAE={mae:.4f}, R²={r2:.4f}")
        
        return OutputModel(
            message=f"Evaluation completed successfully",
            metrics_file_path=metrics_file_path,
            plot_file_path=plot_file_path,
            mae=mae,
            r2=r2
        )
