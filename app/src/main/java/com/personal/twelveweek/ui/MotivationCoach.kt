package com.personal.twelveweek.ui

/** One professional coaching cue, optionally scoped to one or more programs. */
data class MotivationalLine(
    val text: String,
    val tags: Set<String>,
    val programs: Set<String> = emptySet()
)

private const val GENERAL = "general"
private const val WARMUP = "warmup"
private const val STRENGTH = "strength"
private const val STRETCH = "stretch"
private const val REST = "rest"
private const val LATE = "late"

private fun cues(tag: String, vararg text: String): List<MotivationalLine> =
    text.map { MotivationalLine(it, setOf(tag)) }

private fun planCues(program: String, tags: Set<String>, vararg text: String): List<MotivationalLine> =
    text.map { MotivationalLine(it, tags, setOf(program)) }

/**
 * Large, form-first coaching library. It deliberately avoids pain-glorifying
 * language ("push through it", "embrace the burn") and prioritizes control,
 * breathing, range, repeatable effort and clean technique.
 */
object MotivationLibrary {
    val lines: List<MotivationalLine> = buildList {
        addAll(cues(GENERAL,
            "Good work. Stay deliberate and keep the next rep clean.",
            "Settle into a rhythm you can repeat.",
            "Smooth work. Keep your breathing steady.",
            "Quality first. Make this rep look like the last one.",
            "Stay present. One controlled rep at a time.",
            "Strong session so far. Keep the technique consistent.",
            "You are building this set rep by rep. Stay composed.",
            "Keep a little control in reserve and finish well.",
            "Nice pace. No need to rush the movement.",
            "Own the range you can control today.",
            "Keep the effort honest and the form tidy.",
            "Breathe out through the hard part and reset.",
            "Stay tall, stay controlled, keep moving.",
            "Good. Repeat that same quality again.",
            "Consistency wins here. Keep the tempo even.",
            "Make the easy seconds look as good as the hard ones.",
            "You have time. Set up well and move with purpose.",
            "Stay patient with the set. Clean work adds up.",
            "Keep your attention on the movement, not the clock.",
            "Strong and controlled. That is the target.",
            "Keep your jaw and shoulders relaxed while you work.",
            "Use the breath to keep the effort organized.",
            "Good position. Keep it as fatigue builds.",
            "Finish the set with the same control you started with."
        ))

        addAll(cues(WARMUP,
            "Warm-up pace. Explore the range, don't force it.",
            "Use this round to loosen up and find your rhythm.",
            "Easy movement first. Let the body wake up gradually.",
            "Keep this light and smooth. Save the effort for the work sets.",
            "Move through a comfortable range and breathe normally.",
            "This is preparation, not a test. Stay relaxed.",
            "Build temperature and control before adding effort.",
            "Use the warm-up to notice how each side feels today.",
            "Keep the tempo easy and the movement precise.",
            "Good. Let each warm-up rep feel a little more natural.",
            "Stay loose through the shoulders and hips.",
            "Find your positions now so the work sets feel automatic."
        ))

        addAll(cues(STRENGTH,
            "Brace before you move, then keep the rep smooth.",
            "Control the lowering phase. Do not give the weight away.",
            "Drive with intent, return with control.",
            "Keep two clean reps in reserve if the form starts to change.",
            "Stable setup first, strong movement second.",
            "Use a load you can control through the full planned range.",
            "Keep the tempo repeatable. Strength does not need to look rushed.",
            "Reset your position before the next rep.",
            "Keep the working muscles loaded without losing alignment.",
            "Strong rep. Rebuild the same setup and go again.",
            "Let the target muscles do the work; avoid momentum.",
            "Keep the last third of the set technically clean.",
            "Stay stacked and balanced as the effort rises.",
            "Make each rep deliberate enough that you could stop anywhere.",
            "Good control. Keep the eccentric phase honest.",
            "Exhale through the effort, inhale as you reset.",
            "Keep your grip firm without tensing everything else.",
            "The goal is repeatable strength, not rushed reps."
        ))

        addAll(cues("legs",
            "Keep the whole foot connected to the floor.",
            "Track the knee in line with the foot and stay controlled.",
            "Use the hips and legs together; do not collapse into the knee.",
            "Keep your balance before adding speed or depth.",
            "Drive through a stable foot and finish tall.",
            "Control the descent and own the bottom position you choose.",
            "Keep left and right effort as even as you can.",
            "Stay smooth through the knee and hip. No bouncing.",
            "Use a comfortable depth and keep the torso organized.",
            "Good leg work. Keep the next rep quiet and controlled.",
            "Let the glutes and quads share the load.",
            "Keep the knee path steady from start to finish.",
            "Balance first, then force.",
            "Finish each rep fully before starting the next one."
        ))

        addAll(cues("core",
            "Brace as if someone is about to tap your stomach.",
            "Keep the ribs and pelvis controlled while you move.",
            "Slow the movement down if your trunk starts to rotate.",
            "Breathe behind the brace; do not hold unnecessary tension.",
            "Keep your trunk quiet and let the limbs move around it.",
            "Stay long through the spine and steady through the middle.",
            "Control matters more than range on this core set.",
            "Keep the hips level and the movement deliberate.",
            "Good brace. Maintain it without clenching your breath.",
            "Make the center stable before the arms or legs move.",
            "Keep the low back in the position you can control.",
            "Small, clean movement beats a bigger uncontrolled one."
        ))

        addAll(cues("abs",
            "Keep the abdominal work controlled rather than swinging.",
            "Exhale as you shorten the trunk and reset slowly.",
            "Keep tension through the middle without pulling on the neck.",
            "Move from the trunk, not from momentum.",
            "Keep the range clean as the set gets harder.",
            "Stay controlled through every return."
        ))

        addAll(cues("upper_body",
            "Keep the shoulders set and let the arms move from a stable base.",
            "Keep your neck relaxed while the upper body works.",
            "Control the weight all the way back to the start.",
            "Keep the ribcage stacked instead of leaning for extra range.",
            "Strong upper-body work. Keep the shoulder position clean.",
            "Use the full range you can control without shrugging.",
            "Keep the wrists and elbows organized through the rep.",
            "Let the target muscles work; keep the rest of the body quiet.",
            "Good. Keep the next rep just as smooth.",
            "Stay balanced left to right through the whole set."
        ))

        addAll(cues("push",
            "Press from a stable shoulder and finish without overreaching.",
            "Keep the elbows tracking consistently rep to rep.",
            "Stay braced while you press; do not borrow movement from the low back.",
            "Control the return and keep tension through the whole rep.",
            "Press smoothly and keep the shoulders away from the ears.",
            "Keep the chest and shoulders working without losing trunk position."
        ))

        addAll(cues("pull",
            "Start the pull from a stable shoulder blade, not a shrug.",
            "Pull the elbow through, then control the return.",
            "Keep the torso quiet while the back does the work.",
            "Finish the pull without cranking the shoulder forward.",
            "Keep both sides even and avoid twisting for extra range.",
            "Good pull. Pause briefly, then return under control."
        ))

        addAll(cues("posterior_chain",
            "Hinge from the hips and keep the spine long.",
            "Keep the load close and feel the hips travel back.",
            "Stand tall by driving the hips through, not by leaning back.",
            "Keep tension through the hamstrings and glutes as you lower.",
            "Use a controlled hinge and stop before the back position changes.",
            "Keep the shins quiet and let the hips do the traveling.",
            "Good hinge. Keep the next rep just as compact.",
            "Squeeze the glutes at the top without overextending."
        ))

        addAll(cues("cardio",
            "Keep the pace sustainable enough to stay coordinated.",
            "Quick feet, relaxed upper body.",
            "Keep breathing rhythmically as the heart rate rises.",
            "Stay light on the feet and keep the movement tidy.",
            "Energy up, technique intact.",
            "Use a pace you can control rather than chasing speed.",
            "Stay springy and relaxed through the shoulders.",
            "Keep the cadence even and the landing quiet."
        ))

        addAll(cues(STRETCH,
            "Ease into the stretch and let the range come to you.",
            "Breathe slowly and keep the stretch comfortable.",
            "Hold steady. No bouncing and no forcing the end range.",
            "Relax the surrounding muscles and keep breathing.",
            "A mild stretch is enough. More is not automatically better.",
            "Keep the position calm and controlled.",
            "Let the exhale soften the tension a little.",
            "Stay patient. Give the position time to settle.",
            "Keep both sides honest; do not chase symmetry by forcing range.",
            "Use this hold to bring the breathing back down.",
            "Easy pressure, steady breath, relaxed shoulders.",
            "Move out of the stretch as smoothly as you moved into it.",
            "Keep the joint comfortable while the muscle lengthens.",
            "This is recovery work. Stay gentle and precise.",
            "Notice the difference between useful tension and joint discomfort.",
            "Finish the hold with the same calm position."
        ))

        addAll(cues(REST,
            "Let your breathing settle before the next round.",
            "Relax your grip and shoulders. Keep moving lightly if that feels good.",
            "Use the rest. The next round should start composed.",
            "Shake out the working muscles and reset your posture.",
            "Take a sip of water if you need it, then get your setup ready.",
            "Bring the heart rate down and prepare for another clean round.",
            "Recovery is part of the session. Use the full minute.",
            "Check your breathing, then think about the first rep of the next round.",
            "Let fatigue come down before you ask for more work.",
            "Good round. Reset, recover, repeat.",
            "Stay loose during the break; no need to rush back in.",
            "You have time. Recover well, then restart with intent."
        ))

        addAll(cues(LATE,
            "Late in the session now. Protect the quality of the reps.",
            "Fatigue is up; make the setup more deliberate, not less.",
            "Finish professionally: controlled reps, steady breathing.",
            "Keep the final movements clean. There is nothing to prove with sloppy reps.",
            "Stay patient through the last part of the session.",
            "You are close. Keep the technique you started with.",
            "Last part of the work. Stay organized and finish well.",
            "Use the remaining energy on quality, not speed."
        ))

        // Program 1 — longer, general full-body strength session.
        addAll(planCues("program-1", setOf(WARMUP, GENERAL),
            "Full-body day. Build an easy rhythm now; the work comes later.",
            "Use the warm-up to prepare every major movement pattern."
        ))
        addAll(planCues("program-1", setOf(STRENGTH, GENERAL),
            "Full-body session: keep enough in reserve to stay strong across the whole workout.",
            "Think across the whole session, not just this set. Sustainable quality wins.",
            "You are training the whole body today. Keep transitions calm and technique consistent.",
            "Longer session: do not spend all your effort in one movement.",
            "Keep the work balanced. Push, pull, legs and core all need clean reps.",
            "Build volume without letting the movement quality drift."
        ))
        addAll(planCues("program-1", setOf(STRETCH),
            "Full-body work is done. Use the cooldown to bring everything back down gradually.",
            "Good full-body session. Let the final stretches be unhurried."
        ))

        // Program 2 — short weighted session; make each block count without rushing.
        addAll(planCues("program-2", setOf(WARMUP, GENERAL),
            "Short weighted session. Warm up efficiently, but do not skip good positions.",
            "You have a compact session today. Find your movement quality early."
        ))
        addAll(planCues("program-2", setOf(STRENGTH, GENERAL),
            "Short session, deliberate sets. Make the working time count.",
            "The session is brief; that is not a reason to rush the reps.",
            "Stay efficient between movements and precise during them.",
            "Compact workout: choose a load you can control immediately.",
            "Keep the pace moving, but never trade setup for speed.",
            "Use the short format well: focused work, clean transitions."
        ))
        addAll(planCues("program-2", setOf(STRETCH),
            "Work block complete. Give the cooldown the same attention as the lifting.",
            "Short session done well. Slow the breathing and finish the mobility work."
        ))

        // Program 3 — knee-friendly weighted full body. Conservative, form-first language.
        addAll(planCues("program-3", setOf(WARMUP, GENERAL),
            "Knee-friendly full body today. Use the warm-up to find a comfortable range.",
            "Check how the knees feel as you warm up. Smooth and pain-free is the target.",
            "No need to chase depth today. Prepare the hips, ankles and trunk first."
        ))
        addAll(planCues("program-3", setOf(STRENGTH, "legs", GENERAL),
            "Keep the knee movement smooth. A comfortable range is enough.",
            "Control the lowering phase and keep the knee tracking with the foot.",
            "For the knee-friendly plan, clean alignment matters more than depth.",
            "Use the hips and foot pressure to share the load with the knee.",
            "If knee discomfort sharpens, shorten the range or stop that movement.",
            "Stay controlled through the knee. Do not bounce into the bottom position.",
            "Keep the working range comfortable and repeatable on both sides.",
            "Knee capacity builds from controlled work, not forced range.",
            "Keep the foot stable and the knee path quiet.",
            "Smooth reps today. Let tolerance build gradually."
        ))
        addAll(planCues("program-3", setOf(STRENGTH, "posterior_chain", GENERAL),
            "Posterior-chain work supports the lower body without asking for deep knee flexion.",
            "Use the hip hinge well here; keep the knee position quiet and controlled.",
            "Strong hips and controlled trunk position are the focus on this set."
        ))
        addAll(planCues("program-3", setOf(STRETCH),
            "Finish the knee-friendly session gently. Stretch the muscle, not the joint.",
            "Keep the cooldown comfortable around the knee and let the range stay easy.",
            "Use the final mobility work to relax, not to force extra range."
        ))
    }

    /**
     * Prefer a program-specific cue about 45% of the time when one matches,
     * otherwise use a phase/exercise-specific generic cue. [excludeText]
     * prevents the immediately previous cue from repeating.
     */
    fun pick(tags: Set<String>, programId: String, excludeText: String? = null): MotivationalLine {
        fun fresh(pool: List<MotivationalLine>) = pool.filterNot { it.text == excludeText }.ifEmpty { pool }

        val eligible = lines.filter { it.programs.isEmpty() || programId in it.programs }
        val planPool = eligible.filter { line ->
            programId in line.programs && line.tags.any { it in tags }
        }
        val genericTagged = eligible.filter { line ->
            line.programs.isEmpty() && line.tags.any { it in tags }
        }
        val generalPool = eligible.filter { it.programs.isEmpty() && GENERAL in it.tags }

        val usePlan = planPool.isNotEmpty() && kotlin.random.Random.nextFloat() < 0.45f
        val pool = when {
            usePlan -> fresh(planPool)
            genericTagged.isNotEmpty() -> fresh(genericTagged)
            else -> fresh(generalPool)
        }
        return pool.random()
    }
}

object WorkoutIntroCues {
    private val GENERIC = listOf(
        "Session ready. Start easy, then build into the work.",
        "Your workout is ready. Settle in and make the movement quality the priority.",
        "Let's train. Stay controlled, breathe well, and keep the effort repeatable."
    )
    private val BY_PROGRAM = mapOf(
        "program-1" to listOf(
            "Full-body session today. Pace the whole workout, not just the first round.",
            "Full-body work. Build consistency across every movement pattern."
        ),
        "program-2" to listOf(
            "Short weighted session. Stay efficient between sets and deliberate during them.",
            "Compact strength session. Quality reps, clean transitions."
        ),
        "program-3" to listOf(
            "Knee-friendly full body today. Use comfortable ranges and smooth, controlled reps.",
            "Knee-support session. Good alignment and pain-free control come first."
        )
    )

    fun pick(programId: String): String =
        if (kotlin.random.Random.nextFloat() < 0.75f) BY_PROGRAM[programId].orEmpty().randomOrNull() ?: GENERIC.random()
        else GENERIC.random()
}

object RestCues {
    private val START = listOf(
        "Rest starts now. Let your breathing settle.",
        "Good round. Take the full recovery.",
        "Recover now. Relax the grip and shoulders.",
        "Use this minute well. Breathe and reset.",
        "Round complete. Shake it out and recover.",
        "Take your rest. The next round starts with a clean setup.",
        "Recovery time. Walk lightly or stay still—whatever feels better.",
        "Rest. Bring the heart rate down and reset your posture.",
        "Good work. Sip water if you need it and prepare for the next round.",
        "Take the minute. There is no benefit in rushing the recovery."
    )
    private val HALFWAY = listOf(
        "Half the rest is done. Keep the breathing easy.",
        "Thirty seconds. Start thinking about your next setup.",
        "Halfway through recovery. Stay loose.",
        "Thirty seconds left. Let the working muscles settle.",
        "Half the break remains. You should feel more composed now."
    )
    private val ALMOST_DONE = listOf(
        "Five seconds. Get into position for the next movement.",
        "Back to work in five. Build your setup now.",
        "Five seconds. One breath, then restart clean.",
        "Recovery is nearly done. Set your feet and focus.",
        "Five seconds left. Ready for a controlled first rep."
    )
    fun start(): String = START.random()
    fun halfway(): String = HALFWAY.random()
    fun almostDone(): String = ALMOST_DONE.random()
}

object StretchCues {
    private val START = listOf(
        "Ease into the stretch. Keep it comfortable.",
        "Settle into the position and slow the breathing.",
        "Mobility work now. No bouncing and no forcing.",
        "Find mild tension, then hold it calmly.",
        "Take your time getting into this stretch.",
        "Let the range come gradually."
    )
    private val HALFWAY = listOf(
        "Halfway. Keep the breath slow and the position relaxed.",
        "Half the hold is done. Stay gentle.",
        "Keep the same comfortable tension. Halfway there.",
        "Stay patient through the second half of the hold.",
        "Good. Maintain the position without forcing more range."
    )
    private val ALMOST_DONE = listOf(
        "Five seconds. Ease out smoothly when the timer ends.",
        "Five more seconds. Keep breathing.",
        "Almost done. Do not bounce out of the position.",
        "Finish the hold calmly, then release slowly.",
        "Five seconds left. Keep the joint relaxed."
    )
    fun start(): String = START.random()
    fun halfway(): String = HALFWAY.random()
    fun almostDone(): String = ALMOST_DONE.random()
}

object FinisherCues {
    private val GENERIC = listOf(
        "Session complete. Strong, controlled work today.",
        "Workout complete. Good job keeping the session moving.",
        "That's the session. Recover well and take the win.",
        "Done for today. Consistent work adds up.",
        "Session finished. Nice work staying with it.",
        "Workout complete. Good effort and good follow-through.",
        "That's a wrap. Let the recovery start now.",
        "Day complete. You showed up and did the work.",
        "All done. Strong session from start to finish.",
        "Finished. Take a moment to notice what felt better today."
    )
    private val PROGRAM = mapOf(
        "program-1" to listOf(
            "Full-body session complete. Good job managing the work across the whole body.",
            "Full-body day done. Recover well—you covered a lot of movement today."
        ),
        "program-2" to listOf(
            "Short weighted session complete. Focused work, done.",
            "Compact session finished. Efficient and complete."
        ),
        "program-3" to listOf(
            "Knee-friendly full-body session complete. Controlled work is the win today.",
            "Knee-support session done. Let the joints recover and note how the range felt."
        )
    )
    fun pick(programId: String): String =
        if (kotlin.random.Random.nextFloat() < 0.5f) PROGRAM[programId].orEmpty().randomOrNull() ?: GENERIC.random()
        else GENERIC.random()
}

object RepCues {
    private val GET_READY = listOf(
        "Set your position", "Get ready", "Build your setup", "Find your stance", "Brace and get set", "Ready up"
    )
    private val GO = listOf(
        "Start", "Go", "Begin the set", "Smooth reps", "Let's work", "First rep"
    )
    fun getReady(): String = GET_READY.random()
    fun go(): String = GO.random()
}

fun isStretchSection(sectionTitle: String): Boolean {
    val t = sectionTitle.lowercase()
    return "stretch" in t || "cool down" in t || "cooldown" in t
}

/** Cheap classifier used by both the visible coach card and voice cues. */
fun motivationTagsFor(exerciseName: String, sectionTitle: String, ordinal: Int = 0, total: Int = 0): Set<String> {
    val text = "$exerciseName $sectionTitle".lowercase()
    val tags = mutableSetOf<String>()

    if (isStretchSection(sectionTitle)) return setOf(STRETCH)
    if ("warm" in sectionTitle.lowercase()) return setOf(WARMUP)
    if ("rep" in sectionTitle.lowercase()) tags += STRENGTH

    if (listOf("squat", "lunge", "leg", "calf", "glute", "step-up", "step up", "wall sit", "clamshell", "donkey kick").any { it in text }) tags += "legs"
    if (listOf("sit-up", "situp", "crunch", "v-up", "leg raise", "toe touch", "flutter kick", "scissor kick").any { it in text }) tags += "abs"
    if (listOf("plank", "dead bug", "bird dog", "pallof", "hollow", "woodchopper", "russian twist", "anti-rotation").any { it in text }) tags += "core"
    if (listOf("push-up", "pushup", "bench press", "shoulder press", "overhead press", "dip").any { it in text }) tags += "push"
    if (listOf("row", "pull-up", "pullup", "pulldown").any { it in text }) tags += "pull"
    if (listOf("push-up", "pushup", "press", "curl", "tricep", "bicep", "dip", "row", "pull-up", "pullup", "shoulder", "chest", "lat pulldown").any { it in text }) tags += "upper_body"
    if (listOf("deadlift", "romanian", "hip thrust", "glute bridge", "hamstring", "hinge").any { it in text }) tags += "posterior_chain"
    if (listOf("burpee", "jump", "jack", "mountain climber", "sprint", "quick feet", "high knee").any { it in text }) tags += "cardio"
    if (total > 0 && ordinal.toFloat() / total >= 0.72f) tags += LATE
    if (tags.isEmpty()) tags += GENERAL
    return tags
}
