from __future__ import annotations
from typing import TYPE_CHECKING
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import json
import os

if TYPE_CHECKING:
    from domino import Model, ModelVersion

class RegisterModelPiece(BasePiece):
    
    def piece_function(self, input_data: InputModel):
        try:
            from domino import Model, ModelVersion
        except Exception:
            from .registry import Model, ModelVersion

        print(f"[INFO] Registering model: {input_data.name}")

        # Load metrics
        with open(input_data.metrics_path) as f:
            metrics = json.load(f)

        # Create/get model
        model = Model.get_or_create(name=input_data.name, description=input_data.description or "")

        # Register version
        version = ModelVersion.create(
            model=model,
            files=[input_data.model_path],
            metadata={
                "MAE_kW": metrics["MAE_kW"],
                "R2": metrics["R2"],
                "samples": metrics["samples"],
                "trained_at": os.getenv("DOMINO_RUN_START_TIME", "unknown")
            },
            description=f"Daily retrain {os.getenv('DOMINO_RUN_START_TIME', 'unknown')}"
        )

        registry_url = f"https://your-domino-url/models/{model.id}/versions/{version.id}"

        print(f"[SUCCESS] Model registered. Version ID: {version.id}")

        return OutputModel(
            message=f"Model registered successfully with version {version.id}",
            model_version_id=version.id,
            registry_url=registry_url
        )

# import json
# import os
# from domino import Model, ModelVersion
# from models import InputModel, OutputModel

# def main(input_model: InputModel) -> OutputModel:
#     print(f"[INFO] Registering model: {input_model.name}")
    
#     # Load metrics
#     with open(input_model.metrics_path) as f:
#         metrics = json.load(f)
    
#     # Create/get model
#     model = Model.get_or_create(name=input_model.name, description=input_model.description or "")
    
#     # Register version
#     version = ModelVersion.create(
#         model=model,
#         files=[input_model.model_path],
#         metadata={
#             "MAE_kW": metrics["MAE_kW"],
#             "R2": metrics["R2"],
#             "samples": metrics["samples"],
#             "trained_at": os.getenv("DOMINO_RUN_START_TIME", "unknown")
#         },
#         description=f"Daily retrain {os.getenv('DOMINO_RUN_START_TIME', 'unknown')}"
#     )
    
#     registry_url = f"https://your-domino-url/models/{model.id}/versions/{version.id}"
    
#     print(f"[SUCCESS] Model registered. Version ID: {version.id}")
    
#     return OutputModel(
#         message=f"Model registered successfully with version {version.id}",
#         model_version_id=version.id,
#         registry_url=registry_url
#     )

# if __name__ == "__main__":
#     # For testing purposes
#     input_data = InputModel(
#         model_path="/mnt/artifacts/model.pkl",
#         metrics_path="/mnt/artifacts/metrics.json",
#         name="SolarForecastModel",
#         description="XGBoost model for solar forecasting"
#     )
#     result = main(input_data)
#     print(result)