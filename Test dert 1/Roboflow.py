import os
from roboflow import Roboflow
from utils import download_with_retries

rf = Roboflow(api_key="7Ca966bERJo6Wo8lFGyX")
project = rf.workspace("simplon-xajv7").project("cloud_classification-cjuda")
version = project.version(2)
dataset = download_with_retries(version, "coco-mmdetection")

# Update the annotations directory to the new cloud_json folder
annotations_dir = './cloud_json'

# Check if the JSON files exist
for split in ["train", "valid", "test"]:
    annotations_file = os.path.join(annotations_dir, f"{split}_annotations.coco.json")
    if not os.path.exists(annotations_file):

        raise FileNotFoundError(f"{split.capitalize()} annotations file not found: {annotations_file}")
    else:
        print(f"{split.capitalize()} annotations file found: {annotations_file}")