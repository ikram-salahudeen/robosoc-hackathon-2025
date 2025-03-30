from modlib.apps import Annotator
from modlib.devices import AiCamera
from modlib.models.zoo import SSDMobileNetV2FPNLite320x320
import cv2

device = AiCamera()
model = SSDMobileNetV2FPNLite320x320()
device.deploy(model)

annotator = Annotator(thickness=1, text_thickness=1, text_scale=0.4)

objs = []
scores = []


with device as stream:
    for frame in stream:
        objs = []
        scores = []
        detections = frame.detections[frame.detections.confidence > 0.55]
        labels = [f"{model.labels[class_id]}: {score:0.2f}" for _, score, class_id, _ in detections]

        for _, score, class_id, _ in detections:
            objs.append(model.labels[class_id])  # Store class name
            scores.append(score)  # Store score

        annotator.annotate_boxes(frame, detections, labels=labels)
        frame.display()

        # Save the latest frame as output.jpg
        image = frame.image
        cv2.imwrite("output.jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        with open("detections.txt", "w") as file:
            for name, score in zip(objs, scores):
                file.write(f"{name}:{score:.2f}\n")
    
