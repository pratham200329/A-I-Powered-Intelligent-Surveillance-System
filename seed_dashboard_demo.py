import json
import random
from datetime import datetime, timedelta

from sqlalchemy import delete

from backend.database import Base, SessionLocal, engine
from backend.db_models import Alert, VisitLog, Visitor


def _random_trajectory(length: int = 18) -> str:
    x = random.uniform(80, 1200)
    y = random.uniform(60, 620)
    points: list[list[float]] = []

    for _ in range(length):
        x = max(0.0, min(1280.0, x + random.uniform(-35, 35)))
        y = max(0.0, min(720.0, y + random.uniform(-30, 30)))
        points.append([round(x, 2), round(y, 2)])

    return json.dumps(points)


def seed_dashboard_data() -> dict[str, int]:
    random.seed(42)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        demo_visitors = db.query(Visitor).filter(Visitor.external_id.like("DEMO_%")).all()
        demo_ids = [v.id for v in demo_visitors]

        if demo_ids:
            db.execute(delete(Alert).where(Alert.visitor_id.in_(demo_ids)))
            db.execute(delete(VisitLog).where(VisitLog.visitor_id.in_(demo_ids)))
            db.execute(delete(Visitor).where(Visitor.id.in_(demo_ids)))
            db.commit()

        visitors: list[Visitor] = []
        for idx in range(1, 61):
            is_known = idx % 3 != 0
            visitor = Visitor(
                external_id=f"DEMO_{idx:03d}",
                name=f"Visitor {idx:03d}" if is_known else None,
                is_known=is_known,
            )
            db.add(visitor)
            visitors.append(visitor)

        db.flush()

        cameras = ["cam_1", "cam_2", "cam_3", "cam_gate"]
        visit_counts: dict[int, int] = {v.id: 0 for v in visitors}
        now = datetime.utcnow()

        alert_count = 0
        total_logs = 900

        for idx in range(total_logs):
            visitor = random.choice(visitors)
            visit_counts[visitor.id] += 1

            camera_id = random.choice(cameras)
            entry_time = now - timedelta(
                hours=random.randint(0, 24 * 21),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59),
            )

            duration_seconds = max(8.0, min(1100.0, random.gauss(170, 95)))
            exit_time = entry_time + timedelta(seconds=duration_seconds)
            avg_speed = max(0.05, min(5.8, random.gauss(1.25, 0.65)))
            area_coverage = max(0.001, min(0.95, random.gauss(0.13, 0.07)))
            odd_hour_visit = entry_time.hour <= 5 or entry_time.hour >= 23
            repeated_visit_count = max(1, visit_counts[visitor.id] - 1)

            suspicious = (
                duration_seconds > 350
                or (repeated_visit_count >= 4 and odd_hour_visit)
                or (avg_speed < 0.35 and duration_seconds > 220)
            )
            is_anomaly = suspicious or random.random() < 0.035

            log = VisitLog(
                visitor_id=visitor.id,
                camera_id=camera_id,
                track_id=f"demo_track_{idx + 1}",
                entry_time=entry_time,
                exit_time=exit_time,
                duration_seconds=float(duration_seconds),
                trajectory_json=_random_trajectory(),
                avg_speed=float(avg_speed),
                area_coverage=float(area_coverage),
                repeated_visit_count=int(repeated_visit_count),
                odd_hour_visit=bool(odd_hour_visit),
                behavior_label="suspicious" if suspicious else "normal",
                anomaly_score=float(random.uniform(0.65, 0.99) if is_anomaly else random.uniform(0.01, 0.45)),
                is_anomaly=bool(is_anomaly),
                cluster_label=int(random.choice([0, 1, 2])),
            )
            db.add(log)

            if is_anomaly and random.random() < 0.5:
                db.add(
                    Alert(
                        visitor_id=visitor.id,
                        camera_id=camera_id,
                        alert_type="behavior_anomaly",
                        message=f"Anomalous behavior pattern detected for {visitor.external_id}",
                        severity="high",
                        created_at=entry_time + timedelta(seconds=5),
                    )
                )
                alert_count += 1
            elif (not visitor.is_known) and random.random() < 0.28:
                db.add(
                    Alert(
                        visitor_id=visitor.id,
                        camera_id=camera_id,
                        alert_type="unknown_person",
                        message=f"Unknown visitor observed on {camera_id}",
                        severity="medium",
                        created_at=entry_time + timedelta(seconds=3),
                    )
                )
                alert_count += 1

        db.commit()

        return {
            "visitors": len(visitors),
            "visit_logs": total_logs,
            "alerts": alert_count,
        }


def main() -> None:
    summary = seed_dashboard_data()
    print(
        "Seeded dashboard demo data: "
        f"{summary['visitors']} visitors, {summary['visit_logs']} logs, {summary['alerts']} alerts"
    )


if __name__ == "__main__":
    main()
