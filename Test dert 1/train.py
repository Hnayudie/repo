# train.py
import os
from dataset import CloudDetectionDataset
from torch.utils.data import DataLoader
from transformers import DetrForObjectDetection, DetrImageProcessor
import torch

def train_model():
    # Define paths
    train_image_dir = './cloud_classification-2/train/images'
    valid_image_dir = './cloud_classification-2/valid/images'
    train_annotations_file = './cloud_json/train/_annotations.coco.json'
    valid_annotations_file = './cloud_json/valid/_annotations.coco.json'

    # Initialize the processor and model
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

    # Create datasets and dataloaders
    train_dataset = CloudDetectionDataset(train_image_dir, train_annotations_file, processor)
    valid_dataset = CloudDetectionDataset(valid_image_dir, valid_annotations_file, processor)
    train_dataloader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    valid_dataloader = DataLoader(valid_dataset, batch_size=4, shuffle=False)

    # Training loop (simplified)
    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)
    for epoch in range(10):  # Number of epochs
        model.train()
        for batch in train_dataloader:
            optimizer.zero_grad()
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
        print(f"Epoch {epoch+1} completed with training loss: {loss.item()}")

        # Validation loop
        model.eval()
        valid_loss = 0
        with torch.no_grad():
            for batch in valid_dataloader:
                outputs = model(**batch)
                valid_loss += outputs.loss.item()
        valid_loss /= len(valid_dataloader)
        print(f"Epoch {epoch+1} completed with validation loss: {valid_loss}")

    # Save the trained model
    model.save_pretrained("./trained_model")
    processor.save_pretrained("./trained_model")