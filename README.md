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
│   ├── deeplabcut/
│   │   ├── __init__.py
│   │   ├── pipeline.py            # Preprocess images and annotations for DeepLabCut projects
│   │   └── parse_labels.py        # Parse and format labeling information for analysis
│   └── utils/                     # Utility scripts and helper functions
├── tests/                        # Unit and integration tests
├── requirements.txt              # Project dependencies
└── README.md
```

## Detailed Workflows

- Loading Raw Dataset Archives  
  The pipeline automatically searches specified Google Drive folders using the ID set in environment variables. It downloads and extracts raw datasets for further processing.

- Resizing Images and Annotations  
  Using the defined scaling factor in `src/config.py`, images and their corresponding COCO annotations are resized. The coordinate adjustments are handled in `resize_images.py`.

- Generating DeepLabCut Project  
  This feature prepares the dataset for a DeepLabCut project by converting annotations and setting up directory structures as defined in `src/deeplabcut/pipeline.py`.

- Prefect Orchestration  
  The Prefect flow defined in `src/flows/start_flow.py` orchestrates the entire pipeline, ensuring that extraction, processing, and project generation are executed in the correct sequence.

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

- Set the enviromnent variables `DRIVE_RAW_FOLDER_ID` and `DRIVE_PROCESSED_FOLDER_ID` to specify the Google Drive folder from which the raw .tar datasets will be taken, and the folder where the finished reformatted datasets will be uploaded.
- You can update the configuration of `DATA_SCALING_FACTOR` in `src/config.py` with appropriate values.
- For Google Drive operations, ensure you have the proper credentials (service account or OAuth configuration) in place.

## Usage Examples

- **Run Image Resizing:**



  ```bash
  python -m src.flows.start_flow
  ```