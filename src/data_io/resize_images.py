import json
from pathlib import Path
import cv2
from joblib import Parallel, delayed

from src.config import DATA_SCALING_FACTOR

def _resize_one(src_path: Path, dst_root: Path):
    img = cv2.imread(str(src_path), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Failed to read {src_path}")
    h, w = img.shape[:2]
    img_small = cv2.resize(img, (int(w * DATA_SCALING_FACTOR), int(h * DATA_SCALING_FACTOR)),
                           interpolation=cv2.INTER_AREA)
    dst = dst_root / src_path.name
    cv2.imwrite(str(dst), img_small, [cv2.IMWRITE_JPEG_QUALITY, 95])

def _resize_annotations(annotations_dir: Path, annotation_dst_dir: Path):
    """
    Reads COCO format annotations from the annotations folder of the dataset,
    scales down coordinate values by SCALE, and saves to the corresponding
    processed folder.
    """
    file_name = "instances.json"

    annotation_file = annotations_dir / file_name
    if not annotation_file.exists():
        print(f"Annotation file not found: {annotation_file}")
        raise FileNotFoundError(f"Annotation file not found: {annotation_file}")

    with open(annotation_file, "r", encoding="utf-8") as f:
        coco_data = json.load(f)
    
    for image in coco_data.get("images", []):
        image["width"] = int(image["width"] * DATA_SCALING_FACTOR)
        image["height"] = int(image["height"] * DATA_SCALING_FACTOR)
    
    for ann in coco_data.get("annotations", []):
        bbox = ann.get("bbox")
        if bbox:
            ann["bbox"] = [coord * DATA_SCALING_FACTOR for coord in bbox]

        if "segmentation" in ann and isinstance(ann["segmentation"], list):
            ann["segmentation"] = [
                [coord * DATA_SCALING_FACTOR for coord in seg] for seg in ann["segmentation"]
            ]
    
    dst_annotation_file = annotation_dst_dir / file_name
    with open(dst_annotation_file, "w", encoding="utf-8") as f:
        json.dump(coco_data, f, ensure_ascii=False, indent=4)
    
def resize_dataset(ds_dir: Path):
    dst_dir = ds_dir.replace("raw", "processed")
    
    images_dir = ds_dir / "images"
    image_dst_dir = dst_dir / "images"
    
    image_dst_dir.mkdir(parents=True, exist_ok=True)
    Parallel(n_jobs=-1)(delayed(_resize_one)(p, image_dst_dir) for p in images_dir.glob("*"))
    
    annotations_dir = ds_dir / "annotations"
    if not annotations_dir.exists():
        print(f"Annotations directory not found: {annotations_dir}")
        raise FileNotFoundError(f"Annotations directory not found: {annotations_dir}")
    
    annotation_dst_dir = annotations_dir.replace("raw", "processed")
    annotation_dst_dir.mkdir(parents=True, exist_ok=True)
    
    _resize_annotations(annotations_dir, annotation_dst_dir)
    
    print(f"Resized dataset {ds_dir}")