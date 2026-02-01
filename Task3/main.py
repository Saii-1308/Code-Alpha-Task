import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# -----------------------------
# CONFIG
# -----------------------------
CONF_THRESHOLD = 0.5
FRAME_SKIP = 2           # process every 2nd frame
CAMERA_INDEX = 0

# -----------------------------
# Load YOLO model (more accurate than nano)
# -----------------------------
model = YOLO("yolov8s.pt")
model.fuse()  # improves inference speed

# Disable verbose logging
model.overrides["verbose"] = False

# -----------------------------
# Initialize tracker (tuned)
# -----------------------------
tracker = DeepSort(
    max_age=40,
    n_init=3,
    max_cosine_distance=0.2
)

# -----------------------------
# Webcam
# -----------------------------
cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("❌ Webcam not detected")
    exit()

print("✅ Webcam started | Press ESC to exit")

frame_count = 0
detections_cache = []

# -----------------------------
# Main Loop
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # -----------------------------
    # Run detection only every N frames
    # -----------------------------
    if frame_count % FRAME_SKIP == 0:
        results = model.predict(
            frame,
            conf=CONF_THRESHOLD,
            verbose=False
        )[0]

        detections = []

        if results.boxes is not None:
            for box in results.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]

                bbox = [
                    int(x1),
                    int(y1),
                    int(x2 - x1),
                    int(y2 - y1),
                ]
                detections.append((bbox, conf, cls_name))

        detections_cache = detections
    else:
        detections = detections_cache

    # -----------------------------
    # Tracking
    # -----------------------------
    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue

        l, t, w, h = map(int, track.to_ltrb())
        track_id = track.track_id
        cls_name = track.get_det_class()

        label = f"ID {track_id} | {cls_name}"

        cv2.rectangle(frame, (l, t), (l + w, t + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            label,
            (l, t - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # -----------------------------
    # Display
    # -----------------------------
    cv2.imshow("Smooth Object Tracking", frame)

    if cv2.waitKey(1) == 27:
        break

# -----------------------------
# Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()