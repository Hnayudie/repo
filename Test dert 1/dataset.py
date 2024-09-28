def __getitem__(self, idx):
    img_name = self.file_name[idx]
    img_path = os.path.join(self.image_dir, img_name)
    image = Image.open(img_path).convert("RGB")

    # Find the image id
    image_id = None
    for img in self.annotations["images"]:
        if img["file_name"] == img_name:
            image_id = img["id"]
            break

    if image_id is None:
        raise KeyError(f"Image ID not found for {img_name}")

    # Initialize boxes and labels
    boxes = []
    labels = []

    # Find boxes and labels corresponding to the image_id
    for ann in self.annotations.get("annotations", []):
        if ann["image_id"] == image_id:
            boxes.append(ann["bbox"])  # Use 'bbox' from the annotation
            labels.append(ann["category_id"])  # Use 'category_id' for the label

    # Convert to tensors
    if boxes and labels:  # Ensure that boxes and labels have values before conversion
        boxes = torch.tensor(boxes, dtype=torch.float32)
        labels = torch.tensor(labels, dtype=torch.int64)
    else:
        # Handle the case where there are no boxes or labels
        boxes = torch.empty((0, 4), dtype=torch.float32)  # Assuming boxes are in [x, y, width, height] format
        labels = torch.empty((0,), dtype=torch.int64)  # No labels

    if self.transforms:
        image = self.transforms(image)

    # Prepare the encoding
    encoding = self.processor(images=image, annotations={"boxes": boxes, "labels": labels}, return_tensors="pt")

    return encoding
