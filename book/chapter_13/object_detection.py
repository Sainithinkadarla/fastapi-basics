from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import torch 
from transformers import YolosForObjectDetection, YolosImageProcessor

root_dir = Path(__file__).parent
image_path = root_dir / "image.png"
image = Image.open(image_path)

image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")

inputs = image_processor(images = image, return_tensors = "pt")
outputs = model(**inputs)

target_sizes = torch.tensor([image.size[::-1]])
results = image_processor.post_process_object_detection(outputs, target_sizes=target_sizes)[0]

draw = ImageDraw.Draw(image)
for score, box, label in zip(results["scores"], results["boxes"], results["labels"]):
    if score > 0.7:
        box_values = box.tolist()
        label = model.config.id2label[label.item()]
        draw.rectangle(box_values, outline = "red", width = 3)
        draw.text([box_values[0], box_values[1]-10], label, fill="yellow", stroke_width=0.3)

image.save("detected.png")

