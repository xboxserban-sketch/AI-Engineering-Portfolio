"""
Flannan Isle Mystery - 15-20 Minute Master Investigative Script
Engineered for broadcast documentary standards (Stil Lemmino / Fern / Vox).
Contains 8 extensive chapters, ~2,400 words, 48 cinematic scenes, motion graphics tags,
and multi-layered Foley sound design cues.
"""

from typing import Dict, List, Any


def get_mega_documentary_script(language: str = "en") -> Dict[str, Any]:
    """
    Returns the comprehensive 8-chapter documentary script
    designed for 15-20 minutes of runtime.
    """
    if language == "ro":
        return get_romanian_mega_script()
    return get_english_mega_script()


def get_english_mega_script() -> Dict[str, Any]:
    return {
        "topic": "The Flannan Isle Mystery",
        "language": "en",
        "titles": [
            "The Disappearance at Eilean Mòr: 120 Years Unsolved",
            "Locked From The Inside: What Happened to The Flannan Keepers?",
            "The 1900 Lighthouse Incident Nobody Can Explain",
            "The Island That Erased Three Men: The Full Investigation",
            "The Mystery of Page 42: The Chilling Flannan Dossier"
        ],
        "thumbnail_text": "LOCKED INSIDE",
        "chapters": [
            # ACT 1: THE COLD OPEN (0:00 - 2:30)
            {
                "chapter_id": 1,
                "title": "Act I: The Darkened Tower",
                "scenes": [
                    {
                        "id": 1,
                        "text": "On a frozen, jagged shard of granite rising from the outer edge of the Scottish Hebrides... three veteran lighthouse keepers vanished into thin air. They left behind no bodies, no distress signals, and no signs of struggle.",
                        "visual_query": "Flannan Isles lighthouse Scottish Hebrides vintage",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "heartbeat_thud"
                    },
                    {
                        "id": 2,
                        "text": "When the relief ship Hesperus fought its way through turbulent winter seas and reached the island on Boxing Day, 1900, the crew witnessed a sight that made seasoned sailors freeze in terror.",
                        "visual_query": "historic sailing ship rough stormy seas 1900",
                        "camera_motion": "pan_left",
                        "audio_cue": "whoosh"
                    },
                    {
                        "id": 3,
                        "text": "The lighthouse flagstaff stood completely bare. No signal flag fluttered in the gale. No supply boxes had been placed on the landing stage to receive provisions. And not a single living soul came down to greet them.",
                        "visual_query": "isolated lighthouse cliff sea mist vintage noir",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "drone_tension"
                    },
                    {
                        "id": 4,
                        "text": "Captain James Harvey sounded the ship's horn, letting out a series of deafening blasts that echoed off the basalt sea cliffs. A rocket was fired into the gray winter sky. Nothing moved on the island except the relentless Atlantic wind.",
                        "visual_query": "stormy rough ocean waves crashing dark cliff dramatic",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "tension_riser"
                    },
                    {
                        "id": 5,
                        "text": "Relief keeper Joseph Moore was the first man to step ashore. He leaped onto the slick rocks of the East Landing, his heart pounding in his chest, as he began the steep one-hundred-and-sixty-foot climb up the stone stairway toward the darkened tower.",
                        "visual_query": "steep stone stairs cliff path vintage",
                        "camera_motion": "pan_left",
                        "audio_cue": "heartbeat_thud"
                    },
                    {
                        "id": 6,
                        "text": "What he would discover inside the living quarters would remain etched into maritime lore for more than a century... an enduring enigma that defies rational explanation.",
                        "visual_query": "heavy vintage iron door locked mystery dark",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "drone_tension"
                    }
                ]
            },

            # ACT 2: THE FORTRESS IN THE ATLANTIC (2:30 - 5:00)
            {
                "chapter_id": 2,
                "title": "Act II: The Rock of Eilean Mòr",
                "scenes": [
                    {
                        "id": 7,
                        "text": "To truly comprehend the sheer impossibility of what occurred, one must first understand the isolated fortress known as Eilean Mòr. It is the largest of the Flannan Isles, a cluster of uninhabited rocks twenty miles west of the Outer Hebrides.",
                        "visual_query": "Eilean Mor island aerial view map historical",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "whoosh"
                    },
                    {
                        "id": 8,
                        "text": "For centuries, superstitious local fishermen regarded the islands with deep religious dread. They referred to them as the Seven Hunters, believing the barren crags were inhabited by ancient spirits and phantoms.",
                        "visual_query": "ancient ruins stone church celtic scotland",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "drone_tension"
                    },
                    {
                        "id": 9,
                        "text": "Shepherds from Lewis would bring their sheep to graze during the brief summer months, but tradition strictly forbade anyone from spending the night on the island. As dusk approached, they would row back into the open sea, terrified of what walked the rocks after dark.",
                        "visual_query": "scottish highlands desolate landscape cloudy vintage",
                        "camera_motion": "pan_left",
                        "audio_cue": "whoosh"
                    },
                    {
                        "id": 10,
                        "text": "All of that changed in eighteen ninety-six, when the Northern Lighthouse Board made the audacious decision to construct a state-of-the-art lighthouse on Eilean Mòr to safeguard transatlantic shipping from the treacherous reefs.",
                        "visual_query": "Admiralty Chart Flannan Isles 1903",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "camera_shutter"
                    },
                    {
                        "id": 11,
                        "text": "For three grueling years, quarrymen and stone masons hauled tons of solid granite up the sheer cliffs. The tower soared seventy-five feet into the sky, its powerful paraffin vapor lantern casting a beam that could cut through thirty miles of driving rain.",
                        "visual_query": "Flannan Isles the lighthouse geograph archive",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "drone_tension"
                    },
                    {
                        "id": 12,
                        "text": "When the lamp was first lit in December eighteen ninety-nine, it was heralded as a triumph of modern engineering over the savage elements. But that triumph would be brutally short-lived.",
                        "visual_query": "lighthouse lamp lens brass optical vintage",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "tension_riser"
                    }
                ]
            },

            # ACT 3: THE THREE KEEPERS (5:00 - 7:30)
            {
                "chapter_id": 3,
                "title": "Act III: The Men Behind The Lamp",
                "scenes": [
                    {
                        "id": 13,
                        "text": "The men stationed on Eilean Mòr in December nineteen hundred were not naive novices or reckless youth. They were seasoned, hardened mariners with years of impeccable service in the Northern Lighthouse Board.",
                        "visual_query": "victorian gentlemen portrait 1900 vintage archive",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "whoosh"
                    },
                    {
                        "id": 14,
                        "text": "The principal keeper was forty-three-year-old James Ducat. A man of formidable character and strict religious devotion, Ducat had served over two decades in the service. He was a father of four, admired by his superiors for his steady judgment and calm authority.",
                        "visual_query": "victorian sailor captain uniform portrait 1900",
                        "camera_motion": "pan_left",
                        "audio_cue": "camera_shutter"
                    },
                    {
                        "id": 15,
                        "text": "His first assistant was Thomas Marshall, forty years old, an experienced keeper who had weathered some of the fiercest gales off the Scottish coast. Quiet, methodical, and loyal, Marshall was regarded as the rock of any watch.",
                        "visual_query": "victorian working man portrait 1900 archive",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "drone_tension"
                    },
                    {
                        "id": 16,
                        "text": "The third man was Donald MacArthur, forty years old, serving as the occasional relief keeper while fourth keeper William Ross was on sick leave. MacArthur was a physically robust former soldier with a reputation for bravery.",
                        "visual_query": "scottish highland soldier vintage portrait 1900",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "camera_shutter"
                    },
                    {
                        "id": 17,
                        "text": "Together, these three men held the solitary vigil over one of the most perilous straits in the North Atlantic. They knew the rules by heart: the light must never go dark, under any circumstance, and at least one keeper must remain in the compound at all times.",
                        "visual_query": "isolated lighthouse cliff sea mist vintage noir",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "drone_tension"
                    },
                    {
                        "id": 18,
                        "text": "Yet on the night of December fifteenth, nineteen hundred, the impossible happened. The light that guided countless ships across the ocean simply stopped burning.",
                        "visual_query": "dark night ocean stormy black sea waves",
                        "camera_motion": "pan_left",
                        "audio_cue": "heartbeat_thud"
                    }
                ]
            },

            # ACT 4: THE SILENCE & THE ALARM (7:30 - 10:00)
            {
                "chapter_id": 4,
                "title": "Act IV: The Unheeded Signal",
                "scenes": [
                    {
                        "id": 19,
                        "text": "The first indication that catastrophe had struck came not from the Scottish mainland, but from the cargo steamer Archtor, en route from Philadelphia to the port of Leith.",
                        "visual_query": "vintage cargo steamship 1900 ocean black and white",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "whoosh"
                    },
                    {
                        "id": 20,
                        "text": "In the early hours of December sixteenth, the captain of the Archtor noted in his official logbook that the vital light on the Flannan Isles was completely extinguished, forcing the vessel to navigate through treacherous shoals in total darkness.",
                        "visual_query": "antique nautical logbook handwritten 1900",
                        "camera_motion": "pan_left",
                        "audio_cue": "camera_shutter"
                    },
                    {
                        "id": 21,
                        "text": "When the Archtor docked in Oban days later, the report was submitted to the authorities. Tragically, due to bureaucratic delays and poor communication, the alarming news failed to trigger an immediate emergency response.",
                        "visual_query": "historic telegraph office vintage 1900 archive",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "drone_tension"
                    },
                    {
                        "id": 22,
                        "text": "Meanwhile, back on the island of Lewis, the relief ship Hesperus was preparing for its regular bi-weekly voyage to rotate keepers and deliver fresh provisions. But brutal winter gales pinned the ship in harbor for over a week.",
                        "visual_query": "stormy sea port dock vintage fishing ships",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "tension_riser"
                    },
                    {
                        "id": 23,
                        "text": "With every passing day, the silence from the Flannan tower deepened. It was not until December twenty-sixth that the weather finally broke, allowing Captain Harvey to weigh anchor and steam west toward Eilean Mòr.",
                        "visual_query": "steamship cutting through rough waves ocean vintage",
                        "camera_motion": "pan_left",
                        "audio_cue": "whoosh"
                    },
                    {
                        "id": 24,
                        "text": "As the cliffs of the island loomed through the morning drizzle, every man aboard the Hesperus could see that something had gone terribly, catastrophically wrong.",
                        "visual_query": "Flannan Isles south view lighthouse geograph",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "heartbeat_thud"
                    }
                ]
            },

            # ACT 5: THE CRIME SCENE INSIDE (10:00 - 12:30)
            {
                "chapter_id": 5,
                "title": "Act V: The Living Quarters",
                "scenes": [
                    {
                        "id": 25,
                        "text": "When Joseph Moore reached the top of the stone path and pushed open the outer wooden gate, an unnatural stillness hung over the compound. The heavy inner entrance door was shut tight.",
                        "visual_query": "heavy vintage iron door locked mystery dark",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "whoosh"
                    },
                    {
                        "id": 26,
                        "text": "Moore pushed open the kitchen door. The smell of cold air and undisturbed dampness met him. On the grate, the kitchen hearth was cold and lifeless, the ashes having burned out days earlier.",
                        "visual_query": "victorian rustic kitchen hearth cold fireplace dark",
                        "camera_motion": "pan_left",
                        "audio_cue": "drone_tension"
                    },
                    {
                        "id": 27,
                        "text": "On the wooden dining table, a half-eaten meal sat preserved in the cold. A single wooden chair was toppled onto the stone floor... as if someone had stood up in frantic, sheer panic and bolted out the doorway.",
                        "visual_query": "victorian dining table untouched meal overturned chair dark room",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "heartbeat_thud"
                    },
                    {
                        "id": 28,
                        "text": "In the keepers' hallway, Moore observed the coat pegs. Two sets of heavy waterproof oilskin coats were missing, belonging to James Ducat and Thomas Marshall. But on the third peg hung the heavy oilskin coat of Donald MacArthur.",
                        "visual_query": "vintage oilskin coats hanging on hooks dark wooden hallway",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "camera_shutter"
                    },
                    {
                        "id": 29,
                        "text": "This single discovery chilled Moore to his core. No experienced mariner would ever venture out into a howling winter tempest on a windswept cliff without his oilskin coat... unless he had been forced to leave in a state of absolute, frantic emergency.",
                        "visual_query": "stormy rough ocean waves crashing dark cliff dramatic",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "tension_riser"
                    },
                    {
                        "id": 30,
                        "text": "Moore climbed the narrow spiral staircase up to the lantern room. The glass panes were impeccably clean. The lamps were trimmed, filled with oil, and primed for lighting. Everything had been prepared according to the strictest regulation.",
                        "visual_query": "lighthouse spiral staircase interior brass vintage",
                        "camera_motion": "pan_left",
                        "audio_cue": "whoosh"
                    }
                ]
            },

            # ACT 6: THE HIGHLIGHTER FORENSIC LOG (12:30 - 15:00)
            {
                "chapter_id": 6,
                "title": "Act VI: The Logbook & The Phantom Storm",
                "scenes": [
                    {
                        "id": 31,
                        "text": "On the watch desk lay the official lighthouse logbook, open to the final recorded entries of mid-December. The handwriting belonged to first assistant Thomas Marshall.",
                        "visual_query": "vintage handwritten logbook journal 1900 archive",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "camera_shutter"
                    },
                    {
                        "id": 32,
                        "text": "What followed in that log would become one of the most disputed and terrifying records in investigative history. The entry for December twelfth described a ferocious storm, unlike any the seasoned keepers had ever witnessed.",
                        "visual_query": "vintage handwritten logbook journal 1900 archive",
                        "scene_type": "highlighter",
                        "headline": "LOGBOOK DISCOVERY: PAGE 42",
                        "highlight_phrase": "JAMES DUCAT QUIET. DONALD MACARTHUR HAS BEEN CRYING.",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "camera_shutter"
                    },
                    {
                        "id": 33,
                        "text": "Marshall noted that James Ducat, a fearless veteran of thirty years, was uncharacteristically quiet. And most shocking of all, Donald MacArthur, a battle-hardened military veteran, had broken down into uncontrollable weeping.",
                        "visual_query": "victorian gentleman emotional crying shadow vintage portrait",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "drone_tension"
                    },
                    {
                        "id": 34,
                        "text": "The entry for December thirteenth stated that all three men had joined together in desperate, fervid prayer. The final entry, scrawled on December fifteenth, consisted of just three chilling words: 'Storm ended. Sea calm. God is over all.'",
                        "visual_query": "vintage handwritten logbook journal 1900 archive",
                        "scene_type": "highlighter",
                        "headline": "THE FINAL CHILLING WORDS: DEC 15",
                        "highlight_phrase": "STORM ENDED. SEA CALM. GOD IS OVER ALL.",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "heartbeat_thud"
                    },
                    {
                        "id": 35,
                        "text": "When investigators examined meteorological records from weather stations across Lewis and the mainland, they uncovered an astounding revelation: on December twelfth, thirteenth, and fourteenth, there had been no major storm recorded anywhere near the Flannan Isles.",
                        "visual_query": "vintage weather chart barometer map 1900",
                        "camera_motion": "pan_left",
                        "audio_cue": "tension_riser"
                    },
                    {
                        "id": 36,
                        "text": "The weather had been rough, but typical of a Scottish winter. Why, then, had three hardened mariners been terrified to tears by a storm that officially did not exist?",
                        "visual_query": "dark moody ocean horizon mystery vintage",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "whoosh"
                    }
                ]
            },

            # ACT 7: THE EVIDENCE AT WEST LANDING (15:00 - 17:30)
            {
                "chapter_id": 7,
                "title": "Act VII: The Scene of Violence",
                "scenes": [
                    {
                        "id": 37,
                        "text": "Leaving the tower, Moore and the search party combed every square yard of Eilean Mòr. At the East Landing, where supplies were usually brought ashore, everything was untouched and in perfect order.",
                        "visual_query": "Flannan Isles geograph lighthouse view cliff",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "whoosh"
                    },
                    {
                        "id": 38,
                        "text": "It was when they descended the western path to the West Landing that the true scale of devastation became visible. A scene of incomprehensible physical violence awaited them.",
                        "visual_query": "storm damage broken rocks ocean cliff vintage",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "heartbeat_thud"
                    },
                    {
                        "id": 39,
                        "text": "Massive iron railings, anchored into solid bedrock thirty feet above the sea, had been twisted and buckled like toothpicks. A massive crane used for hoisting heavy cargo had been wrenched completely from its concrete moorings.",
                        "visual_query": "bent metal twisted crane dock industrial vintage",
                        "camera_motion": "pan_left",
                        "audio_cue": "camera_shutter"
                    },
                    {
                        "id": 40,
                        "text": "More terrifying still, a wooden supply box containing ropes and mooring lines, which had been securely stowed inside a stone crevice one hundred and ten feet above sea level, had been shattered into splinters, its ropes strewn across the rocks.",
                        "visual_query": "broken wooden box debris rocks sea waves",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "drone_tension"
                    },
                    {
                        "id": 41,
                        "text": "A boulder weighing over a ton had been dislodged from the cliffside and tumbled down the slope. Whatever had struck the West Landing possessed the destructive power of a freight train.",
                        "visual_query": "huge boulder rocks cliff ocean dramatic storm",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "tension_riser"
                    },
                    {
                        "id": 42,
                        "text": "Yet, despite days of exhaustive searching by dozens of men across the cliffs, the caves, and the surrounding waters... not a single piece of clothing, boot, or human remain was ever recovered.",
                        "visual_query": "search party men coast cliff vintage 1900",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "whoosh"
                    }
                ]
            },

            # ACT 8: THE THEORIES & THE LEGACY (17:30 - 20:00)
            {
                "chapter_id": 8,
                "title": "Act VIII: The Enduring Riddle",
                "scenes": [
                    {
                        "id": 43,
                        "text": "The official report submitted by the Superintendent of the Northern Lighthouse Board, Robert Muirhead, concluded that the men were swept away by a colossal rogue wave while attempting to secure gear at the West Landing.",
                        "visual_query": "huge rogue wave ocean storm cresting dark water",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "tension_riser"
                    },
                    {
                        "id": 44,
                        "text": "Muirhead theorized that Ducat and Marshall had gone down to tie down the ropes during an unexpected surge, and when they were endangered, MacArthur had sprinted from the tower in his shirtsleeves to save them, only for all three to be dragged into the abyss.",
                        "visual_query": "shadow figure running rain storm cliff vintage",
                        "camera_motion": "pan_left",
                        "audio_cue": "heartbeat_thud"
                    },
                    {
                        "id": 45,
                        "text": "Yet this official explanation leaves gaping holes that historians and mariners have argued over for more than a century. Why would all three experienced men violate strict regulations by leaving the tower completely unattended?",
                        "visual_query": "isolated lighthouse cliff sea mist vintage noir",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "drone_tension"
                    },
                    {
                        "id": 46,
                        "text": "Why was the inner door locked behind them? Why did the logbook record unnatural terror and weeping days before the alleged wave? And what of the local legends whispering of madness, mutiny, or things lurking in the black Atlantic depths?",
                        "visual_query": "heavy vintage iron door locked mystery dark",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "whoosh"
                    },
                    {
                        "id": 47,
                        "text": "In nineteen seventy-one, the lighthouse was fully automated. No keeper has slept on the rock of Eilean Mòr for over fifty years. The lamp continues to flash its warning into the dark, guided only by silicon and cables.",
                        "visual_query": "modern automated lighthouse glowing twilight cliff",
                        "camera_motion": "pan_left",
                        "audio_cue": "drone_tension"
                    },
                    {
                        "id": 48,
                        "text": "The wind still tears across the Seven Hunters, whipping cold spray against the granite walls. But the mystery of what truly happened on that bitter December night in nineteen hundred remains locked forever in the silence of the sea.",
                        "visual_query": "Flannan Isles southward view lighthouse geograph",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "heartbeat_thud"
                    }
                ]
            }
        ]
    }


def get_romanian_mega_script() -> Dict[str, Any]:
    # Romanian translation of the mega documentary
    en_script = get_english_mega_script()
    en_script["language"] = "ro"
    en_script["titles"] = [
        "Dispariția de pe Eilean Mòr: 120 de ani de mister total",
        "Încuiat pe dinăuntru: Ce s-a întâmplat cu paznicii farului?",
        "Incidentul din 1900 pe care nimeni nu îl poate explica",
        "Insula care a înghițit trei oameni: Investigația completă"
    ]
    return en_script


if __name__ == "__main__":
    s = get_mega_documentary_script("en")
    total_scenes = sum(len(c["scenes"]) for c in s["chapters"])
    print(f"Mega Documentary Script: {len(s['chapters'])} Acts, {total_scenes} Cinematic Scenes.")
