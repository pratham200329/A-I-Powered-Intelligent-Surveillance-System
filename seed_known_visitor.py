import argparse

from cv_module.face_recognizer import FaceRecognizer
from data_pipeline.feature_store import FeatureStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Enroll a known visitor from image")
    parser.add_argument("--external-id", required=True)
    parser.add_argument("--name", default=None)
    parser.add_argument("--image", required=True)
    args = parser.parse_args()

    recognizer = FaceRecognizer()
    ok = recognizer.add_known_face(args.image, args.external_id)
    if not ok:
        raise RuntimeError("Could not detect face in image")

    FeatureStore().upsert_visitor(
        external_id=args.external_id,
        name=args.name,
        is_known=True,
    )
    print("Visitor enrolled successfully")


if __name__ == "__main__":
    main()
