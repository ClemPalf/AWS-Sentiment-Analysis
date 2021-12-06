import json
import logging
import sys
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import io
import requests
JSON_CONTENT_TYPE = 'application/json'
JPEG_CONTENT_TYPE = 'image/png'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # calling gpu

def Net():
    """Instantiate an alexnet model."""

    model = models.alexnet(pretrained=True)

    for param in model.parameters():
        param.requires_grad = False   

    num_features=model.classifier[6].in_features # 1000 
    
    # I added a few layers for a "smoother" descent to 133 neurons.
    model.classifier[6] = nn.Sequential(
        nn.Linear(num_features, 750),
        nn.ReLU(inplace=True),
        nn.Linear(750, 500),
        nn.ReLU(inplace=True),
        nn.Linear(500, 250),
        nn.ReLU(inplace=True),
        nn.Linear(250, 133)) # No need for a softmax, it is included in the "nn.CrossEntropyLoss()"
    
    return model

def model_fn(model_dir):
    """Load the PyTorch model from the `model_dir` directory."""
    
    print("Loading model.")
    
    model = Net().to(device)
    
    with open(os.path.join(model_dir, "model.pth"), "rb") as f:
        checkpoint = torch.load(f, map_location=device)
        model.load_state_dict(checkpoint)

    model.eval()
    
    return model


def input_fn(request_body, content_type):

    if content_type == JPEG_CONTENT_TYPE: 
        return Image.open(io.BytesIO(request_body))
    
    raise Exception('Requested unsupported ContentType in content_type: {}'.format(content_type))


def predict_fn(input_object, model):
    

    test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                             std=[0.229, 0.224, 0.225])])
    
    input_object=test_transform(input_object)
    input_object = input_object.to(device) #put data into GPU
    
    with torch.no_grad():
        prediction = model(input_object.unsqueeze(0))
        
    return prediction