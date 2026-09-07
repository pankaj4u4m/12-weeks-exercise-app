#!/usr/bin/env python3
"""Generate the curated 30-minute full-body plan with strict weekly variety."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM_DIRS = [
    ROOT / "programs",
    ROOT / "app/src/main/assets/programs",
    ROOT / "app/src/wasmJsMain/resources/programs",
]
PROGRAM_ID = "program-1"

CATALOG_MEDIA = {
    e["name"]: {k: e[k] for k in ("wgerId", "exerciseDbId", "freeExerciseDbId", "bundledMediaAsset", "externalMediaUrl") if e.get(k)}
    for e in json.loads((ROOT / "programs/_pools/exercise-catalog.json").read_text(encoding="utf-8"))["exercises"]
}


def ex(name: str, *, reps: int | None = None, seconds: int | None = None, raw: str | None = None, media_name: str | None = None):
    assert (reps is None) != (seconds is None), name
    item = {"raw": raw or (f"{reps} {name}" if reps is not None else f"{seconds}s {name}"), "name": name}
    if reps is not None:
        item["reps"] = reps
    else:
        item["seconds"] = seconds
    media_key = media_name or name
    media = CATALOG_MEDIA.get(media_key)
    assert media, f"Missing media for {name} (base {media_key})"
    item.update(media)
    return item


def side_ex(base_name: str, side: str, *, reps: int | None = None, seconds: int | None = None):
    return ex(f"{base_name} {side}", reps=reps, seconds=seconds, media_name=base_name)


def split_total_reps(base_name: str, total_reps: int):
    each = max(1, (total_reps + 1) // 2)
    return [side_ex(base_name, "L", reps=each), side_ex(base_name, "R", reps=each)]


def scale(value: int, factor: float, cap: int | None = None):
    scaled = max(1, round(value * factor))
    return min(cap, scaled) if cap is not None else scaled


def warmup(day: int):
    # Different warm-up each day. Every exact exercise is capped at two days/week.
    sets = {
        1: [ex("Arm Circle Forward", seconds=15), ex("Standing Hip Circles", seconds=20), ex("Inchworm", reps=4), ex("High Knees", reps=16)],
        2: [ex("Arm Swing", seconds=20), ex("Torso Twist", seconds=20), ex("Walking Lunges", reps=8, raw="8 Walking Lunges · total"), ex("Shoulder Roll", seconds=20)],
        3: [ex("Arm Circle Backward", seconds=15), ex("Cat Cow", seconds=25), ex("Standing Toe Touches", seconds=20), ex("Shoulder Circles", reps=8)],
        4: [ex("Arm Circle Forward", seconds=15), ex("Cat Cow Stretch", seconds=25), ex("High Knees", reps=16), ex("SLOW Push-ups", reps=4)],
        5: [ex("Arm Swing", seconds=20), ex("Standing Hip Circles", seconds=20), ex("Inchworm", reps=4), ex("Shoulder Roll", seconds=20)],
        6: [ex("Arm Circle Backward", seconds=15), ex("Torso Twist", seconds=20), ex("Walking Lunges", reps=8, raw="8 Walking Lunges · total"), ex("Shoulder Circles", reps=8)],
        7: [ex("Cat Cow", seconds=25), ex("Standing Toe Touches", seconds=20), ex("SLOW Push-ups", reps=4), ex("Mountain Climbers", reps=12, raw="12 Mountain Climbers · easy")],
    }
    return sets[day]


def stretching(day: int):
    # Hamstrings/posterior chain, torso and traps get extra weekly attention,
    # but the exact same stretch is never scheduled on more than two days.
    sets = {
        1: [
            ex("Hamstring Stretch L", seconds=45), ex("Hamstring Stretch R", seconds=45),
            ex("Upper Back Stretch", seconds=45, raw="45s Upper Back Stretch · relax neck and traps"),
            ex("Hip Flexor Stretch L", seconds=30), ex("Hip Flexor Stretch R", seconds=30),
        ],
        2: [
            ex("Downward Facing Dog", seconds=40), ex("Torso Rotation Stretch", seconds=40),
            ex("Cross Body Shoulder Stretch L", seconds=30), ex("Cross Body Shoulder Stretch R", seconds=30),
            side_ex("Side Stretch", "L", seconds=30), side_ex("Side Stretch", "R", seconds=30),
        ],
        3: [
            side_ex("Pigeon Pose", "L", seconds=30), side_ex("Pigeon Pose", "R", seconds=30),
            ex("Butterfly Stretch", seconds=40), ex("Calf Stretch L", seconds=30),
            ex("Calf Stretch R", seconds=30), ex("Spinal Stretch", seconds=40),
        ],
        4: [
            ex("Hamstring Stretch L", seconds=45), ex("Hamstring Stretch R", seconds=45),
            ex("Upper Back Stretch", seconds=45, raw="45s Upper Back Stretch · relax neck and traps"),
            side_ex("Side Lunge Stretch", "L", seconds=30), side_ex("Side Lunge Stretch", "R", seconds=30), ex("Child's Pose", seconds=40),
        ],
        5: [
            ex("Hip Flexor Stretch L", seconds=30), ex("Hip Flexor Stretch R", seconds=30),
            ex("Torso Rotation Stretch", seconds=40), ex("Wall Pectoral Stretch L", seconds=30),
            ex("Wall Pectoral Stretch R", seconds=30),
        ],
        6: [
            ex("Downward Facing Dog", seconds=40), ex("Cross Body Shoulder Stretch L", seconds=30),
            ex("Cross Body Shoulder Stretch R", seconds=30), ex("Hug Knees To Chest", seconds=40),
            side_ex("Side-Lying Floor Stretch", "L", seconds=30), side_ex("Side-Lying Floor Stretch", "R", seconds=30),
        ],
        7: [
            side_ex("Pigeon Pose", "L", seconds=30), side_ex("Pigeon Pose", "R", seconds=30),
            ex("Butterfly Stretch", seconds=40), ex("Spinal Stretch", seconds=40),
            side_ex("Side Stretch", "L", seconds=30), side_ex("Side Stretch", "R", seconds=30), ex("Quad Wall Stretch L", seconds=30), ex("Quad Wall Stretch R", seconds=30),
        ],
    }
    return sets[day]


def main_moves(day: int, f: float):
    sets = {
        1: [
            ex("Squats", reps=scale(10, f, 14)),
            ex("Push-ups", reps=scale(7, f, 10), raw=f"{scale(7, f, 10)} Push-ups · leave 2 reps in reserve"),
            ex("Reverse Lunge", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Reverse Lunges · total"),
            ex("Glute Bridge", reps=scale(10, f, 14)),
            ex("Superman", reps=scale(8, f, 12)),
            ex("Front Plank", seconds=scale(25, f, 35)),
            ex("Calf Raises", reps=scale(12, f, 16)),
            ex("Dead Bug", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Dead Bugs · total"),
        ],
        2: [
            ex("Dumbbell Walking Lunge", reps=scale(10, f, 14), raw=f"{scale(10, f, 14)} Dumbbell Walking Lunges · total"),
            ex("Pike Push-ups", reps=scale(8, f, 12)),
            ex("Lateral Lunge", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Lateral Lunges · total"),
            ex("Glute Bridge", reps=scale(10, f, 14)),
            ex("Bird Dog", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Bird Dogs · total"),
            ex("Side Plank L", seconds=scale(20, f, 30)),
            ex("Side Plank R", seconds=scale(20, f, 30)),
            ex("Punches", reps=scale(20, f, 30), raw=f"{scale(20, f, 30)} Punches · total"),
        ],
        3: [
            *split_total_reps("Split Squats", scale(8, f, 12)),
            ex("Pike Push-ups", reps=scale(5, f, 8)),
            *split_total_reps("Single Leg Glute Bridge", scale(8, f, 12)),
            ex("Wide Push-up", reps=scale(6, f, 10)),
            ex("Plank Shoulder Taps", reps=scale(10, f, 16), raw=f"{scale(10, f, 16)} Plank Shoulder Taps · total"),
            ex("Standing Oblique Crunch", reps=scale(10, f, 16), raw=f"{scale(10, f, 16)} Standing Oblique Crunches · total"),
            *split_total_reps("Single Leg Calf Raise", scale(10, f, 14)),
            ex("Russian Twist", reps=scale(12, f, 18), raw=f"{scale(12, f, 18)} Russian Twists · total"),
        ],
        4: [
            ex("Squats", reps=8), ex("Knee Push-ups", reps=6),
            *split_total_reps("Clamshell", 10), *split_total_reps("Donkey Kicks", 10),
            ex("High Plank", seconds=20), ex("Heel Touches", reps=12, raw="12 Heel Touches · total"),
            ex("Side Lunge", reps=8, raw="8 Side Lunges · total"), ex("Superman", reps=8),
        ],
        5: [
            ex("Sumo Squats", reps=scale(10, f, 14)), ex("Diamond Push-up", reps=scale(6, f, 10)),
            ex("Dumbbell Walking Lunge", reps=scale(10, f, 14), raw=f"{scale(10, f, 14)} Dumbbell Walking Lunges · total"),
            ex("Glute Bridge March", reps=scale(10, f, 14), raw=f"{scale(10, f, 14)} Glute Bridge Marches · total"),
            ex("Plank Reach", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Plank Reaches · total"),
            ex("Bicycle Crunch", reps=scale(12, f, 18), raw=f"{scale(12, f, 18)} Bicycle Crunches · total"),
            ex("Calf Raises", reps=scale(12, f, 16)),
            ex("Push-ups", reps=scale(7, f, 10), raw=f"{scale(7, f, 10)} Push-ups · leave 2 reps in reserve"),
        ],
        6: [
            ex("Quick Feet", seconds=25),
            ex("Reverse Lunge", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Reverse Lunges · total"),
            ex("Knee Push-ups", reps=scale(8, f, 12)), ex("Glute Bridge March", reps=scale(10, f, 14)),
            ex("Bird Dog", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Bird Dogs · total"),
            ex("Front Plank", seconds=scale(25, f, 35)), ex("Scissor Kicks", reps=scale(12, f, 18), raw=f"{scale(12, f, 18)} Scissor Kicks · total"),
            ex("Punches", reps=scale(20, f, 30), raw=f"{scale(20, f, 30)} Punches · total"),
        ],
        7: [
            *split_total_reps("Static Lunge", 8), ex("Wide Push-up", reps=6),
            *split_total_reps("Single Leg Glute Bridge", 8),
            *split_total_reps("Clamshell", 10), ex("High Plank", seconds=20),
            ex("Standing Oblique Crunch", reps=10, raw="10 Standing Oblique Crunches · total"),
            *split_total_reps("Single Leg Calf Raise", 10),
            ex("Dead Bug", reps=8, raw="8 Dead Bugs · total"),
        ],
    }
    return sets[day]


FACTORS = {1: .90, 2: .95, 3: 1.00, 4: .90, 5: 1.00, 6: 1.05, 7: 1.05, 8: .90, 9: 1.05, 10: 1.10, 11: 1.10, 12: 1.00}
DAY_TITLES = {1: "Strength A", 2: "Strength B", 3: "Strength C", 4: "Recovery A", 5: "Strength D", 6: "Conditioning", 7: "Recovery B"}


def workout(day: int, f: float):
    moves = main_moves(day, f)
    return {
        "index": day,
        "estimatedMinutes": 30 if day not in (4, 7) else 24,
        "sections": [
            {"title": "Warm-up", "exercises": warmup(day)},
            {"title": f"Rep 1 · {DAY_TITLES[day]}", "exercises": moves},
            {"title": "Rep 2", "exercises": moves},
            {"title": "Stretching", "exercises": stretching(day)},
        ],
    }


def build_program():
    return {
        "id": PROGRAM_ID,
        "title": "Full Body · 30 min",
        "level": "INTERMEDIATE",
        "focusAreas": ["FULL_BODY", "STRENGTH", "CORE"],
        "equipment": ["HOME"],
        "sessionMinutes": 30,
        "weeks": [
            {"number": week, "workouts": [workout(day, FACTORS[week]) for day in range(1, 8)]}
            for week in range(1, 13)
        ],
    }


def validate(program):
    assert len(program["weeks"]) == 12
    for week in program["weeks"]:
        assert len(week["workouts"]) == 7
        exercise_days: dict[str, set[int]] = {}
        for work in week["workouts"]:
            assert [s["title"].split(" · ")[0] for s in work["sections"]] == ["Warm-up", "Rep 1", "Rep 2", "Stretching"]
            for section in work["sections"]:
                for item in section["exercises"]:
                    assert any(k in item for k in ("wgerId", "exerciseDbId", "freeExerciseDbId", "bundledMediaAsset", "externalMediaUrl")), item["name"]
                    exercise_days.setdefault(item["name"], set()).add(work["index"])
        too_frequent = {name: sorted(days) for name, days in exercise_days.items() if len(days) > 2}
        assert not too_frequent, too_frequent


def main():
    program = build_program()
    validate(program)
    program_text = json.dumps(program, ensure_ascii=False, indent=2) + "\n"
    for directory in PROGRAM_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
        for path in directory.glob("*.json"):
            if path.name not in {"program-1.json", "program-2.json", "index.json"}:
                path.unlink()
        (directory / "program-1.json").write_text(program_text, encoding="utf-8")

        index_path = directory / "index.json"
        existing = []
        if index_path.exists():
            existing = [p for p in json.loads(index_path.read_text(encoding="utf-8")).get("programs", []) if p.get("id") != PROGRAM_ID]
        entry = {
            "id": PROGRAM_ID,
            "title": program["title"],
            "level": program["level"],
            "focusAreas": program["focusAreas"],
            "equipment": program["equipment"],
            "weeks": 12,
            "file": "programs/program-1.json",
            "sessionMinutes": program["sessionMinutes"],
        }
        index_path.write_text(json.dumps({"programs": [entry, *existing]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Generated program-1: Full Body · 30 min with strict <=2 days/week exercise frequency.")


if __name__ == "__main__":
    main()
