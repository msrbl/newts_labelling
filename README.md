# SBER Reindeintification of Newts

This repository contains the **newts_labelling** project which provides tools for processing and labeling newt datasets. The project includes workflows for:
- Loading raw archives.
- Resizing images and COCO-format annotations.
- Running data pipelines using Prefect for orchestration.

## Project Structure

```
newts_labelling/
├── src/
│   ├── config.py                  # Configuration file with constants (e.g., SCALE, folder IDs)
│   ├── data_io/
│   │   ├── __init__.py
│   │   ├── drive/
│   │   │   ├── drive_manager.py   # Functions to manage Google Drive operations
│   │   ├── gdrive_raw.py          # Functions for listing and downloading files from Google Drive
│   │   └── resize_images.py       # Image resizing and annotation transformation functions
│   ├── flows/
│   │   ├── __init__.py
│   │   └── start_flow.py          # Entry point for pipelines using Prefect
│   └── temp.py                    # Temporary file for testing flows and functions
├── prefect.yaml                   # Prefect deployment configuration file
├── requirements.txt               # Project dependencies
└── README.md
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd newts_labelling
   ```

2. **Create and activate a Conda environment (or use your preferred environment manager):**

   ```bash
   conda create --name newts_labelling python=3.11
   conda activate newts_labelling
   ```

3. **Install the project dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

- Update the configuration in `src/config.py` with appropriate values for your environment (such as `DATA_SCALING_FACTOR`, `RAW_FOLDER_ID`, and `PROCESSED_FOLDER_ID`).
- For Google Drive operations, ensure you have the proper credentials (service account or OAuth configuration) in place.

## Running the Flow

The project uses [Prefect](https://www.prefect.io/) to orchestrate the data processing pipelines.

1. **Run a Prefect agent (if not already running):**

   ```bash
   prefect agent start -q default
   ```

2. **Deploy and run the flow:**

   The deployment is defined in `prefect.yaml`. Since the deployment entrypoint is `flows.start_flow`, run the flow using the full format:
   
   ```bash
   prefect deployment run start_flow/dlc_pipeline
   ```

   Alternatively, if adjustments were made to the entrypoint name, use the corresponding `<FLOW_NAME>/<DEPLOYMENT_NAME>` format.

## Usage Examples

- **Run Image Resizing:**

  Within your project, you can trigger image resizing (and annotation scaling) from a script or an interactive session:

  ```python
  from pathlib import Path
  from src.data_io.resize_images import resize_dataset, resize_annotations

  ds_name = "my_dataset"
  ds_dir = Path("data/raw/my_dataset")  # adjust the path as needed

  resize_dataset(ds_name, ds_dir)
  resize_annotations(ds_name, ds_dir)
  ```

## Contributing

Feel free to fork the repository and submit pull requests for improvements or bug fixes. Make sure to adhere to the code style and add tests for major changes.

## License

Include licensing information here if applicable.