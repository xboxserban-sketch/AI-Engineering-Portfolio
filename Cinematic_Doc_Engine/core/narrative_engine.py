"""
Narrative & Retention Engine: Crafts documentary scripts engineered for maximum psychological retention
(Hook in first 3 seconds, Zeigarnik effect / open loops, emotional pacing) and generates high-CTR titles & thumbnail blueprints.
"""

import json
import os
import re
from typing import Dict, List, Any


class DocumentaryScript:
    def __init__(
        self,
        topic: str,
        language: str = "en",
        titles: List[str] = None,
        thumbnail_concepts: List[Dict[str, str]] = None,
        scenes: List[Dict[str, Any]] = None
    ):
        self.topic = topic
        self.language = language
        self.titles = titles or []
        self.thumbnail_concepts = thumbnail_concepts or []
        self.scenes = scenes or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "language": self.language,
            "titles": self.titles,
            "thumbnail_concepts": self.thumbnail_concepts,
            "scenes": self.scenes
        }

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


def get_curated_template(topic: str, language: str = "en") -> DocumentaryScript:
    """
    Returns an engineered psychological documentary script for flagship topics or custom topics.
    Designed with Lemmino-level pacing:
    - 0-5s: The Hook & Paradox (Cold Open)
    - 6-25s: The Inciting Reality & Atmospheric Setting
    - 26-55s: The Discovery / The Unsettling Clues
    - 56-85s: The Psychological Analysis & The Unsolved Loop
    """
    topic_lower = topic.lower()

    if "flannan" in topic_lower or "far" in topic_lower or "lighthouse" in topic_lower:
        if language == "ro":
            return DocumentaryScript(
                topic="Misterul Farului de pe Insula Flannan",
                language="ro",
                titles=[
                    "Ce s-a întâmplat în camera secretă a farului în 1900?",
                    "Cei 3 oameni care s-au evaporat dintr-o cameră încuiată pe dinăuntru",
                    "Incidentul Flannan: Însemnarea de la pagina 42 pe care nimeni nu o poate explica",
                    "Insula de pe care nu a mai plecat nimeni viu",
                    "Misterul de 120 de ani pe care autoritățile l-au clasat în tăcere"
                ],
                thumbnail_concepts=[
                    {
                        "layout": "Față în umbră + Far solitar pe stâncă luminat dramatic",
                        "text_overlay": "ÎNCUIAȚI PE DINĂUNTRU",
                        "color_palette": "Albastru rece marin, lumină aurie puternică de felinar",
                        "image_prompt": "Dark stormy sea cliff at night, isolated 1900 Victorian stone lighthouse glowing, dramatic lightning in distant clouds, cinematic mystery documentary style, 8k"
                    },
                    {
                        "layout": "Jurnal vechi deschis cu pete de cerneală și ceas oprit la ora 1:55",
                        "text_overlay": "UNDE SUNT?",
                        "color_palette": "Sepia întunecat, umbre accentuate noir",
                        "image_prompt": "Close up of an old weathered Victorian logbook page with vintage handwritten notes, antique brass clock stopped at 1:55, cinematic low-key lighting"
                    }
                ],
                scenes=[
                    {
                        "id": 1,
                        "text": "Pe o insulă stâncoasă și pustie din Atlanticul de Nord... trei bărbați au încetat pur și simplu să existe.",
                        "visual_query": "Flannan Isle lighthouse archive 1900 black and white",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "heartbeat_thud",
                        "estimated_duration": 6.5
                    },
                    {
                        "id": 2,
                        "text": "Când nava de salvare a ajuns la țărm, ușa masivă de fier era încuiată. Pe dinăuntru.",
                        "visual_query": "heavy vintage iron door locked mystery dark",
                        "camera_motion": "pan_left",
                        "audio_cue": "drone_tension",
                        "estimated_duration": 6.0
                    },
                    {
                        "id": 3,
                        "text": "Pe masă, mâncarea era neatinsă. Un singur scaun era răsturnat pe podea... ca și cum cineva s-ar fi ridicat în grabă extremă.",
                        "visual_query": "victorian dining table untouched meal overturned chair dark room",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "tension_riser",
                        "estimated_duration": 7.5
                    },
                    {
                        "id": 4,
                        "text": "Dar cel mai înfiorător detaliu a fost descoperit în jurnalul oficial de bord. Ultima însemnare menționa o furtună monstruoasă.",
                        "visual_query": "vintage handwritten logbook journal 1900 archive",
                        "scene_type": "highlighter",
                        "headline": "DESCOPERIREA DIN JURNAL: PAGINA 42",
                        "highlight_phrase": "O FURTUNĂ MONSTRUOASĂ CARE NU A EXISTAT NICIODATĂ",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "camera_shutter",
                        "estimated_duration": 7.0
                    },
                    {
                        "id": 5,
                        "text": "O furtună care, conform tuturor rapoartelor meteorologice din zonă... nu a existat niciodată.",
                        "visual_query": "stormy rough ocean waves crashing dark cliff dramatic",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "heartbeat_thud",
                        "estimated_duration": 6.5
                    },
                    {
                        "id": 6,
                        "text": "Au trecut peste o sută douăzeci de ani. Niciun cadavru nu a fost găsit. Iar întrebarea rămâne: de ce anume au fugit cei trei paznici în noapte?",
                        "visual_query": "isolated lighthouse cliff sea mist vintage noir",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "drone_tension",
                        "estimated_duration": 8.5
                    }
                ]
            )
        else:
            return DocumentaryScript(
                topic="The Flannan Isle Mystery",
                language="en",
                titles=[
                    "The Men Who Vanished From an Island",
                    "Locked From The Inside: The 1900 Flannan Isle Incident",
                    "The Chilling Final Log Entry on Page 42",
                    "Why 3 Lighthouse Keepers Ceased to Exist",
                    "The Century-Old Mystery That Defies All Logic"
                ],
                thumbnail_concepts=[
                    {
                        "layout": "Silhouette on cliff + ominous glowing lantern beam through dense mist",
                        "text_overlay": "LOCKED INSIDE",
                        "color_palette": "Deep oceanic navy blue, sharp lantern amber",
                        "image_prompt": "Victorian lighthouse isolated on rugged Scottish cliff at twilight, turbulent sea mist, single ominous warm light beam cutting through gloom, cinematic master shot"
                    },
                    {
                        "layout": "Weathered archive logbook with clock frozen at 1:55",
                        "text_overlay": "NEVER FOUND",
                        "color_palette": "Dark vintage sepia, harsh directional shadows",
                        "image_prompt": "Antique logbook with faded cursive entries and a maritime brass compass, dimly lit by candlelight, high mystery atmosphere"
                    }
                ],
                scenes=[
                    {
                        "id": 1,
                        "text": "On a frozen, desolate rock in the North Atlantic... three men simply ceased to exist.",
                        "visual_query": "Flannan Isle lighthouse archive 1900 black and white",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "heartbeat_thud",
                        "estimated_duration": 6.0
                    },
                    {
                        "id": 2,
                        "text": "When the relief vessel finally reached the island, the heavy outer steel door was locked. From the inside.",
                        "visual_query": "heavy vintage iron door locked mystery dark",
                        "camera_motion": "pan_left",
                        "audio_cue": "drone_tension",
                        "estimated_duration": 6.5
                    },
                    {
                        "id": 3,
                        "text": "Inside, dinner remained untouched on the table. A single wooden chair was knocked onto its side... as if someone had risen in sheer terror.",
                        "visual_query": "victorian dining table untouched meal overturned chair dark room",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "tension_riser",
                        "estimated_duration": 8.0
                    },
                    {
                        "id": 4,
                        "text": "Yet the most disturbing discovery was found inside the keeper's log. The final entry described a monstrous, weeping storm.",
                        "visual_query": "vintage handwritten logbook journal 1900 archive",
                        "scene_type": "highlighter",
                        "headline": "LOGBOOK DISCOVERY: PAGE 42",
                        "highlight_phrase": "A MONSTROUS WEEPING STORM NEVER RECORDED ON MAINLAND",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "camera_shutter",
                        "estimated_duration": 7.0
                    },
                    {
                        "id": 5,
                        "text": "A storm that, according to every meteorological station across the British Isles... never actually occurred.",
                        "visual_query": "stormy rough ocean waves crashing dark cliff dramatic",
                        "camera_motion": "zoom_in_slow",
                        "audio_cue": "heartbeat_thud",
                        "estimated_duration": 7.0
                    },
                    {
                        "id": 6,
                        "text": "More than a century has passed. No bodies were ever recovered. And one chilling question endures: what did they see outside that door?",
                        "visual_query": "isolated lighthouse cliff sea mist vintage noir",
                        "camera_motion": "zoom_out_slow",
                        "audio_cue": "drone_tension",
                        "estimated_duration": 8.5
                    }
                ]
            )

    # General Dynamic Fallback for ANY custom topic (True Crime, Historical Mystery, Science)
    return generate_dynamic_script(topic, language)


def generate_dynamic_script(topic: str, language: str = "en") -> DocumentaryScript:
    """
    Dynamically generates a psychological suspense script structure for any given topic.
    """
    clean_title = topic.strip().title()
    
    if language == "ro":
        titles = [
            f"Adevărul ascuns din spatele cazului: {clean_title}",
            f"Misterul nerezolvat pe care nimeni nu îl poate explica: {clean_title}",
            f"Ce s-a întâmplat cu adevărat în cazul {clean_title}?",
            f"Detaliul tulburător ignorat de toți: {clean_title}",
            f"Dosarul secret: {clean_title}"
        ]
        thumbnails = [
            {
                "layout": f"Prim-plan dramatic + Documente clasificate blurate",
                "text_overlay": "SECRET CLASAT",
                "color_palette": "Noir, contrast intens, tonuri reci",
                "image_prompt": f"Dramatic investigative documentary still about {topic}, moody lighting, archival textures, 4k"
            }
        ]
        scenes = [
            {
                "id": 1,
                "text": f"Există evenimente în istorie pe care mintea umană refuză să le creadă. Dar povestea despre {topic}... depășește orice imaginație.",
                "visual_query": f"{topic} mysterious archive historical",
                "camera_motion": "zoom_in_slow",
                "audio_cue": "heartbeat_thud",
                "estimated_duration": 6.5
            },
            {
                "id": 2,
                "text": "Totul a început aparent normal, până în clipa în care un indiciu bizar a transformat o zi obișnuită într-o enigmă absolută.",
                "visual_query": f"{topic} old police evidence crime archive",
                "camera_motion": "pan_left",
                "audio_cue": "drone_tension",
                "estimated_duration": 6.5
            },
            {
                "id": 3,
                "text": "Anchetatorii au crezut inițial că au o explicație simplă. Însă, când au examinat probele din dosar, detaliile pur și simplu nu se legau.",
                "visual_query": f"{topic} investigation forensic document vintage",
                "camera_motion": "zoom_in_slow",
                "audio_cue": "tension_riser",
                "estimated_duration": 7.0
            },
            {
                "id": 4,
                "text": "Cineva ascundea ceva. Sau poate... adevărul era atât de tulburător încât nimeni nu a îndrăznit să îl privească în față.",
                "visual_query": f"{topic} dark silhouette mystery night noir",
                "camera_motion": "zoom_out_slow",
                "audio_cue": "drone_tension",
                "estimated_duration": 6.5
            },
            {
                "id": 5,
                "text": f"Chiar și astăzi, dosarul despre {topic} continuă să ridice mai multe întrebări decât răspunsuri.",
                "visual_query": f"{topic} historic newspaper headline archive",
                "camera_motion": "zoom_in_slow",
                "audio_cue": "heartbeat_thud",
                "estimated_duration": 6.0
            }
        ]
    else:
        titles = [
            f"The Unsolved Truth Behind {clean_title}",
            f"What Actually Happened During The {clean_title} Incident?",
            f"The Disturbing Case of {clean_title}",
            f"The Mystery Nobody Can Explain: {clean_title}",
            f"The Chilling Evidence in {clean_title}"
        ]
        thumbnails = [
            {
                "layout": f"Moody forensic lighting + Subject silhouette + High stakes text",
                "text_overlay": "CLASSIFIED",
                "color_palette": "Deep shadows, teal and orange accents",
                "image_prompt": f"Cinematic documentary still for {topic}, archival dark atmospheric lighting, high quality"
            }
        ]
        scenes = [
            {
                "id": 1,
                "text": f"Some mysteries leave behind too many clues. But in the case of {clean_title}... the evidence itself makes no sense.",
                "visual_query": f"{topic} mysterious archive historical",
                "camera_motion": "zoom_in_slow",
                "audio_cue": "heartbeat_thud",
                "estimated_duration": 6.0
            },
            {
                "id": 2,
                "text": "It began as an ordinary day, until a single unsettling discovery turned this case into an enduring nightmare.",
                "visual_query": f"{topic} old police evidence crime archive",
                "camera_motion": "pan_left",
                "audio_cue": "drone_tension",
                "estimated_duration": 6.5
            },
            {
                "id": 3,
                "text": "Investigators initially suspected a routine explanation. But the physical evidence told a completely different story.",
                "visual_query": f"{topic} investigation forensic document vintage",
                "camera_motion": "zoom_in_slow",
                "audio_cue": "tension_riser",
                "estimated_duration": 7.0
            },
            {
                "id": 4,
                "text": "Witnesses contradicted each other, logs were mysteriously altered, and crucial documents seemed to vanish into thin air.",
                "visual_query": f"{topic} dark silhouette mystery night noir",
                "camera_motion": "zoom_out_slow",
                "audio_cue": "drone_tension",
                "estimated_duration": 6.5
            },
            {
                "id": 5,
                "text": f"Decades later, {clean_title} remains one of the darkest unsolved chapters in modern history.",
                "visual_query": f"{topic} historic newspaper headline archive",
                "camera_motion": "zoom_in_slow",
                "audio_cue": "heartbeat_thud",
                "estimated_duration": 6.0
            }
        ]

    return DocumentaryScript(
        topic=clean_title,
        language=language,
        titles=titles,
        thumbnail_concepts=thumbnails,
        scenes=scenes
    )


if __name__ == "__main__":
    script = get_curated_template("Flannan Isle Lighthouse Mystery", language="en")
    output_test = "output/test_script.json"
    script.save(output_test)
    print(f"Generated documentary script saved to {output_test}")
    print(f"Top 3 Viral Titles:")
    for t in script.titles[:3]:
        print(f" - {t}")
