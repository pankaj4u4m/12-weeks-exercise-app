#!/usr/bin/env python3
"""Add a second curated 12-week, 15-minute weighted full-body plan."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM_DIRS = [
    ROOT / "programs",
    ROOT / "app/src/main/assets/programs",
    ROOT / "app/src/wasmJsMain/resources/programs",
]
PROGRAM_ID = "program-2"

CATALOG_MEDIA = {
    e["name"]: {k: e[k] for k in ("wgerId", "exerciseDbId", "freeExerciseDbId", "bundledMediaAsset", "externalMediaUrl") if e.get(k)}
    for e in json.loads((ROOT / "programs/_pools/exercise-catalog.json").read_text(encoding="utf-8"))["exercises"]
}

MEDIA = {
    "Jumping Jacks": {"wgerId": "320"},
    "Arm Circle Forward": {"wgerId": "994"},
    "Arm Circle Backward": {"wgerId": "995"},
    "Standing Hip Circles": {"freeExerciseDbId": "Standing_Hip_Circles"},
    "Torso Twist": {"wgerId": "1377"},
    "Torso Rotation Stretch": {"freeExerciseDbId": "Torso_Rotation"},
    "Side Stretch": {"wgerId": "1861"},
    "Squats": {"wgerId": "615", "freeExerciseDbId": "Bodyweight_Squat"},
    "Push-ups": {"wgerId": "1551", "freeExerciseDbId": "Pushups"},
    "Incline Push-up": {"wgerId": "1111", "freeExerciseDbId": "Incline_Push-Up"},
    "Dumbbell Goblet Squat": {"wgerId": "203", "exerciseDbId": "exr_41n2hQDiSwTZXM4F", "freeExerciseDbId": "Goblet_Squat"},
    "Dumbbell Lunges": {"wgerId": "984", "freeExerciseDbId": "Dumbbell_Lunges"},
    "Dumbbell Walking Lunge": {"wgerId": "206", "exerciseDbId": "exr_41n2hQHmRSoUkk9F", "freeExerciseDbId": "Dumbbell_Lunges"},
    "Step-ups": {"wgerId": "981", "exerciseDbId": "exr_41n2hXvPyEyMBgNR"},
    "Dumbbell Row": {"wgerId": "81", "exerciseDbId": "exr_41n2hY9EdwkdGz9a", "freeExerciseDbId": "Bent_Over_Two-Dumbbell_Row"},
    "Dumbbell Shoulder Press": {"wgerId": "567", "exerciseDbId": "exr_41n2hs6camM22yBG", "freeExerciseDbId": "Dumbbell_Shoulder_Press"},
    "Dumbbell Bicep Curl": {"wgerId": "92", "freeExerciseDbId": "Dumbbell_Bicep_Curl"},
    "Dumbbell Bench Press": {"wgerId": "75", "freeExerciseDbId": "Dumbbell_Bench_Press"},
    "Lateral Raise": {"wgerId": "348", "exerciseDbId": "exr_41n2hjuGpcex14w7", "freeExerciseDbId": "Side_Lateral_Raise"},
    "Romanian Deadlift": {"wgerId": "507", "exerciseDbId": "exr_41n2hn8rpbYihzEW", "freeExerciseDbId": "Romanian_Deadlift"},
    "Barbell Row": {"wgerId": "83", "freeExerciseDbId": "Bent_Over_Barbell_Row"},
    "Barbell Shoulder Press": {"wgerId": "566", "freeExerciseDbId": "Barbell_Shoulder_Press"},
    "Glute Bridge": {"wgerId": "265", "freeExerciseDbId": "Butt_Lift_Bridge"},
    "Glute Bridge March": {"wgerId": "265", "freeExerciseDbId": "Butt_Lift_Bridge"},
    "Single Leg Glute Bridge": {"wgerId": "1740", "freeExerciseDbId": "Single_Leg_Glute_Bridge"},
    "Calf Raises": {"wgerId": "622", "freeExerciseDbId": "Standing_Calf_Raises"},
    "Bird Dog": {"wgerId": "1572"},
    "Dead Bug": {"wgerId": "2505", "freeExerciseDbId": "Dead_Bug"},
    "Superman": {"wgerId": "636", "freeExerciseDbId": "Superman"},
    "Front Plank": {"wgerId": "1001", "freeExerciseDbId": "Plank"},
    "Side Plank L": {"wgerId": "580", "freeExerciseDbId": "Side_Bridge"},
    "Side Plank R": {"wgerId": "580", "freeExerciseDbId": "Side_Bridge"},
    "Triceps Dip": {"wgerId": "194", "exerciseDbId": "exr_41n2hadQgEEX8wDN", "freeExerciseDbId": "Dips"},
    "Mountain Climbers": {"wgerId": "996", "freeExerciseDbId": "Mountain_Climbers"},
    "Punches": {"exerciseDbId": "exr_41n2hezAZ6CdkAcM"},
    "Hamstring Stretch L": {"wgerId": "1393", "freeExerciseDbId": "Hamstring_Stretch"},
    "Hamstring Stretch R": {"wgerId": "1393", "freeExerciseDbId": "Hamstring_Stretch"},
    "Quad Wall Stretch L": {"wgerId": "1873", "freeExerciseDbId": "Quad_Stretch"},
    "Quad Wall Stretch R": {"wgerId": "1873", "freeExerciseDbId": "Quad_Stretch"},
    "Hip Flexor Stretch L": {"wgerId": "1867", "freeExerciseDbId": "Kneeling_Hip_Flexor"},
    "Hip Flexor Stretch R": {"wgerId": "1867", "freeExerciseDbId": "Kneeling_Hip_Flexor"},
    "Calf Stretch L": {"wgerId": "1239", "freeExerciseDbId": "Calf_Stretch_Hands_Against_Wall"},
    "Calf Stretch R": {"wgerId": "1239", "freeExerciseDbId": "Calf_Stretch_Hands_Against_Wall"},
    "Doorway Chest Stretch": {"freeExerciseDbId": "Chest_And_Front_Of_Shoulder_Stretch"},
    "Cross Body Shoulder Stretch L": {"freeExerciseDbId": "Shoulder_Stretch"},
    "Cross Body Shoulder Stretch R": {"freeExerciseDbId": "Shoulder_Stretch"},
    "Upper Back Stretch": {"freeExerciseDbId": "Upper_Back_Stretch"},
    "Child's Pose": {"wgerId": "1002", "freeExerciseDbId": "Childs_Pose"},
    "Spinal Stretch": {"freeExerciseDbId": "Spinal_Stretch"},
}


def ex(name: str, *, reps: int | None = None, seconds: int | None = None, raw: str | None = None, media_name: str | None = None):
    assert (reps is None) != (seconds is None), name
    item = {"raw": raw or (f"{reps} {name}" if reps is not None else f"{seconds}s {name}"), "name": name}
    if reps is not None:
        item["reps"] = reps
    else:
        item["seconds"] = seconds
    media_key = media_name or name
    media = {**CATALOG_MEDIA.get(media_key, {}), **MEDIA.get(media_key, {})}
    assert media, f"Missing media for {name} (base {media_key})"
    item.update(media)
    return item


def side_ex(base_name: str, side: str, *, reps: int | None = None, seconds: int | None = None):
    return ex(f"{base_name} {side}", reps=reps, seconds=seconds, media_name=base_name)


def split_total_reps(base_name: str, total_reps: int):
    each = max(1, (total_reps + 1) // 2)
    return [side_ex(base_name, "L", reps=each), side_ex(base_name, "R", reps=each)]


def scale(value: int, factor: float, cap: int):
    return min(cap, max(1, round(value * factor)))


def warmup(day: int):
    # Curated per day. No exact warm-up exercise is used on more than two days/week.
    sets = {
        1: [
            ex("Arm Circle Forward", seconds=15), ex("Standing Hip Circles", seconds=20),
            ex("Inchworm", reps=4), ex("High Knees", reps=16),
        ],
        2: [
            ex("Arm Swing", seconds=20), ex("Torso Twist", seconds=20),
            ex("Walking Lunges", reps=8, raw="8 Walking Lunges · total"), ex("Shoulder Roll", seconds=20),
        ],
        3: [
            ex("Arm Circle Backward", seconds=15), ex("Cat Cow", seconds=25),
            ex("Standing Toe Touches", seconds=20), ex("Shoulder Circles", reps=8),
        ],
        4: [
            ex("Arm Circle Forward", seconds=15), ex("Cat Cow Stretch", seconds=25),
            ex("High Knees", reps=16), ex("SLOW Push-ups", reps=4),
        ],
        5: [
            ex("Arm Swing", seconds=20), ex("Standing Hip Circles", seconds=20),
            ex("Inchworm", reps=4), ex("Shoulder Roll", seconds=20),
        ],
        6: [
            ex("Arm Circle Backward", seconds=15), ex("Torso Twist", seconds=20),
            ex("Walking Lunges", reps=8, raw="8 Walking Lunges · total"), ex("Shoulder Circles", reps=8),
        ],
        7: [
            ex("Cat Cow", seconds=25), ex("Standing Toe Touches", seconds=20),
            ex("SLOW Push-ups", reps=4), ex("Mountain Climbers", reps=12, raw="12 Mountain Climbers · easy"),
        ],
    }
    return sets[day]


def stretch(day: int):
    # Different sequence every day. Hamstrings/posterior chain, torso and traps
    # get extra weekly attention through different movements, never daily cloning.
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


def blocks(day: int, f: float):
    """Seven deliberately different full-body days; mostly <=2 uses/exercise/week."""
    if day == 1:  # squat + push/pull + hinge
        return [
            [
                ex("Dumbbell Goblet Squat", reps=scale(8, f, 12)),
                ex("Push-ups", reps=scale(6, f, 10), raw=f"{scale(6, f, 10)} Push-ups · leave 2 reps in reserve"),
                ex("Dumbbell Row", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Dumbbell Rows · total"),
            ],
            [
                ex("Romanian Deadlift", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Romanian Deadlifts · controlled"),
                ex("Dumbbell Shoulder Press", reps=scale(6, f, 10)),
                ex("Dead Bug", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Dead Bugs · total"),
            ],
        ]
    if day == 2:  # lunge + back + posterior chain
        return [
            [
                ex("Dumbbell Walking Lunge", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Dumbbell Walking Lunges · total"),
                ex("Pike Push-ups", reps=scale(7, f, 10)),
                ex("Pull-Up", reps=scale(4, f, 8), raw=f"{scale(4, f, 8)} Pull-Ups · controlled"),
            ],
            [
                ex("Reverse Lunge", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Reverse Lunges · total"),
                ex("Glute Bridge March", reps=scale(10, f, 14), raw=f"{scale(10, f, 14)} Glute Bridge Marches · total"),
                ex("Bird Dog", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Bird Dogs · total"),
            ],
        ]
    if day == 3:  # hinge + chest + shoulder stability
        return [
            [
                ex("Romanian Deadlift", reps=scale(8, f, 12)),
                ex("Wide Push-up", reps=scale(7, f, 10)),
                ex("Dumbbell Row", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Dumbbell Rows · total"),
            ],
            [
                *split_total_reps("Single Leg Glute Bridge", scale(8, f, 12)),
                ex("Lateral Raise", reps=scale(8, f, 12)),
                ex("Side Plank L", seconds=scale(18, f, 25)),
                ex("Side Plank R", seconds=scale(18, f, 25)),
            ],
        ]
    if day == 4:  # easier recovery-strength day
        return [
            [
                ex("Squats", reps=8, raw="8 Easy Squats"),
                ex("Knee Push-ups", reps=6, raw="6 Easy Knee Push-ups"),
                ex("Superman", reps=8, raw="8 Superman · slow"),
            ],
            [
                ex("Glute Bridge", reps=10),
                ex("Calf Raises", reps=10),
                ex("Front Plank", seconds=20),
            ],
        ]
    if day == 5:  # second weighted strength day, different lower-body pattern
        return [
            [
                ex("Dumbbell Goblet Squat", reps=scale(8, f, 12)),
                ex("Push-ups", reps=scale(6, f, 10), raw=f"{scale(6, f, 10)} Push-ups · clean reps"),
                ex("Pull-Up", reps=scale(4, f, 8), raw=f"{scale(4, f, 8)} Pull-Ups · controlled"),
            ],
            [
                ex("Dumbbell Walking Lunge", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Dumbbell Walking Lunges · total"),
                ex("Dumbbell Shoulder Press", reps=scale(6, f, 10)),
                ex("Dead Bug", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Dead Bugs · total"),
            ],
        ]
    if day == 6:  # brisk full-body conditioning without repeating day 2
        return [
            [
                ex("Jumping Jacks", reps=scale(25, f, 35)),
                ex("Reverse Lunge", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Reverse Lunges · total"),
                ex("Wide Push-up", reps=scale(7, f, 10)),
            ],
            [
                ex("Mountain Climbers", reps=scale(16, f, 24), raw=f"{scale(16, f, 24)} Mountain Climbers · total"),
                ex("Glute Bridge March", reps=scale(10, f, 14), raw=f"{scale(10, f, 14)} Glute Bridge Marches · total"),
                ex("Bird Dog", reps=scale(8, f, 12), raw=f"{scale(8, f, 12)} Bird Dogs · total"),
            ],
        ]
    # day 7: easy posture / accessory day
    return [
        [
            ex("Squats", reps=8, raw="8 Easy Squats"),
            ex("Diamond Push-up", reps=scale(6, f, 10)),
            ex("Superman", reps=8, raw="8 Superman · slow"),
        ],
        [
            *split_total_reps("Single Leg Glute Bridge", scale(8, f, 12)),
            ex("Dumbbell Bicep Curl", reps=scale(8, f, 12)),
            ex("Front Plank", seconds=20),
        ],
    ]


# Small progression only. The time budget stays fixed; progression comes from
# better form and gradually heavier dumbbells, not endlessly adding exercises.
FACTORS = {1: .90, 2: .95, 3: 1.00, 4: .90, 5: 1.00, 6: 1.05, 7: 1.05, 8: .90, 9: 1.05, 10: 1.10, 11: 1.10, 12: 1.00}


def workout(day: int, factor: float):
    rep1, rep2 = blocks(day, factor)
    return {
        "index": day,
        "estimatedMinutes": 15,
        "sections": [
            {"title": "Warm-up", "exercises": warmup(day)},
            {"title": "Rep 1", "exercises": rep1},
            {"title": "Rep 2", "exercises": rep2},
            {"title": "Stretching", "exercises": stretch(day)},
        ],
    }


def build_program():
    return {
        "id": PROGRAM_ID,
        "title": "Full Body · 15 min · Weights",
        "level": "INTERMEDIATE",
        "focusAreas": ["FULL_BODY", "STRENGTH", "CORE"],
        "equipment": ["HOME"],
        "sessionMinutes": 15,
        "weeks": [
            {"number": week, "workouts": [workout(day, FACTORS[week]) for day in range(1, 8)]}
            for week in range(1, 13)
        ],
    }


def validate(program):
    assert len(program["weeks"]) == 12
    for week in program["weeks"]:
        assert len(week["workouts"]) == 7
        for work in week["workouts"]:
            assert work["estimatedMinutes"] == 15
            assert [s["title"].split(" · ")[0] for s in work["sections"]] == ["Warm-up", "Rep 1", "Rep 2", "Stretching"]
            for section in work["sections"]:
                assert len(section["exercises"]) <= 8
                for item in section["exercises"]:
                    assert any(k in item for k in ("wgerId", "exerciseDbId", "freeExerciseDbId", "bundledMediaAsset", "externalMediaUrl")), item["name"]
            main_names = [e["name"] for section in work["sections"][1:3] for e in section["exercises"]]
            assert all(a != b for a, b in zip(main_names, main_names[1:])), (week["number"], work["index"])
        exercise_days = {}
        for work in week["workouts"]:
            for section in work["sections"]:
                for item in section["exercises"]:
                    exercise_days.setdefault(item["name"], set()).add(work["index"])
        too_frequent = {name: sorted(days) for name, days in exercise_days.items() if len(days) > 2}
        assert not too_frequent, too_frequent


def main():
    plan = build_program()
    validate(plan)
    plan_text = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    for directory in PROGRAM_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "program-2.json").write_text(plan_text, encoding="utf-8")

        index_path = directory / "index.json"
        index = json.loads(index_path.read_text(encoding="utf-8"))
        existing = [p for p in index.get("programs", []) if p.get("id") != PROGRAM_ID]
        existing.append({
            "id": PROGRAM_ID,
            "title": plan["title"],
            "level": plan["level"],
            "focusAreas": plan["focusAreas"],
            "equipment": plan["equipment"],
            "weeks": 12,
            "file": "programs/program-2.json",
            "sessionMinutes": 15,
        })
        index_path.write_text(json.dumps({"programs": existing}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Added program-2: Full Body · 15 min · Weights (12 weeks × 7 days).")


if __name__ == "__main__":
    main()
