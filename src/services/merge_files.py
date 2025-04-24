import os
from pathlib import Path
import shutil
import json

def copy_images(input_dir, out_images_dir):
    for root, dirs, files in os.walk(input_dir):
        if os.path.basename(root) == "images":
            for file in files:
                src = os.path.join(root, file)
                dst = os.path.join(out_images_dir, file)
                if os.path.exists(dst):
                    base, ext = os.path.splitext(file)
                    counter = 1
                    new_file = f"{base}_copy{counter}{ext}"
                    dst = os.path.join(out_images_dir, new_file)
                    while os.path.exists(dst):
                        counter += 1
                        new_file = f"{base}_copy{counter}{ext}"
                        dst = os.path.join(out_images_dir, new_file)
                shutil.copy2(src, dst)

def merge_instances(input_dir):
    merged = {"images": [], "annotations": [], "categories": None, "defects": []}
    images_set = set()
    ann_image_ids = set()

    for root, dirs, files in os.walk(input_dir):
        if "instances.json" in files:
            instances_path = os.path.join(root, "instances.json")
            with open(instances_path, encoding="utf-8") as f:
                data = json.load(f)
            if merged["categories"] is None:
                merged["categories"] = data.get("categories", [])
            for img in data.get("images", []):
                images_set.add(img["id"])
                merged["images"].append(img)
            for ann in data.get("annotations", []):
                if "image_id" in ann:
                    ann_image_ids.add(ann["image_id"])
                merged["annotations"].append(ann)

    defect_images = [img_id for img_id in images_set if img_id not in ann_image_ids]
    merged["defects"] = defect_images
    return merged

def merge_subfolders(dataset_path: Path):
    if (dataset_path / "images").exists() and (dataset_path / "annotations").exists():
        return

    out_images_dir = os.path.join(dataset_path, "images")
    os.makedirs(out_images_dir, exist_ok=True)
    out_annotations_dir = os.path.join(dataset_path, "annotations")
    os.makedirs(out_annotations_dir, exist_ok=True)

    copy_images(dataset_path, out_images_dir)

    merged_data = merge_instances(dataset_path)
    out_json_path = os.path.join(out_annotations_dir, "instances.json")
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
        
    for item in os.listdir(dataset_path):
        if item not in ["images", "annotations"]:
            item_path = os.path.join(dataset_path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            else:
                shutil.rmtree(item_path)