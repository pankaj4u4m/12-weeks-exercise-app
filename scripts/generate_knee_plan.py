#!/usr/bin/env python3
"""Generate a 30-minute weighted full-body plan that is knee-friendly and exactly timed."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM_DIRS = [
    ROOT / "programs",
    ROOT / "app/src/main/assets/programs",
    ROOT / "app/src/wasmJsMain/resources/programs",
]
PROGRAM_ID = "program-3"
TARGET_SECONDS = 30 * 60
SECONDS_PER_REP_NUMERATOR = 5  # 2.5 seconds/rep, expressed exactly as 5/2.
REP_PREP_SECONDS = 3
TRANSITION_SECONDS = 5
ROUNDS = 2

CATALOG_MEDIA = {
    e["name"]: {k: e[k] for k in ("wgerId", "exerciseDbId", "freeExerciseDbId", "bundledMediaAsset", "externalMediaUrl") if e.get(k)}
    for e in json.loads((ROOT / "programs/_pools/exercise-catalog.json").read_text(encoding="utf-8"))["exercises"]
}


def ex(name: str, *, reps: int | None = None, seconds: int | None = None, raw: str | None = None, media_name: str | None = None):
    assert (reps is None) != (seconds is None), name
    item = {
        "raw": raw or (f"{reps} {name}" if reps is not None else f"{seconds}s {name}"),
        "name": name,
    }
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


def scale(value: int, factor: float, cap: int):
    return min(cap, max(1, int(value * factor + 0.5)))


def per_side(name: str, base: int, factor: float, cap: int, note: str = ""):
    each = scale(base, factor, cap)
    suffix = f" · {note}" if note else ""
    # reps is TOTAL reps because the guided timer allocates 2.5 seconds per rep.
    return ex(name, reps=each * 2, raw=f"{each}/side {name}{suffix}")


def kotlin_rep_seconds(reps: int) -> int:
    # Kotlin roundToInt() for positive reps: n*2.5, .5 rounds upward.
    return (reps * SECONDS_PER_REP_NUMERATOR + 1) // 2


def active_step_seconds(item: dict) -> int:
    if "reps" in item:
        return kotlin_rep_seconds(item["reps"]) + REP_PREP_SECONDS
    return item["seconds"]


def runtime_seconds(sections: list[dict]) -> int:
    """Actual guided-session wall time, including section recovery metadata."""
    exercise_steps = [item for section in sections for item in section["exercises"]]
    rest_steps = sum(1 for section in sections if section.get("restAfterSeconds", 0) > 0)
    total_steps = len(exercise_steps) + rest_steps
    if total_steps == 0:
        return 0
    exercise_seconds = sum(active_step_seconds(item) for item in exercise_steps)
    rest_seconds = sum(section.get("restAfterSeconds", 0) for section in sections)
    return exercise_seconds + rest_seconds + (total_steps - 1) * TRANSITION_SECONDS


def training_seconds(sections: list[dict]) -> int:
    """Displayed workout duration: wall time excluding explicit recovery."""
    rest_seconds = sum(section.get("restAfterSeconds", 0) for section in sections)
    return runtime_seconds(sections) - rest_seconds


def warmup(day: int):
    # Four warm-up movements every day, 25 seconds each.
    # No exact movement appears on >2 days/week.
    sets = {
        1: [ex("Standing Hip Circles", seconds=25), ex("Arm Circle Forward", seconds=25), ex("Torso Twist", seconds=25), ex("Shoulder Roll", seconds=25)],
        2: [ex("Cat Cow", seconds=25), ex("Arm Swing", seconds=25), ex("Wall Pectoral Stretch L", seconds=25), ex("Wall Pectoral Stretch R", seconds=25)],
        3: [ex("Arm Circle Backward", seconds=25), ex("Standing Toe Touches", seconds=25, raw="25s Standing Toe Touches · gentle"), ex("Shoulder Circles", seconds=25), ex("SLOW Push-ups", seconds=25, raw="25s SLOW Push-ups · controlled")],
        4: [ex("Cat Cow Stretch", seconds=25), ex("Torso Twist", seconds=25), ex("Dynamic Chest Stretch", seconds=25), ex("Arm Circle Forward", seconds=25)],
        5: [ex("Standing Hip Circles", seconds=25), ex("Arm Swing", seconds=25), ex("Shoulder Roll", seconds=25), ex("SLOW Push-ups", seconds=25, raw="25s SLOW Push-ups · controlled")],
        6: [ex("Cat Cow", seconds=25), ex("Arm Circle Backward", seconds=25), ex("Doorway Chest Stretch", seconds=25), ex("Shoulder Circles", seconds=25)],
        7: [ex("Inchworm", seconds=25, raw="25s Inchworm · slow"), ex("Standing Toe Touches", seconds=25, raw="25s Standing Toe Touches · gentle"), ex("Cat Cow Stretch", seconds=25), ex("Chest And Front Of Shoulder Stretch", seconds=25)],
    }
    return sets[day]


def stretching(day: int):
    # Six stretches every day, 40 seconds each. Exact stretches are capped at two days/week.
    sets = {
        1: [ex("Hamstring Stretch L", seconds=40), ex("Hamstring Stretch R", seconds=40), ex("Calf Stretch L", seconds=40), ex("Calf Stretch R", seconds=40), ex("Upper Back Stretch", seconds=40), ex("Torso Rotation Stretch", seconds=40)],
        2: [ex("Hip Flexor Stretch L", seconds=40), ex("Hip Flexor Stretch R", seconds=40), ex("Butterfly Stretch", seconds=40), side_ex("Pigeon Pose", "L", seconds=40), side_ex("Pigeon Pose", "R", seconds=40), side_ex("Side Stretch", "L", seconds=40), side_ex("Side Stretch", "R", seconds=40), ex("Spinal Stretch", seconds=40)],
        3: [ex("Downward Facing Dog", seconds=40), ex("Child's Pose", seconds=40), ex("Cross Body Shoulder Stretch L", seconds=40), ex("Cross Body Shoulder Stretch R", seconds=40), ex("Quad Wall Stretch L", seconds=40), ex("Quad Wall Stretch R", seconds=40)],
        4: [ex("Hamstring Stretch L", seconds=40), ex("Hamstring Stretch R", seconds=40), ex("Hip Flexor Stretch L", seconds=40), ex("Hip Flexor Stretch R", seconds=40), side_ex("Side-Lying Floor Stretch", "L", seconds=40), side_ex("Side-Lying Floor Stretch", "R", seconds=40), ex("Upper Back Stretch", seconds=40)],
        5: [ex("Calf Stretch L", seconds=40), ex("Calf Stretch R", seconds=40), ex("Butterfly Stretch", seconds=40), side_ex("Pigeon Pose", "L", seconds=40), side_ex("Pigeon Pose", "R", seconds=40), ex("Torso Rotation Stretch", seconds=40), side_ex("Side Stretch", "L", seconds=40), side_ex("Side Stretch", "R", seconds=40)],
        6: [ex("Spinal Stretch", seconds=40), ex("Downward Facing Dog", seconds=40), ex("Cross Body Shoulder Stretch L", seconds=40), ex("Cross Body Shoulder Stretch R", seconds=40), side_ex("Side-Lying Floor Stretch", "L", seconds=40), side_ex("Side-Lying Floor Stretch", "R", seconds=40), ex("Child's Pose", seconds=40)],
        7: [ex("Quad Wall Stretch L", seconds=40), ex("Quad Wall Stretch R", seconds=40), ex("Wall Pectoral Stretch L", seconds=40), ex("Wall Pectoral Stretch R", seconds=40), ex("Hug Knees To Chest", seconds=40), side_ex("Knee to Chest Stretch", "L", seconds=40), side_ex("Knee to Chest Stretch", "R", seconds=40)],
    }
    return sets[day]


def main_move_names(day: int):
    """Four movements per day: one knee/lower pattern, one push, one pull, one posterior/core pattern."""
    sets = {
        1: ["Dumbbell Goblet Squat", "Push-ups", "Dumbbell Row", "Romanian Deadlift"],
        2: ["Reverse Lunge", "Dumbbell Shoulder Press", "Pull-Up", "Glute Bridge"],
        3: ["Static Lunge", "Pike Push-ups", "Pull-Up", "Single Leg Glute Bridge"],
        4: ["Wall Sit", "Wide Push-up", "Rear Delt Fly", "Romanian Deadlift"],
        5: ["Dumbbell Goblet Squat", "Dumbbell Shoulder Press", "Dumbbell Row", "Glute Bridge March"],
        6: ["Reverse Lunge", "Knee Push-ups", "Upright Row", "Bird Dog"],
        7: ["Sumo Squats", "Wide Push-up", "Rear Delt Fly", "Dead Bug"],
    }
    return sets[day]


SIDE_SPECIFIC_TIMED = {"Static Lunge", "Single Leg Glute Bridge", "Pallof Press"}

MOVEMENT_PATTERN = {
    "Dumbbell Goblet Squat": "lower",
    "Reverse Lunge": "lower",
    "Static Lunge": "lower",
    "Wall Sit": "lower",
    "Sumo Squats": "lower",
    "Push-ups": "push",
    "Dumbbell Shoulder Press": "push",
    "Pike Push-ups": "push",
    "Wide Push-up": "push",
    "Knee Push-ups": "push",
    "Dumbbell Row": "pull",
    "Pull-Up": "pull",
    "Rear Delt Fly": "pull",
    "Upright Row": "pull",
    "Romanian Deadlift": "posterior_core",
    "Glute Bridge": "posterior_core",
    "Single Leg Glute Bridge": "posterior_core",
    "Glute Bridge March": "posterior_core",
    "Bird Dog": "posterior_core",
    "Dead Bug": "posterior_core",
}


def base_exercise_name(name: str) -> str:
    return name[:-2] if name.endswith((" L", " R")) else name


def timed_work(name: str, seconds: int, *, media_name: str | None = None):
    base_name = media_name or name
    notes = {
        "Static Lunge": "shallow pain-free range",
        "Wall Sit": "comfortable knee angle",
        "Reverse Lunge": "shallow pain-free range; alternate sides",
        "Dumbbell Shoulder Press": "controlled reps; leave 2 reps in reserve",
        "Push-ups": "clean controlled reps",
        "Pike Push-ups": "controlled reps; keep shoulders stable",
        "Wide Push-up": "controlled reps; keep body aligned",
        "Knee Push-ups": "controlled reps; keep body aligned",
        "Dumbbell Row": "use both dumbbells; controlled pull",
        "Pull-Up": "controlled pull; stop before form breaks",
        "Rear Delt Fly": "light dumbbells; squeeze shoulder blades",
        "Upright Row": "light dumbbells; controlled pull",
        "Romanian Deadlift": "light-to-moderate load; controlled hinge",
        "Single Leg Glute Bridge": "controlled single-side reps",
        "Glute Bridge": "controlled reps; pause at the top",
        "Glute Bridge March": "alternate sides slowly; keep hips level",
        "Bird Dog": "alternate sides slowly",
        "Plank Reach": "stay square; move slowly",
        "Dead Bug": "keep lower back controlled",
    }
    note = notes.get(base_name, "controlled reps")
    return ex(name, seconds=seconds, raw=f"{seconds}s {name} · {note}", media_name=base_name)


def timed_work_items(name: str, seconds: int):
    if name not in SIDE_SPECIFIC_TIMED:
        return [timed_work(name, seconds)]
    each = seconds // 2
    return [
        timed_work(f"{name} L", each, media_name=name),
        timed_work(f"{name} R", each, media_name=name),
    ]


FACTORS = {
    1: .85, 2: .90, 3: .95, 4: .85,
    5: .95, 6: 1.00, 7: 1.00, 8: .90,
    9: 1.00, 10: 1.05, 11: 1.10, 12: .95,
}


def build_round_sections(day: int, factor: float):
    del factor  # progression is load/form; the session structure stays stable.
    move_names = main_move_names(day)

    # Four identical movements are repeated in Rep 1, Rep 2 and Rep 3.
    # Main work is a clean 90 seconds per movement. Recovery is section
    # metadata, never an exercise row: 60s after warm-up and after every rep.
    sections = [
        {"title": "Warm-up", "exercises": warmup(day), "restAfterSeconds": 60},
    ]
    for round_index in range(ROUNDS):
        items = []
        for name in move_names:
            items.extend(timed_work_items(name, 90))
        sections.append({
            "title": f"Rep {round_index + 1}",
            "exercises": items,
            "restAfterSeconds": 60,
        })
    sections.append({"title": "Stretching", "exercises": stretching(day)})

    training = training_seconds(sections)
    assert runtime_seconds(sections) == training + 3 * 60
    return sections


def workout(day: int, factor: float):
    sections = build_round_sections(day, factor)
    training = training_seconds(sections)
    return {
        "index": day,
        "sections": sections,
        "estimatedMinutes": round(training / 60),
    }


def build_program():
    return {
        "id": PROGRAM_ID,
        "title": "Knee-Friendly Full Body · Weights",
        "level": "INTERMEDIATE",
        "focusAreas": ["FULL_BODY", "LEGS", "STRENGTH", "CORE", "UPPER_BODY"],
        "equipment": ["HOME"],
        "sessionMinutes": 20,
        "weeks": [
            {"number": week, "workouts": [workout(day, FACTORS[week]) for day in range(1, 8)]}
            for week in range(1, 13)
        ],
    }


def validate(program):
    assert len(program["weeks"]) == 12
    for week in program["weeks"]:
        assert len(week["workouts"]) == 7
        days_by_exercise: dict[str, set[int]] = defaultdict(set)
        for work in week["workouts"]:
            training = training_seconds(work["sections"])
            assert runtime_seconds(work["sections"]) == training + 3 * 60
            assert work["estimatedMinutes"] == round(training / 60)
            assert [s["title"] for s in work["sections"]] == ["Warm-up", "Rep 1", "Rep 2", "Stretching"]
            assert len(work["sections"][0]["exercises"]) == 4
            assert len(work["sections"][-1]["exercises"]) >= 6
            assert all(
                item["name"] != "Pause"
                for section in work["sections"]
                for item in section["exercises"]
            )
            assert [section.get("restAfterSeconds", 0) for section in work["sections"]] == [60, 60, 60, 0]
            rep_names = [
                [item["name"] for item in section["exercises"]]
                for section in work["sections"][1:3]
            ]
            assert rep_names[0] == rep_names[1], rep_names
            for section in work["sections"][1:3]:
                collapsed = []
                for item in section["exercises"]:
                    base_name = base_exercise_name(item["name"])
                    if not collapsed or collapsed[-1] != base_name:
                        collapsed.append(base_name)
                    expected_seconds = 45 if base_name in SIDE_SPECIFIC_TIMED else 90
                    assert item.get("seconds") == expected_seconds, item
                assert len(collapsed) == 4, collapsed
                assert [MOVEMENT_PATTERN[name] for name in collapsed] == [
                    "lower", "push", "pull", "posterior_core"
                ], collapsed
            for section in work["sections"]:
                for item in section["exercises"]:
                    if item["name"] != "Pause":
                        assert any(k in item for k in ("wgerId", "exerciseDbId", "freeExerciseDbId", "bundledMediaAsset", "externalMediaUrl")), item["name"]
                        days_by_exercise[item["name"]].add(work["index"])
        overused = {name: sorted(days) for name, days in days_by_exercise.items() if len(days) > 2}
        assert not overused, overused


def main():
    plan = build_program()
    validate(plan)
    plan_text = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    for directory in PROGRAM_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "program-3.json").write_text(plan_text, encoding="utf-8")
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
            "file": "programs/program-3.json",
            "sessionMinutes": plan["sessionMinutes"],
        })
        index_path.write_text(json.dumps({"programs": existing}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Generated program-3: {plan['title']}")
    for workout_row in plan["weeks"][0]["workouts"]:
        rests = [s.get("restAfterSeconds", 0) for s in workout_row["sections"] if s.get("restAfterSeconds", 0) > 0]
        work_seconds = [e["seconds"] for s in workout_row["sections"] if s["title"].startswith("Rep ") for e in s["exercises"]]
        print(f"Day {workout_row['index']}: training {training_seconds(workout_row['sections'])}s; wall {runtime_seconds(workout_row['sections'])}s; 4 warm-ups; 4 moves × 2 reps; work {min(work_seconds)}-{max(work_seconds)}s; rests {rests}; {len(workout_row['sections'][-1]['exercises'])} stretches")


if __name__ == "__main__":
    main()
