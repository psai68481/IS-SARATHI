"""
IS-SARATHI Requirement Extraction Service
==========================================
Converts unstructured tender language into structured technical requirements.
Generic rule-based engine (regex + linguistic heuristics) with optional spaCy
fallback for noun-phrase detection. NOT limited to a fixed product list.
"""

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger("is_sarathi.nlp")

# Domain cue lexicon: term -> generic category label. Used for classification
# hints only — matching itself is done by the evidence engine over the dataset.
DOMAIN_CUES: Dict[str, str] = {
    "helmet": "Personal Protective Equipment",
    "headgear": "Personal Protective Equipment",
    "glove": "Personal Protective Equipment",
    "mask": "Personal Protective Equipment",
    "respirator": "Personal Protective Equipment",
    "footwear": "Personal Protective Equipment",
    "harness": "Personal Protective Equipment",
    "pipe": "Pipes & Plumbing",
    "plumbing": "Pipes & Plumbing",
    "cable": "Electrical & Electronics",
    "wiring": "Electrical & Electronics",
    "wire": "Electrical & Electronics",
    "transformer": "Electrical & Electronics",
    "circuit breaker": "Electrical & Electronics",
    "mcb": "Electrical & Electronics",
    "earthing": "Electrical & Electronics",
    "cement": "Civil & Construction Materials",
    "concrete": "Civil & Construction Materials",
    "rebar": "Civil & Construction Materials",
    "tmt": "Civil & Construction Materials",
    "aggregate": "Civil & Construction Materials",
    "steel": "Civil & Construction Materials",
    "cylinder": "Mechanical & Tooling",
    "valve": "Mechanical & Tooling",
    "water": "Chemical & Plastics",
    "plastic": "Chemical & Plastics",
    "furniture": "Furniture & Fixtures",
    "desk": "Furniture & Fixtures",
    "chair": "Furniture & Fixtures",
    "fire": "Firefighting & Safety Equipment",
    "extinguisher": "Firefighting & Safety Equipment",
}

_TEMP_RE = re.compile(
    r"(-?\d+(?:\.\d+)?)\s*°\s*c(?:\s*(?:to|-|–|and)\s*[-+]?\s*(\d+(?:\.\d+)?)\s*°\s*c)?",
    re.IGNORECASE,
)
_PRESSURE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(mpa|bar|kg/cm2|kg/cm²|psi|kpa)", re.IGNORECASE)
_VOLTAGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(kv|v)\b", re.IGNORECASE)
_LOAD_RE = re.compile(r"(?:load|capacity|withstand)\D{0,20}(\d+(?:\.\d+)?)\s*(kg|kn|tonnes?|t)\b", re.IGNORECASE)
_GRADE_RE = re.compile(r"\b(33|43|53)\s*(?:grade|mpa)?\b", re.IGNORECASE)
_QTY_RE = re.compile(r"\b(\d{1,3}(?:,\d{3})+|\d{2,7})\s*(bags?|units?|nos?|numbers?|meters?|pcs?|pieces?|tonnes?|litres?|liters?)?\b")
_IS_REF_RE = re.compile(r"\bis\s*:?\s*(\d{3,5})(?::(\d{4}))?", re.IGNORECASE)
_BULK_TOKENS_RE = re.compile(r"\b(impact|shock|absorption|penetration|puncture|tensile|crush|compressive|flexural)\b", re.IGNORECASE)
_FIRE_RE = re.compile(r"\b(fire|flame|frls|low[\s-]+smoke|zero[\s-]+halogen|fire[\s-]+retardant)\b", re.IGNORECASE)
_ELEC_RE = re.compile(r"\b(electrical|dielectric|insulation|insulated|voltage|switch)\b", re.IGNORECASE)
_WATER_RE = re.compile(r"\b(potable|drinking|water\s+supply|sewerage|irrigation)\b", re.IGNORECASE)


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

    # ------------------------------------------------------------------
    def _classify_domain(self, lower_text: str) -> str:
        best_cat, best_hits = "General Procurement", 0
        for cue, cat in DOMAIN_CUES.items():
            hits = lower_text.count(cue)
            if hits > best_hits:
                best_cat, best_hits = cat, hits
        return best_cat

    def extract_requirements(self, text: str) -> List[Dict[str, Any]]:
        """
        Extracts structured technical requirements from any tender text.
        Returns a list of {field, value, category, confidence} dicts.
        """
        extracted: List[Dict[str, Any]] = []
        if not text or not text.strip():
            return extracted

        lower_text = text.lower()
        domain = self._classify_domain(lower_text)

        # ---- 1. Product / subject identification ----
        product_found = False
        for cue, cat in DOMAIN_CUES.items():
            if re.search(rf"\b{re.escape(cue)}\w*\b", lower_text):
                extracted.append({
                    "field": "Product Domain",
                    "value": cat,
                    "category": "Classification",
                    "confidence": 90.0,
                })
                product_found = True
                break

        if not product_found:
            if self.nlp:
                doc = self.nlp(text)
                chunks = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) <= 3]
                if chunks:
                    extracted.append({
                        "field": "Product Category",
                        "value": chunks[0].title(),
                        "category": "Classification",
                        "confidence": 75.0,
                    })
                else:
                    extracted.append({
                        "field": "Product Category",
                        "value": "General Procurement Item",
                        "category": "Classification",
                        "confidence": 60.0,
                    })
            else:
                extracted.append({
                    "field": "Product Category",
                    "value": "General Procurement Item",
                    "category": "Classification",
                    "confidence": 60.0,
                })

        # ---- 2. Explicit IS references cited in tender ----
        for m in _IS_REF_RE.finditer(text):
            ref = f"IS {m.group(1)}" + (f":{m.group(2)}" if m.group(2) else "")
            extracted.append({
                "field": "Referenced Standard",
                "value": ref,
                "category": "Normative Reference",
                "confidence": 99.0,
            })

        # ---- 3. Temperature requirement(s) ----
        temps = _TEMP_RE.findall(lower_text)
        if temps:
            if temps[0][1]:  # range form
                extracted.append({
                    "field": "Operating Temperature Range",
                    "value": f"{temps[0][0]}°C to {temps[0][1]}°C",
                    "category": "Environmental",
                    "confidence": 95.0,
                })
            else:
                vals = [t[0] for t in temps]
                extracted.append({
                    "field": "Operating Temperature",
                    "value": ", ".join(f"{v}°C" for v in vals[:4]),
                    "category": "Environmental",
                    "confidence": 90.0,
                })

        # ---- 4. Pressure rating ----
        pressures = _PRESSURE_RE.findall(lower_text)
        if pressures:
            val, unit = pressures[0]
            extracted.append({
                "field": "Pressure Rating",
                "value": f"{val} {unit}".upper(),
                "category": "Mechanical Performance",
                "confidence": 92.0,
            })

        # ---- 5. Voltage / electrical rating ----
        voltages = _VOLTAGE_RE.findall(lower_text)
        if voltages and _ELEC_RE.search(lower_text):
            val, unit = voltages[0]
            extracted.append({
                "field": "Electrical Rating",
                "value": f"{val} {unit}".upper(),
                "category": "Electrical Safety",
                "confidence": 93.0,
            })
        elif _ELEC_RE.search(lower_text):
            extracted.append({
                "field": "Electrical Insulation",
                "value": "Required",
                "category": "Electrical Safety",
                "confidence": 85.0,
            })

        # ---- 6. Load / mechanical capacity ----
        loads = _LOAD_RE.findall(lower_text)
        if loads:
            val, unit = loads[0]
            extracted.append({
                "field": "Load Capacity",
                "value": f"≥ {val} {unit}".upper(),
                "category": "Mechanical Performance",
                "confidence": 92.0,
            })

        # ---- 7. Mechanical safety / impact tests ----
        if _BULK_TOKENS_RE.search(lower_text):
            extracted.append({
                "field": "Mechanical Test Requirement",
                "value": "Impact / strength testing mandated by tender",
                "category": "Mechanical Safety",
                "confidence": 88.0,
            })

        # ---- 8. Fire safety ----
        if _FIRE_RE.search(lower_text):
            extracted.append({
                "field": "Fire Safety Requirement",
                "value": "Flame-retardant / low-smoke performance specified",
                "category": "Fire Safety",
                "confidence": 90.0,
            })

        # ---- 9. Water / plumbing context ----
        if _WATER_RE.search(lower_text):
            extracted.append({
                "field": "Application Context",
                "value": "Potable water / fluid distribution system",
                "category": "Infrastructure",
                "confidence": 88.0,
            })

        # ---- 10. Compressive strength grade (cement / concrete) ----
        if "cement" in lower_text or "concrete" in lower_text:
            grade_match = _GRADE_RE.search(lower_text)
            val = f"{grade_match.group(1)} Grade" if grade_match else "Structural Grade (unspecified)"
            extracted.append({
                "field": "Compressive Strength Grade",
                "value": val,
                "category": "Mechanical Performance",
                "confidence": 90.0,
            })

        # ---- 11. Procurement quantity ----
        qty_match = _QTY_RE.search(lower_text)
        if qty_match:
            num = qty_match.group(1)
            unit = (qty_match.group(2) or "Units").title()
            extracted.append({
                "field": "Procurement Quantity",
                "value": f"{num} {unit}",
                "category": "Procurement Scope",
                "confidence": 95.0,
            })

        return extracted


nlp_service = SpacyNLPService()
