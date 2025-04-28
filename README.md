# SBER Reindeintification of Newts

This repository contains the **newts_labelling** project which provides tools for processing and labeling newt datasets. The project includes workflows for:
- Loading raw dataset archives: Automatically locating and extracting raw .tar files from designated folders.
- Resizing images and COCO-format annotations: Standardizing image sizes and updating annotation coordinates.
- Generating DeepLabCut project: Preprocessing images and annotations to initialize a DeepLabCut analysis project.
- Running data pipelines using Prefect for orchestration: Coordinating the overall workflow through scheduled tasks and dependency management.

## Project Structure

```
newts_labelling/
├── docs/                         # Documentation files and project notes
├── data/                         # Raw and processed dataset files
├── src/
│   ├── config.py                 # Configuration file with constants
│   ├── services/                 # Additional logic scripts to handle drive and files operations
│   │   ├── __init__.py
│   │   ├── drive/
│   │   │   ├── credentials.json  # Contains Google Drive API credentials for authentication.
│   │   │   └── drive_manager.py     # Module for handling Google Drive operations.
│   │   ├── merge_files.py        # Merging instance JSONs and images
│   │   └── resize_dataset.py     # Image resizing and annotation transformation
│   ├── flows/                    # Prefect flows for orchestration
│   │   ├── __init__.py
│   │   ├── upload_datasets.py    # Upload processed datasets to Google Drive
│   │   ├── download_raw_archives.py  # Download and extract raw archives
│   │   ├── aggregate_datasets.py     # Aggregate and resize raw datasets
│   │   └── init_dlc_project.py         # Initialize DeepLabCut project
│   ├── deeplabcut/              # DeepLabCut related modules
│   │   ├── __init__.py
│   │   └── labels.py            # Handling label extraction & CSV creation
│   ├── utils/                   # Utility modules and helper functions
│   │   ├── __init__.py
│   │   └── file_utils.py        # Common file handling functions
│   └── main.py                  # Orchestration entry point (alternative to start_flow.py)
├── tests/                       # Unit and integration tests
├── requirements.txt             # Project dependencies
└── README.md
```

## Detailed Workflows

- **Download and Extraction:**  
  The "download_raw_archives" flow locates new raw .tar archives from the designated Google Drive folder, downloads them, unpacks the contents, and collates files into a standard structure.

- **Aggregation and Resizing:**  
  The "aggregate_datasets" flow processes the raw dataset by aggregating subfolder files and resizing images while adjusting COCO annotations based on the defined scaling factor.

- **Upload Processed Datasets:**  
  The "upload_datasets" flow packs the processed datasets into tar archives and uploads them back to a specified Google Drive folder.

- **DeepLabCut Project Initialization:**  
  The "init_dlc_project" flow creates a DeepLabCut project using the processed datasets. It automatically extracts frames, fills in labeling data, updates the configuration, and packages the project.

- **Prefect Orchestration:**  
  The main pipeline flow (defined in `src/main.py`) orchestrates all the stages sequentially—from downloading to project initialization.

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

- Set the environment variables `DRIVE_RAW_FOLDER_ID` and `DRIVE_PROCESSED_FOLDER_ID` to specify the Google Drive folders for raw and processed datasets.
- Adjust the scaling factor `DATA_SCALING_FACTOR` in `src/config.py` as needed.
- Ensure that correct Google Drive credentials (service account) in the `credentials.json` file is located in the `src/services/drive` directory and available in `src/services/drive/drive_manager.py`.

## Usage

- **Run the Full Pipeline:**  
  To process datasets, generate DeepLabCut projects, and upload results, run:
  ```bash
  python -m src.main
  ```

- **Starting Individual Flows:**  
  Every flow can be easily started by running:
  ```bash
  python -m src.flows.<flow_name>
  ```
  For example:
  - `python -m src.flows.download_raw_archives`
  - `python -m src.flows.aggregate_datasets`
  - `python -m src.flows.upload_datasets`
  - `python -m src.flows.init_dlc_project`
  
## Using Docker

Before running the container, build the Docker image:
```bash
docker build -t <image-name> .
```
Then run the container by specifying the required environment variables:
```bash
docker run -e DRIVE_RAW_FOLDER_ID="your_drive_raw_folder_id" -e DRIVE_PROCESSED_FOLDER_ID="your_drive_processed_folder_id" <image-name>
```

## Troubleshooting

- Verify that the environment variables `DRIVE_RAW_FOLDER_ID` and `DRIVE_PROCESSED_FOLDER_ID` are correctly set.
- Ensure that your Google Drive credentials (`credentials.json`) are placed in the `src/data_io/drive` folder.
- Check the logs output by Prefect for hints on failed tasks.

## Contributing

Contributions are welcome! Please follow these steps:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Submit a pull request with a clear description of your changes.