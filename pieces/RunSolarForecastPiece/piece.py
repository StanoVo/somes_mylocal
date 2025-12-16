from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

class RunSolarForecastPiece(BasePiece):
    
    def piece_function(self, input_data: InputModel):

        print(f"[INFO] Running forecast using model: {input_data.model_path}")
    
        # Load model
        model = joblib.load(input_data.model_path)
    
        # Load forecast features
        df = pd.read_csv(input_data.features_csv)
        features = ['GHI', 'DIF', 'TEMP', 'diffuse_fraction', 'solar_elevation_sin', 'hour_of_day']
        X = df[features]
        y_true = df['PVOUT']
    
        # Predict
        y_pred = model.predict(X)
        df['PVOUT_kW'] = y_pred
    
        # Save forecast
        forecast_file_path = str(Path(self.results_path) / "solar_forecast.csv")
        df[['datetime', 'PVOUT', 'PVOUT_kW']].to_csv(forecast_file_path, index=False)

        print(f"[SUCCESS] Forecast saved to {forecast_file_path}")
    
        # Plot comparison        
        plt.figure(figsize=(12, 5))
        plt.plot(y_true.values, label="Solargis PVOUT", color="steelblue")
        plt.plot(y_pred, '--', label="XGBoost prediction", color="crimson")
        plt.title(f"XGBoost vs Solargis Forecast")
        plt.xlabel("Time index (15-min steps)")
        plt.ylabel("Power (kW)")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()        
        plot_file_path = str(Path(self.results_path) / "comparison.png")
        plt.savefig(plot_file_path, dpi=150)
        plt.close()
        
        print(f"[SUCCESS] Comparison forecast saved to {plot_file_path}")

        self.display_result = {
            "file_type": "png",
            "file_path": plot_file_path
        }
               
        return OutputModel(
            message=f"Forecast generated successfully",
            forecast_file=forecast_file_path,
            plot_file=plot_file_path
        )
    # def piece_function(self, input_data: InputModel):

    #     print(f"[INFO] Running forecast using model: {input_data.model_path}")
    
    #     # Load model
    #     model = joblib.load(input_data.model_path)
    
    #     # Load forecast features
    #     df = pd.read_csv(input_data.features_csv)
    #     features = ['GHI', 'DIF', 'TEMP', 'diffuse_fraction', 'solar_elevation_sin', 'hour_of_day']
    #     X = df[features]
    
    #     # Predict
    #     df['PVOUT_kW'] = model.predict(X)
    
    #     # Save forecast
    #     forecast_file_path = str(Path(self.results_path) / "solar_forecast.csv")
    #     df[['datetime', 'PVOUT_kW']].to_csv(forecast_file_path, index=False)

    #     print(f"[SUCCESS] Forecast saved to {forecast_file_path}")
    
    #     # Plot
    #     plt.figure(figsize=(10, 4))
    #     plt.plot(df['datetime'], df['PVOUT_kW'], 'b-', label='Forecasted PV Output')
    #     plt.title('Next-Days Solar Generation Forecast')
    #     plt.xlabel('Time')
    #     plt.ylabel('Power (kW)')
    #     plt.xticks(rotation=45)
    #     plt.grid(alpha=0.3)
    #     plt.tight_layout()
    #     plot_file_path = str(Path(self.results_path) / "solar_forecast.png")
    #     plt.savefig(plot_file_path)
    #     plt.close()
        
    #     print(f"[SUCCESS] Comparison forecast saved to {plot_file_path}")
               
    #     return OutputModel(
    #         message=f"Forecast generated successfully",
    #         forecast_file=forecast_file_path,
    #         plot_file=plot_file_path
    #     )
