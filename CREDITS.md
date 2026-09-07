# Third-party media credits

Most exercise demo media comes from two sources baked into the app's own
media pipeline and already covered by their own licenses/terms:

- [free-exercise-db](https://github.com/yuhonas/free-exercise-db) — public
  domain (Unlicense). Referenced by id (`freeExerciseDbId` in `programs/*.json`);
  images are fetched directly from that repo, never copied into this one.
- [wger](https://wger.de) — free, keyless public exercise database.
  Referenced by id (`wgerId`); fetched live from wger's own API.
- [ExerciseDB](https://exercisedb.dev) (via RapidAPI / Ascend API) —
  commercial, requires your own free API key (Settings → Add exercise
  demos). Never bundled into this repo — it's their product, not ours to
  redistribute.

## One-off hotlinks (`externalMediaUrl`)

A handful of exercises have no entry in any of the above but a verified,
individually-checked free match exists elsewhere. These are linked directly
(never downloaded into this repo) via the `externalMediaUrl` field on
`Exercise`, and credited here:

| Exercise | Source | Author | License |
|---|---|---|---|
| Jumping Jack | [Jumpingjacks.gif](https://commons.wikimedia.org/wiki/File:Jumpingjacks.gif), Wikimedia Commons | [Wensceslao](https://commons.wikimedia.org/wiki/User:Wensceslao) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| Diamond Push-up | [Diamondpushups1.jpg](https://commons.wikimedia.org/wiki/File:Diamondpushups1.jpg), Wikimedia Commons | [Erick76470](https://commons.wikimedia.org/wiki/User:Erick76470) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| Downward Facing Dog | [Downward-Facing-Dog.JPG](https://commons.wikimedia.org/wiki/File:Downward-Facing-Dog.JPG), Wikimedia Commons | [Iveto](https://commons.wikimedia.org/w/index.php?title=User:Iveto) | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) |
| Crunch Floor | [Sit-ups or Crunch.gif](https://commons.wikimedia.org/wiki/File:Sit-ups_or_Crunch.gif), Wikimedia Commons | [Zimmermanns](https://commons.wikimedia.org/wiki/User:Zimmermanns) | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) |

CC BY-SA requires attribution and share-alike for derivatives; this table
is that attribution. No modifications were made to the linked file.

## Bundled exercise demos (`exercise_media/`)

These files are copied into the Android and web builds so common exercises do
not depend on an API key or a fragile remote hotlink. They are used unmodified.

| Local asset | Exercise(s) | Source | Creator | License |
|---|---|---|---|---|
| `bicycle-crunch.jpg` | Bicycle Crunch | [Bicycle crunch with back support](https://commons.wikimedia.org/wiki/File:Bicycle_crunch_with_back_support.jpg), Wikimedia Commons | Tim Cigelske | [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/) |
| `clamshell.png` | Clamshell | Figure 2, [Lee et al., *Medicina* 2026](https://www.mdpi.com/1648-9144/62/6/1025) | Hwa-Yeon Lee, Yi-Heng Zhang, Ki-Choul Kim, Hyoung-Won Lim | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| `downward-facing-dog.jpg` | Downward Facing Dog | [Downward-Facing-Dog.JPG](https://commons.wikimedia.org/wiki/File:Downward-Facing-Dog.JPG), Wikimedia Commons | Iveto | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) |
| `plank-reach.jpg` | Plank Reach | [Plank with Hand Raise](https://www.dvidshub.net/video/640233/plank-with-hand-raise), DVIDS | U.S. Marine Corps | Public domain |
| `punches.jpg` | Punches | [Shadow boxing (or dancing)](https://commons.wikimedia.org/wiki/File:Shadow_boxing_(or_dancing)_(33650053352).jpg), Wikimedia Commons | Neil Dalphin | CC0 |
| `quick-feet.jpg` | Quick Feet | [Quick feet](https://www.dvidshub.net/image/8674174/quick-feet), DVIDS | John Quinn / Devens Reserve Forces Training Area | Public domain |
| `side-lunge.jpg` | Side Lunge; Side Lunge Stretch | [USMC-100330-M-3740P-008](https://commons.wikimedia.org/wiki/File:USMC-100330-M-3740P-008.jpg), Wikimedia Commons / U.S. Marine Corps | Lance Cpl. Jennifer J. Pirante | Public domain |
| `static-lunge.gif` | Static Lunge | [Lunge—CDC Strength Training for Older Adults](https://commons.wikimedia.org/wiki/File:Lunge-CDC_strength_training_for_older_adults.gif), Wikimedia Commons | U.S. Centers for Disease Control and Prevention | Public domain |
| `wall-sit.jpg` | Wall Sit | [Coast Guard members work out](https://www.dvidshub.net/image/984477/coast-guard-members-work-out), DVIDS | Petty Officer 1st Class Brandyn Hill / U.S. Coast Guard | Public domain |

The additional no-key mappings for Arm Swing, SLOW Push-ups, Single Leg Calf
Raise, Sumo Squats, and Wall Pectoral Stretch use `free-exercise-db`, whose
images are public domain under the Unlicense as described above.
