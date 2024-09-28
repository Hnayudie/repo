import torch
from torch.utils.data import Dataset
import os
from PIL import Image
import json

class CloudDetectionDataset(Dataset):
    def __init__(self, image_dir, annotations_file, processor, transforms=None):
        self.image_dir = image_dir
        self.annotations = json.load(open(annotations_file))
        self.transforms = transforms
        self.processor = processor
        self.images = list(self.annotations["images"])
        self.file_name = []
        for i in self.images :
            self.file_name.append(i["file_name"])
            print(i["file_name"])


    def __len__(self):
        return len(self.file_name)

    def __getitem__(self, idx):
        img_name = self.file_name[idx]
        img_path = os.path.join(self.image_dir, img_name)
        image = Image.open(img_path).convert("RGB")

        boxes = torch.tensor(self.annotations[img_name]['boxes'], dtype=torch.float32)
        labels = torch.tensor(self.annotations[img_name]['labels'], dtype=torch.int64)

        if self.transforms:
            image = self.transforms(image)

        encoding = self.processor(images=image, annotations={"boxes": boxes, "labels": labels}, return_tensors="pt")

        return encoding