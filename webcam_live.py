import cv2
import torch
from ultralytics import YOLO

def run_live(model_size="yolov8n", confidence=0.25):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[Live] Loading {model_size} on {device}...")
    model = YOLO(f"{model_size}.pt")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Error] Could not open webcam.")
        return

    print("[Live] Press Q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(
            source=frame,
            conf=confidence,
            device=device,
            verbose=False,
        )

        annotated = results[0].plot()

        detections = results[0].boxes
        count = len(detections)
        cv2.putText(
            annotated,
            f"Objects: {count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        cv2.imshow("YOLOv8 Live Detection — Press Q to quit", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[Live] Stopped.")

if __name__ == "__main__":
    run_live()
