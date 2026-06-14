import cv2
import torch
import numpy as np
from ultralytics import YOLO
from PIL import Image

MODELS = {
    "YOLOv8 Nano (fastest)": "yolov8n",
    "YOLOv8 Small": "yolov8s",
    "YOLOv8 Medium": "yolov8m",
    "YOLOv8 Large (most accurate)": "yolov8l",
}

class ObjectDetector:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.current_model_name = None
        self.model = None
        self.load_model("YOLOv8 Nano (fastest)")

    def load_model(self, model_label: str):
        if model_label == self.current_model_name:
            return
        model_file = MODELS[model_label]
        print(f"[Detector] Loading {model_file} on {self.device}...")
        self.model = YOLO(f"{model_file}.pt")
        self.current_model_name = model_label
        print(f"[Detector] Model ready.")

    def detect_image(self, image: Image.Image, confidence: float = 0.25):
        img_array = np.array(image)
        results = self.model.predict(
            source=img_array,
            conf=confidence,
            device=self.device,
            verbose=False,
        )
        result = results[0]
        annotated = cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB)
        output_image = Image.fromarray(annotated)

        detections = []
        for box in result.boxes:
            label = self.model.names[int(box.cls)]
            conf = float(box.conf)
            detections.append(f"{label}: {conf:.0%}")

        summary = "\n".join(detections) if detections else "No objects detected"
        return output_image, summary, f"{len(detections)} object(s) detected"

    def detect_video(self, video_path: str, confidence: float = 0.25):
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 24

        output_path = "output_video.mp4"
        writer = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height),
        )

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = self.model.predict(
                source=frame,
                conf=confidence,
                device=self.device,
                verbose=False,
            )
            annotated = results[0].plot()
            writer.write(annotated)
            frame_count += 1

        cap.release()
        writer.release()
        print(f"[Detector] Processed {frame_count} frames")
        return output_path