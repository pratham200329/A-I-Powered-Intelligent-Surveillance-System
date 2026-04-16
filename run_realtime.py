import argparse

import cv2

from data_pipeline.stream_processor import StreamProcessor


def main() -> None:
    parser = argparse.ArgumentParser(description="Run real-time visitor detection and tracking")
    parser.add_argument("--source", type=str, default="0", help="Camera source: 0, 1 or video path/rtsp url")
    parser.add_argument("--camera-id", type=str, default="cam_local")
    args = parser.parse_args()

    source = int(args.source) if args.source.isdigit() else args.source

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open source: {source}")

    processor = StreamProcessor()

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        out = processor.process_frame(args.camera_id, frame)
        cv2.imshow("Smart Visitor Monitoring", out)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
