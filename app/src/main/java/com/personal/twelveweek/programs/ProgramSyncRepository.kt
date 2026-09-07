package com.personal.twelveweek.programs

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.Cache
import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.File
import java.io.IOException

/**
 * Pulls the program library from the public GitHub repo
 * (`pankaj4u4m/12-weeks-workout`) over plain HTTPS via
 * raw.githubusercontent.com — the repo is public, so no auth token is needed.
 * Runs once on every app launch (see AppRoot); best-effort and silent on
 * failure — offline or a dead network just means the last-synced (or
 * bundled-asset) copy keeps being used, never a crash or a blocking spinner.
 */
class ProgramSyncRepository(
    private val client: OkHttpClient,
    private val library: ProgramLibrary,
    private val baseRawUrl: String =
        "https://raw.githubusercontent.com/pankaj4u4m/12-weeks-workout/main"
) {
suspend fun sync() = withContext(Dispatchers.IO) {
        val indexJson = fetch("$baseRawUrl/programs/index.json") ?: return@withContext
        val entries = runCatching { parseIndex(indexJson) }.getOrDefault(emptyList())
        // Only accept the three curated plans. Ignore older remote indexes so stale
        // generated libraries can never repopulate the removed plan explosion.
        if (entries.map { it.meta.id }.toSet() != setOf("program-1", "program-2", "program-3")) return@withContext
        // Fetch the set atomically: a partial/stale remote library must never
        // overwrite the bundled media-complete plans one file at a time.
        val fetchedFiles = mutableMapOf<String, String>()
        entries.forEach { entry ->
            val programJson = fetch("$baseRawUrl/${entry.file}") ?: return@withContext
            fetchedFiles["${entry.meta.id}.json"] = programJson
        }

        // The current curated library guarantees bundled no-key media, encodes
        // recovery as section metadata (never a fake Pause exercise), and makes
        // genuinely one-sided movements explicit L/R pairs in the same section.
        // Reject an older remote snapshot until those invariants are present.
        if (fetchedFiles.values.any { "\"bundledMediaAsset\"" !in it }) return@withContext
        if (fetchedFiles.values.any { !remoteProgramMeetsCurrentInvariants(it) }) return@withContext

        fetchedFiles.forEach { (name, content) -> library.writeCache(name, content) }
        library.writeCache("index.json", indexJson)
    }


    private fun remoteProgramMeetsCurrentInvariants(json: String): Boolean {
        val program = runCatching { parseProgram(json) }.getOrNull() ?: return false
        val sideSpecific = setOf(
            "Hamstring Stretch", "Calf Stretch", "Hip Flexor Stretch",
            "Cross Body Shoulder Stretch", "Quad Wall Stretch", "Wall Pectoral Stretch",
            "Side Plank", "Pigeon Pose", "Side Stretch", "Side-Lying Floor Stretch",
            "Knee to Chest Stretch", "Side Lunge Stretch", "Clamshell", "Donkey Kicks",
            "Single Leg Calf Raise", "Single Leg Glute Bridge", "Static Lunge",
            "Split Squats", "Pallof Press"
        )
        val forbiddenEquipmentTokens = listOf(
            "cable", "barbell", "bench press", "step-up", "step up",
            "incline push", "hip thrust", "triceps dip", "machine", "smith", "leg press"
        )
        if (program.meta.equipment.toSet() != setOf(Equipment.HOME)) return false
        if (program.meta.id == "program-3" && program.weeks.any { week ->
                week.workouts.any { workout -> workout.sections.any { it.title == "Rep 3" } }
            }) return false
        if (!plan3HasBalancedRepPatterns(program)) return false
        return program.weeks.all { week ->
            week.workouts.all { workout ->
                workout.sections.all { section ->
                    val names = section.exercises.map { it.name }.toSet()
                    section.exercises.none { it.isRest } &&
                        section.exercises.all { exercise ->
                            (exercise.seconds ?: 0) <= 90 &&
                                forbiddenEquipmentTokens.none { token -> token in exercise.name.lowercase() }
                        } &&
                        sideSpecific.all { base ->
                            base !in names && (("$base L" in names) == ("$base R" in names))
                        }
                }
            }
        }
    }
    private fun plan3HasBalancedRepPatterns(program: LibraryProgram): Boolean {
        if (program.meta.id != "program-3") return true
        val expected = listOf("lower", "push", "pull", "posterior_core")
        return program.weeks.all { week ->
            week.workouts.all { workout ->
                val reps = workout.sections.filter { it.title == "Rep 1" || it.title == "Rep 2" }
                reps.size == 2 && reps.all { section ->
                    val collapsed = buildList {
                        section.exercises.forEach { exercise ->
                            val base = exercise.name.removeSuffix(" L").removeSuffix(" R")
                            if (lastOrNull() != base) add(base)
                        }
                    }
                    collapsed.size == 4 && collapsed.map { movementPattern(it) } == expected
                }
            }
        }
    }
    private fun movementPattern(name: String): String? = when (name) {
        "Dumbbell Goblet Squat", "Reverse Lunge", "Static Lunge", "Wall Sit", "Sumo Squats" -> "lower"
        "Push-ups", "Dumbbell Shoulder Press", "Pike Push-ups", "Wide Push-up", "Knee Push-ups" -> "push"
        "Dumbbell Row", "Pull-Up", "Rear Delt Fly", "Upright Row" -> "pull"
        "Romanian Deadlift", "Glute Bridge", "Single Leg Glute Bridge", "Glute Bridge March", "Bird Dog", "Dead Bug" -> "posterior_core"
        else -> null
    }

    private fun fetch(url: String): String? = runCatching {
        val request = Request.Builder().url(url).get().build()
        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) null else response.body?.string()
        }
    }.getOrNull()

    companion object {
        /** Composition-root factory, same pattern as ExerciseMediaRepository.default(). */
        fun default(context: Context, library: ProgramLibrary): ProgramSyncRepository {
            val cacheDir = File(context.cacheDir, "program_sync_http")
            val client = OkHttpClient.Builder()
                .cache(Cache(cacheDir, 10L * 1024 * 1024))
                .build()
            return ProgramSyncRepository(client, library)
        }
    }
}
