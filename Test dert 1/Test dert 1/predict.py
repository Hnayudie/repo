import os
import torch
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from transformers import DetrImageProcessor
from model import DETR

CLOUD_TYPE_COLORS = {
    0: (255, 0, 0),
    1: (0, 255, 0),
    2: (0, 0, 255),
    3: (128, 0, 128)
}

def visualize_predictions(image, outputs):
    image = image.cpu().permute(1, 2, 0).numpy()
    image = (image * 255).astype('uint8')
    plt.imshow(image)

    for box, label in zip(outputs['boxes'], outputs['labels']):
        xmin, ymin, xmax, ymax = box.detach().cpu().numpy()
        color = CLOUD_TYPE_COLORS.get(label.item(), (255, 255, 255))
        cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)

    plt.imshow(image)
    plt.show()

def make_predictions(image_dir):
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DETR(num_classes=91, hidden_dim=256, nheads=8, num_encoder_layers=6, num_decoder_layers=6, batch_first=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    for image_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_name)
        if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        image = Image.open(image_path).convert("RGB")
        encoding = processor(images=image, return_tensors="pt")
        pixel_values = encoding["pixel_values"].to(device)

        with torch.no_grad():
            outputs = model(pixel_values=pixel_values)
            results = processor.post_process_object_detection(outputs, threshold=0.9)[0]

        visualize_predictions(pixel_values[0], results)