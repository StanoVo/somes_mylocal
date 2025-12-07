from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import pandas as pd
from pathlib import Path
from docx import Document
from glob import glob


class FetchSolargisDataPiece(BasePiece):
    
    def _read_docx_files(self, file_paths):
        """Extract data from DOCX files."""
        csv_data = []
        
        for doc_file in file_paths:
            if not doc_file.exists():
                print(f"[WARNING] File not found: {doc_file}")
                continue
                
            print(f"[INFO] Processing DOCX document: {doc_file}")
            doc = Document(doc_file)
            csv_started = False
        
            # Process each paragraph in the document
            for paragraph in doc.paragraphs:
                line = paragraph.text.strip()
                # Check if we've reached the CSV data section
                if "#Data:" in line:
                    csv_started = True
                    continue

                # If we're in the CSV section, store the line
                if csv_started and line:
                    csv_data.append(line)
        
        return csv_data
    
    def _read_csv_files(self, file_paths):
        """Read and concatenate data from CSV files."""
        dfs = []
        
        for csv_file in file_paths:
            if not csv_file.exists():
                print(f"[WARNING] File not found: {csv_file}")
                continue
                
            print(f"[INFO] Processing CSV file: {csv_file}")
            df = pd.read_csv(csv_file)
            dfs.append(df)
        
        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)
            return combined_df.values.tolist()
        return []
    
    def _resolve_file_paths(self, input_path_str, file_type):
        """Resolve wildcard patterns and return list of matching files."""
        input_path = Path(input_path_str)
        file_extension = '.docx' if file_type.lower() == 'docx' else '.csv'
        
        # Resolve wildcard patterns in input path
        if '*' in str(input_path) or '?' in str(input_path):
            # Handle wildcard patterns
            matching_files = glob(str(input_path))
            if not matching_files:
                return []
            files = [Path(f) for f in matching_files if f.endswith(file_extension)]
        else:
            # Check if it's a directory
            if input_path.is_dir():
                # If directory, find all files of specified type
                pattern = f'*{file_extension}'
                files = list(input_path.glob(pattern))
            else:
                # Single file
                files = [input_path]
        
        return files
    
    def piece_function(self, input_data: InputModel):

        print(f"[INFO] Fetching data from {input_data.input_path} → {input_data.output_path}")
        print(f"[INFO] File type: {input_data.input_filetype}")

        csv_data = []
        
        # Resolve file paths based on wildcards
        file_paths = self._resolve_file_paths(input_data.input_path, input_data.input_filetype)
        
        if not file_paths:
            message = f"No {input_data.input_filetype.upper()} files found at: {input_data.input_path}"
            print(f"[WARNING] {message}")
            return OutputModel(
                message=message,
                file_path=""
            )
        
        # Process files based on type
        if input_data.input_filetype.lower() == 'docx':
            csv_data = self._read_docx_files(file_paths)
        elif input_data.input_filetype.lower() == 'csv':
            csv_data = self._read_csv_files(file_paths)
        else:
            message = f"Unsupported file type: {input_data.input_filetype}"
            print(f"[ERROR] {message}")
            return OutputModel(
                message=message,
                file_path=""
            )

        # Convert to DataFrame and write to CSV
        if csv_data:
            df = pd.DataFrame(csv_data)
            message = f"Files processed successfully, {len(df)} rows found."
            print(f"[SUCCESS] {message}")
            output_data_file = Path(input_data.output_path) 
            #output_data_file.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_data_file, index=False, header=False)
            
        else:
            message = f"No data found in {input_data.input_filetype.upper()} files."
            print(f"[WARNING] {message}")
            output_data_file = None
            
        # Set display result
        self.display_result = {
            "file_type": "csv",
            "file_path": str(output_data_file) if csv_data else ""
        }

        # Return output
        return OutputModel(
            message=message,
            file_path=str(output_data_file) if csv_data else ""
        )

# import boto3
# import os
# from urllib.parse import urlparse
# from models import InputModel, OutputModel

# def main(input_model: InputModel) -> OutputModel:
#     print(f"[INFO] Fetching data from {input_model.s3_path} → {input_model.output_path}")
    
#     # Parse S3 path
#     parsed = urlparse(input_model.s3_path, allow_fragments=False)
#     if parsed.scheme == "s3":
#         bucket = parsed.netloc
#         key = parsed.path.lstrip('/')
        
#         # Initialize S3 client
#         s3 = boto3.client('s3')
        
#         # Create output directory if not exists
#         os.makedirs(os.path.dirname(input_model.output_path), exist_ok=True)
        
#         # Download file
#         s3.download_file(bucket, key, input_model.output_path)
#         print(f"[SUCCESS] Downloaded {input_model.s3_path}")
        
#         return OutputModel(
#             message=f"Successfully downloaded {input_model.s3_path}",
#             downloaded_file=input_model.output_path
#         )
#     else:
#         raise ValueError("Only S3 paths are supported")

# if __name__ == "__main__":
#     # For testing purposes
#     input_data = InputModel(
#         s3_path="s3://bucket/data.csv",
#         output_path="/mnt/artifacts/data.csv"
#     )
#     result = main(input_data)
#     print(result)