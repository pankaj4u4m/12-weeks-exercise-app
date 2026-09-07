package com.personal.twelveweek.programs

import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

/**
 * Guards against silent media gaps: every exercise name used anywhere in
 * the bundled program library, and every entry in the rotation catalog,
 * must have at least one real media identifier — or be "Pause", the only
 * intentional exception (rest, not a movement). Reads the actual repo files
 * on disk; this test lives in app/src/test (JVM-only) rather than
 * commonTest specifically so it can use java.io.File — see ProgramJsonTest
 * in commonTest for the equivalent parsing-behavior tests using inline JSON.
 */
class ExerciseCatalogCompletenessTest {

    // Exercises with no real matching media after searching wger, RapidAPI ExerciseDB,
    // free-exercise-db, and Wikimedia Commons (Task 2). These are niche compound
    // movements with genuinely unavailable media — accepted outcome per plan spec.
    private val INTENTIONALLY_UNMATCHED = setOf(
        "Curtsy Lunge",
        "Side Plank with Rotation L",
        "Side Plank with Rotation R",
        "Single-Arm Plank L",
        "Single-Arm Plank R",
        "Skater Jumps"
    )

    private val SIDE_SPECIFIC_BASES = setOf(
        "Hamstring Stretch", "Calf Stretch", "Hip Flexor Stretch",
        "Cross Body Shoulder Stretch", "Quad Wall Stretch", "Wall Pectoral Stretch",
        "Side Plank", "Pigeon Pose", "Side Stretch", "Side-Lying Floor Stretch",
        "Knee to Chest Stretch", "Side Lunge Stretch", "Clamshell", "Donkey Kicks",
        "Single Leg Calf Raise", "Single Leg Glute Bridge", "Static Lunge",
        "Split Squats", "Pallof Press"
    )

    private val FORBIDDEN_HOME_EQUIPMENT_TOKENS = listOf(
        "cable", "barbell", "bench press", "step-up", "step up",
        "incline push", "hip thrust", "triceps dip", "machine", "smith", "leg press"
    )

    // Gradle's working directory for `:app:test` is the `app/` module dir;
    // walk up one level to the repo root where `programs/` lives. If a
    // different Gradle version changes this, adjust here (print
    // `repoRoot.absolutePath` while debugging).
    private val repoRoot = File(System.getProperty("user.dir")).let {
        if (it.name == "app") it.parentFile!! else it
    }

    private fun hasMedia(obj: JsonObject): Boolean =
        listOf("wgerId", "exerciseDbId", "freeExerciseDbId", "bundledMediaAsset", "externalMediaUrl")
            .any { key -> obj[key]?.jsonPrimitive?.contentOrNull != null }

    @Test
    fun `every exercise name in every bundled program has real media or is Pause`() {
        val programsDir = File(repoRoot, "programs")
        val programFiles = programsDir.listFiles { f -> f.name.endsWith(".json") && f.name != "index.json" }
            ?: error("No program files found under $programsDir")
        assertTrue("Expected bundled programs, found none", programFiles.isNotEmpty())

        val gaps = mutableListOf<String>()
        for (file in programFiles) {
            val program = Json.parseToJsonElement(file.readText()).jsonObject
            for (week in program["weeks"]!!.jsonArray) {
                for (workout in week.jsonObject["workouts"]!!.jsonArray) {
                    for (section in workout.jsonObject["sections"]!!.jsonArray) {
                        for (exercise in section.jsonObject["exercises"]!!.jsonArray) {
                            val obj = exercise.jsonObject
                            val name = obj["name"]!!.jsonPrimitive.content
                            if (name == "Pause" || name in INTENTIONALLY_UNMATCHED) continue
                            if (!hasMedia(obj)) gaps.add("${file.name}: $name")
                        }
                    }
                }
            }
        }
        assertTrue(
            "Exercises with no media match (add to CREDITS.md / catalog): ${gaps.distinct()}",
            gaps.isEmpty()
        )
    }

    @Test
    fun `rest is metadata and never encoded as an exercise`() {
        val programsDir = File(repoRoot, "programs")
        val programFiles = programsDir.listFiles { f -> f.name.endsWith(".json") && f.name != "index.json" }
            ?: error("No program files found under $programsDir")
        val pauseRows = mutableListOf<String>()
        for (file in programFiles) {
            val program = Json.parseToJsonElement(file.readText()).jsonObject
            for (week in program["weeks"]!!.jsonArray) {
                for (workout in week.jsonObject["workouts"]!!.jsonArray) {
                    for (section in workout.jsonObject["sections"]!!.jsonArray) {
                        for (exercise in section.jsonObject["exercises"]!!.jsonArray) {
                            val name = exercise.jsonObject["name"]!!.jsonPrimitive.content
                            if (name.equals("Pause", ignoreCase = true)) {
                                pauseRows += "${file.name}: week=${week.jsonObject["number"]} day=${workout.jsonObject["index"]} section=${section.jsonObject["title"]}"
                            }
                        }
                    }
                }
            }
        }
        assertTrue("Pause/rest must use section restAfterSeconds, not exercise rows: $pauseRows", pauseRows.isEmpty())
    }

    @Test
    fun `one-sided movements are explicit paired L and R exercises`() {
        val programsDir = File(repoRoot, "programs")
        val programFiles = programsDir.listFiles { f -> f.name.endsWith(".json") && f.name != "index.json" }
            ?: error("No program files found under $programsDir")
        val issues = mutableListOf<String>()
        for (file in programFiles) {
            val program = Json.parseToJsonElement(file.readText()).jsonObject
            for (week in program["weeks"]!!.jsonArray) {
                for (workout in week.jsonObject["workouts"]!!.jsonArray) {
                    for (section in workout.jsonObject["sections"]!!.jsonArray) {
                        val names = section.jsonObject["exercises"]!!.jsonArray
                            .map { it.jsonObject["name"]!!.jsonPrimitive.content }
                            .toSet()
                        for (base in SIDE_SPECIFIC_BASES) {
                            if (base in names) issues += "${file.name}: unsuffixed $base"
                            val hasL = "$base L" in names
                            val hasR = "$base R" in names
                            if (hasL != hasR) issues += "${file.name}: orphan side for $base"
                        }
                    }
                }
            }
        }
        assertTrue("Side-specific exercises must appear as paired L/R rows: $issues", issues.isEmpty())
    }

    @Test
    fun `no timed exercise exceeds 90 seconds`() {
        val programsDir = File(repoRoot, "programs")
        val programFiles = programsDir.listFiles { f -> f.name.endsWith(".json") && f.name != "index.json" }
            ?: error("No program files found under $programsDir")
        val overLimit = mutableListOf<String>()
        for (file in programFiles) {
            val program = Json.parseToJsonElement(file.readText()).jsonObject
            for (week in program["weeks"]!!.jsonArray) {
                for (workout in week.jsonObject["workouts"]!!.jsonArray) {
                    for (section in workout.jsonObject["sections"]!!.jsonArray) {
                        for (exercise in section.jsonObject["exercises"]!!.jsonArray) {
                            val obj = exercise.jsonObject
                            val seconds = obj["seconds"]?.jsonPrimitive?.contentOrNull?.toIntOrNull() ?: continue
                            if (seconds > 90) {
                                overLimit += "${file.name}: week=${week.jsonObject["number"]} day=${workout.jsonObject["index"]} section=${section.jsonObject["title"]} ${obj["name"]}=${seconds}s"
                            }
                        }
                    }
                }
            }
        }
        assertTrue("Timed exercises must be <= 90 seconds: $overLimit", overLimit.isEmpty())
    }

    @Test
    fun `bundled plans only use the available home equipment`() {
        val programsDir = File(repoRoot, "programs")
        val programFiles = programsDir.listFiles { f -> f.name.endsWith(".json") && f.name != "index.json" }
            ?: error("No program files found under $programsDir")
        val issues = mutableListOf<String>()
        for (file in programFiles) {
            val program = Json.parseToJsonElement(file.readText()).jsonObject
            val equipment = program["equipment"]!!.jsonArray.map { it.jsonPrimitive.content }
            if (equipment != listOf("HOME")) issues += "${file.name}: equipment=$equipment"
            for (week in program["weeks"]!!.jsonArray) {
                for (workout in week.jsonObject["workouts"]!!.jsonArray) {
                    for (section in workout.jsonObject["sections"]!!.jsonArray) {
                        for (exercise in section.jsonObject["exercises"]!!.jsonArray) {
                            val name = exercise.jsonObject["name"]!!.jsonPrimitive.content
                            if (FORBIDDEN_HOME_EQUIPMENT_TOKENS.any { token -> token in name.lowercase() }) {
                                issues += "${file.name}: unsupported equipment exercise $name"
                            }
                        }
                    }
                }
            }
        }
        assertTrue("Bundled plans must match dumbbells + mat + push-up bars + pull-up bar: $issues", issues.isEmpty())
    }

    @Test
    fun `program 3 has exactly two rep sections`() {
        val file = File(repoRoot, "programs/program-3.json")
        val program = Json.parseToJsonElement(file.readText()).jsonObject
        val issues = mutableListOf<String>()
        for (week in program["weeks"]!!.jsonArray) {
            for (workout in week.jsonObject["workouts"]!!.jsonArray) {
                val titles = workout.jsonObject["sections"]!!.jsonArray
                    .map { it.jsonObject["title"]!!.jsonPrimitive.content }
                if (titles != listOf("Warm-up", "Rep 1", "Rep 2", "Stretching")) {
                    issues += "week=${week.jsonObject["number"]} day=${workout.jsonObject["index"]}: $titles"
                }
            }
        }
        assertTrue("Program 3 must have two reps only: $issues", issues.isEmpty())
    }

    @Test
    fun `every catalog entry has real media or is explicitly excluded`() {
        val catalogFile = File(repoRoot, "programs/_pools/exercise-catalog.json")
        assertTrue("Catalog not found at $catalogFile", catalogFile.exists())
        val catalog = Json.parseToJsonElement(catalogFile.readText()).jsonObject
        val gaps = catalog["exercises"]!!.jsonArray
            .map { it.jsonObject }
            .filterNot { hasMedia(it) || it["name"]!!.jsonPrimitive.content in INTENTIONALLY_UNMATCHED }
            .map { it["name"]!!.jsonPrimitive.content }
        assertTrue("Catalog entries with no media match: $gaps", gaps.isEmpty())
    }

    @Test
    fun `every bundled media asset exists for android and web`() {
        val catalogFile = File(repoRoot, "programs/_pools/exercise-catalog.json")
        val catalog = Json.parseToJsonElement(catalogFile.readText()).jsonObject
        val referencedAssets = catalog["exercises"]!!.jsonArray
            .map { it.jsonObject }
            .mapNotNull { it["bundledMediaAsset"]?.jsonPrimitive?.contentOrNull }
            .toSet()

        val androidDir = File(repoRoot, "app/src/main/assets/exercise_media")
        val webDir = File(repoRoot, "app/src/wasmJsMain/resources/exercise_media")
        val missing = referencedAssets.flatMap { asset ->
            buildList {
                if (!File(androidDir, asset).isFile) add("android:$asset")
                if (!File(webDir, asset).isFile) add("web:$asset")
            }
        }
        assertTrue("Bundled media files missing: $missing", missing.isEmpty())
    }
}
