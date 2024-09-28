# main.py
import argparse
from train import train_model
from predict import make_predictions

def main():
    parser = argparse.ArgumentParser(description="Cloud Detection using DETR")
    parser.add_argument('--mode', type=str, required=True, choices=['train', 'predict'], help="Mode: train or predict")
    parser.add_argument('--image_dir', type=str, help="Path to the input image directory for prediction")
    args = parser.parse_args()

    if args.mode == 'train':
        train_model()
    elif args.mode == 'predict':
        if not args.image_dir:
            parser.error("The --image_dir argument is required in predict mode.")
        make_predictions(args.image_dir)

if __name__ == "__main__":
    main()