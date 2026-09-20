import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger("is_sarathi.nlp")

class SpacyNLPService:
    def __init__(self):
        self.nlp = None
        try:
            import spacy
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("Loaded spaCy model en_core_web_sm")
            except Exception:
                logger.warning("spaCy en_core_web_sm model not found. Using regex NLP engine.")
        except ImportError:
            logger.warning("spaCy not installed, using regex NLP engine.")

    def extract_requirements(self, text: str) -> List[Dict[str, Any]]:
        extracted = []
        lower_text = text.lower()

        # 1. High-Precision Product Type Extraction (with strict word boundaries \b)
        product_patterns = [
            (r"\b(cement|portland\s+cement|opc|ppc|mortar)\b", "Ordinary Portland Cement (OPC)", "Classification", 99.0),
            (r"\b(tmt|rebars?|steel\s+bars?|reinforcement\s+bars?)\b", "High-Strength TMT Steel Rebars", "Classification", 98.0),
            (r"\b(helmets?|headgear|safety\s+helmet)\b", "Industrial Safety Helmet", "Classification", 98.0),
            (r"\b(pvc\s+pipes?|upvc|cpvc|plastic\s+pipes?|hdpe\s+pipes?)\b", "PVC / UPVC Piping System", "Classification", 97.0),
            (r"\b(transformers?|distribution\s+transformer)\b", "Power & Distribution Transformer", "Classification", 97.0),
            (r"\b(cables?|copper\s+wiring|frls\s+cable|power\s+cables?|electric\s+wiring)\b", "Building & Industrial Cables", "Classification", 96.0),
            (r"\b(cylinders?|lpg\s+cylinders?|gas\s+cylinder)\b", "LPG Gas Cylinder / Pressure Vessel", "Classification", 98.0),
            (r"\b(packaged\s+water|bottled\s+water|mineral\s+water)\b", "Packaged Drinking Water", "Classification", 96.0),
            (r"\b(masks?|respirators?|half\s+mask|ffp[123])\b", "Respiratory Protective Equipment", "Classification", 95.0),
            (r"\b(gloves?|electrical\s+gloves?)\b", "Electrical Insulating Gloves", "Classification", 95.0)
        ]

        found_product = False
        for pattern, label, cat, conf in product_patterns:
            if re.search(pattern, lower_text):
                extracted.append({
                    "field": "Product Type",
                    "value": label,
                    "category": cat,
                    "confidence": conf
                })
                found_product = True
                break

        if not found_product:
            if self.nlp:
                doc = self.nlp(text)
                chunks = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) <= 3]
                if chunks:
                    extracted.append({
                        "field": "Product Category",
                        "value": chunks[0].title(),
                        "category": "Classification",
                        "confidence": 85.0
                    })
            else:
                extracted.append({
                    "field": "Product Category",
                    "value": "General Procurement Item",
                    "category": "Classification",
                    "confidence": 75.0
                })

        # 2. Batch Quantity Extraction (e.g. 10,000 cement bags)
        qty_match = re.search(r"\b(\d{1,3}(?:,\d{3})+|\d{2,7})\s*(bags?|units?|nos?|numbers?|meters?|pcs?|pieces?|tonnes?|mt)?\b", lower_text)
        if qty_match:
            num = qty_match.group(1)
            unit = (qty_match.group(2) or "Units").title()
            extracted.append({
                "field": "Procurement Quantity",
                "value": f"{num} {unit}",
                "category": "Procurement Scope",
                "confidence": 98.0
            })

        # 3. Application / Infrastructure Domain
        app_patterns = [
            (r"\b(road\s+construction|highway|bridge|pavement|expressway)\b", "Road & Highway Pavement Construction", "Infrastructure"),
            (r"\b(building|commercial|hospital|residential|housing)\b", "Commercial & Institutional Infrastructure", "Infrastructure"),
            (r"\b(potable\s+water|drinking\s+water|municipal\s+supply|irrigation)\b", "Municipal Potable Water Distribution", "Infrastructure"),
            (r"\b(substation|utility\s+grid|transmission|power\s+plant)\b", "Power Generation & Grid Transmission", "Infrastructure"),
            (r"\b(mining|underground|tunnel)\b", "Underground Mining & Tunnel Excavation", "Infrastructure")
        ]
        for pattern, label, cat in app_patterns:
            if re.search(pattern, lower_text):
                extracted.append({
                    "field": "Application Context",
                    "value": label,
                    "category": cat,
                    "confidence": 96.0
                })
                break

        # 4. Compressive Strength / Grade (for Cement / Concrete / Steel)
        grade_match = re.search(r"\b(33|43|53)\s*(?:grade|mpa)?\b", lower_text)
        if "cement" in lower_text or "concrete" in lower_text:
            val = f"{grade_match.group(1)} Grade (Compressive Strength Target)" if grade_match else "43/53 Grade (Structural High-Strength)"
            extracted.append({
                "field": "Compressive Strength Grade",
                "value": val,
                "category": "Mechanical Performance",
                "confidence": 95.0
            })

        # 5. Mechanical Safety / Impact Resistance (for PPE/helmets/pipes, not cement)
        if re.search(r"\b(impact|shock|absorption|penetration|puncture|tensile|crush)\b", lower_text) and "cement" not in lower_text:
            extracted.append({
                "field": "Impact Resistance",
                "value": "Mandatory Shock Absorption Threshold",
                "category": "Mechanical Safety",
                "confidence": 95.0
            })

        # 6. Electrical Insulation
        if re.search(r"\b(electrical|dielectric|insulation|voltage|10kv|11kv|33kv|1100v)\b", lower_text):
            val = "Required"
            v_match = re.search(r"(\d+\s*kv|\d+\s*v)", lower_text)
            if v_match:
                val = f"Rated for {v_match.group(1).upper()}"
            extracted.append({
                "field": "Electrical Insulation",
                "value": val,
                "category": "Electrical Safety",
                "confidence": 93.0
            })

        # 7. Temperature Conditioning & Operating Range (Strict: requires ° or deg)
        temp_match = re.search(r"(-?\d+\s*°\s*c|-?\d+\s*°c|-?\d+\s*deg(?:rees?)?\s*c|\boperating\s+temperature\b)", lower_text)
        if temp_match and ("°" in temp_match.group(0) or "deg" in temp_match.group(0)):
            extracted.append({
                "field": "Operating Temp",
                "value": temp_match.group(0).replace(" ", "").upper(),
                "category": "Environmental",
                "confidence": 90.0
            })

        # 8. Pressure / Hydraulic Rating
        if re.search(r"\b(pressure|bar|kg/cm2|mpa|hydraulic)\b", lower_text):
            p_match = re.search(r"(\d+\s*(?:bar|kg/cm2|mpa))", lower_text)
            val = f"Rated for {p_match.group(1)}" if p_match else "Hydraulic Pressure Tested"
            extracted.append({
                "field": "Hydraulic Pressure Rating",
                "value": val,
                "category": "Fluid Mechanics",
                "confidence": 92.0
            })

        # 9. Fire Safety / FRLS
        if re.search(r"\b(fire|flame|frls|low\s+smoke|zero\s+halogen)\b", lower_text):
            extracted.append({
                "field": "Fire Safety / FRLS",
                "value": "Flame Retardant Low Smoke Zero Halogen",
                "category": "Fire Safety",
                "confidence": 95.0
            })

        return extracted

nlp_service = SpacyNLPService()
