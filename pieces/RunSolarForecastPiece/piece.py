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
# Below is an alternative standalone script version of the same logic.
# import pandas as pd
# import joblib
# import matplotlib.pyplot as plt
# import os
# from models import InputModel, OutputModel

# def main(input_model: InputModel) -> OutputModel:
#     print(f"[INFO] Running forecast using model: {input_model.model_path}")
    
#     # Load model
#     model = joblib.load(input_model.model_path)
    
#     # Load forecast features
#     df = pd.read_csv(input_model.features_csv)
#     features = ['GHI', 'DIF', 'TEMP', 'diffuse_fraction', 'solar_elevation_sin', 'hour_of_day']
#     X = df[features]
    
#     # Predict
#     df['PVOUT_kW'] = model.predict(X)
    
#     # Save forecast
#     os.makedirs(os.path.dirname(input_model.output_csv), exist_ok=True)
#     df[['datetime', 'PVOUT_kW']].to_csv(input_model.output_csv, index=False)
    
#     # Plot
#     os.makedirs(os.path.dirname(input_model.output_plot), exist_ok=True)
#     plt.figure(figsize=(10, 4))
#     plt.plot(df['datetime'], df['PVOUT_kW'], 'b-', label='Forecasted PV Output')
#     plt.title('Next-Day Solar Generation Forecast')
#     plt.xlabel('Time')
#     plt.ylabel('Power (kW)')
#     plt.xticks(rotation=45)
#     plt.grid(alpha=0.3)
#     plt.tight_layout()
#     plt.savefig(input_model.output_plot)
#     plt.close()
    
#     print(f"[SUCCESS] Forecast saved to {input_model.output_csv}")
    
#     return OutputModel(
#         message=f"Forecast generated successfully",
#         forecast_file=input_model.output_csv,
#         plot_file=input_model.output_plot
#     )

# if __name__ == "__main__":
#     # For testing purposes
#     input_data = InputModel(
#         model_path="/mnt/artifacts/model.pkl",
#         features_csv="/mnt/artifacts/weather_features.csv",
#         output_csv="/mnt/artifacts/forecast.csv",
#         output_plot="/mnt/artifacts/forecast.png"
#     )
#     result = main(input_data)
#     print(result)