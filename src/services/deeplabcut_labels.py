import os
import csv
import json
from pathlib import Path

def get_keypoint_for_image(json_paths, image_file):
    for json_path in json_paths:
        with open(json_path, mode="r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        image_id = None
        for image in data.get("images", []):
            if image.get("file_name", "") == image_file:
                image_id = image.get("id")
                break

        if image_id is None:
            continue

        annotation = None
        for ann in data.get("annotations", []):
            if ann.get("image_id") == image_id:
                annotation = ann
                break

        if annotation is None:
            continue

        keypoints = annotation.get("keypoints", [])

        coords = []
        for i in range(0, len(keypoints), 3):
            coords.append(str(keypoints[i]))
            coords.append(str(keypoints[i + 1]))
        return coords

    print("Не удалось найти координаты для изображения:", image_file)
    return None

def create_csv_in_subfolders(json_paths, root_dir):
    for current_path, subdirs, _ in os.walk(root_dir):
        if Path(current_path) == root_dir:
            continue

        csv_file_name = "CollectedData_exp.csv"
        csv_path = os.path.join(current_path, csv_file_name)

        row1 = [
            "scorer", "", "",
            "exp", "exp", "exp", "exp", 
            "exp", "exp", "exp", "exp", 
            "exp", "exp", "exp", "exp", 
            "exp", "exp", "exp", "exp", 
            "exp", "exp", "exp", "exp", 
            "exp", "exp", "exp", "exp", 
            "exp", "exp", "exp", "exp", 
            "exp", "exp", "exp", "exp", 
            "exp", "exp", "exp", "exp", 
            "exp", "exp", "exp", "exp", 
            "exp", "exp"
        ]
        row2 = [
            "bodyparts", "", "",
            "point1", "point1", "point2", "point2",
            "point3", "point3", "point4", "point4",
            "point5", "point5", "point6", "point6",
            "point7", "point7", "point8", "point8",
            "point9", "point9", "point10", "point10",
            "point11", "point11", "point12", "point12",
            "point13", "point13", "point14", "point14",
            "point15", "point15", "point16", "point16",
            "point17", "point17", "point18", "point18",
            "point19", "point19", "point20", "point20",
            "point21", "point21"
        ]
        row3 = [
            "coords", "", "",
            "x", "y", "x", "y", "x", "y", "x", "y",
            "x", "y", "x", "y", "x", "y", "x", "y",
            "x", "y", "x", "y", "x", "y", "x", "y",
            "x", "y", "x", "y", "x", "y", "x", "y",
            "x", "y", "x", "y", "x", "y", "x", "y",
            "x", "y"
        ]
        # Определяем имя файла изображения и получаем координаты
        folder_name = os.path.basename(current_path)
        image_file = folder_name + ".jpg"
        coords = get_keypoint_for_image(json_paths, image_file)
        if not coords:
            coords = [""] * 42
        row4 = ["labeled-data", folder_name, "img0.png"] + coords

        # Проверяем, что количество колонок во всех строках совпадает
        expected = len(row1)
        rows = [row1, row2, row3, row4]
        for idx, row in enumerate(rows, start=1):
            if len(row) != expected:
                print("Несоответствие количества колонок в файле '{}': строка {} имеет {} столбцов, ожидается {}".format(csv_path, idx, len(row), expected))

        # Записываем строки в csv файл
        with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(row1)
            writer.writerow(row2)
            writer.writerow(row3)
            writer.writerow(row4)