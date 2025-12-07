from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import pandas as pd
import joblib
import matplotlib.pyplot as plt

class RunSolarForecastPiece(BasePiece):
    
    def piece_function(self, input_data: InputModel):

        print(f"[INFO] Running forecast using model: {input_data.model_path}")
    
        # Load model
        model = joblib.load(input_data.model_path)
    
        # Load forecast features
        df = pd.read_csv(input_data.features_csv)
        features = ['GHI', 'DIF', 'TEMP', 'diffuse_fraction', 'solar_elevation_sin', 'hour_of_day']
        X = df[features]
    
        # Predict
        df['PVOUT_kW'] = model.predict(X)
    
        # Save forecast
        df[['datetime', 'PVOUT_kW']].to_csv(input_data.output_csv, index=False)
    
        # Plot
        plt.figure(figsize=(10, 4))
        plt.plot(df['datetime'], df['PVOUT_kW'], 'b-', label='Forecasted PV Output')
        plt.title('Next-Day Solar Generation Forecast')
        plt.xlabel('Time')
        plt.ylabel('Power (kW)')
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(input_data.output_plot)
        plt.close()
        
        print(f"[SUCCESS] Forecast saved to {input_data.output_csv}")
        
        return OutputModel(
            message=f"Forecast generated successfully",
            forecast_file=input_data.output_csv,
            plot_file=input_data.output_plot
        )

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