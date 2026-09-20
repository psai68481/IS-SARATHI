"""
IS-SARATHI Generic Procurement Parser
=====================================
Converts ANY tender text into a structured procurement model:

    product          — the item being procured (product identity / head noun)
    product_subtype  — qualifiers narrowing the product ("distribution", "industrial")
    materials        — substrate words (steel, PVC, copper, ...)
    product_forms    — form words (pipe, cable, bar, sheet, ...)
    applications     — application/context words (construction, potable, mining, ...)
    quantity / unit  — procurement volume
    parameters       — extracted technical parameters
    missing          — structurally missing specification fields

The parser is domain-independent: it uses word-class lexicons (materials,
forms, applications, units) rather than product lookup tables, so it works
for any procurement line and any future knowledge-base expansion.
"""

import re
import logging
from typing import Any, Dict, List

logger = logging.getLogger("is_sarathi.parser")

# ---------------------------------------------------------------------------
# Word-class lexicons (NOT product->standard maps)
# ---------------------------------------------------------------------------

MATERIAL_WORDS = {
    "steel", "iron", "copper", "aluminium", "aluminum", "brass", "bronze",
    "zinc", "lead", "nickel", "tin", "titanium", "cast", "wrought", "galvanized",
    "pvc", "upvc", "cpvc", "hdpe", "ldpe", "pe", "polyethylene", "polypropylene",
    "pp", "abs", "rubber", "elastomer", "neoprene", "silicone", "vinyl", "xlpe",
    "glass", "ceramic", "concrete", "cement", "timber", "wood", "bamboo",
    "paper", "cardboard", "leather", "textile", "cotton", "jute",
    "crosslinked", "composite", "alloy",
}

FORM_WORDS = {
    "pipe", "pipes", "pipeline", "tube", "tubes", "tubular",
    "cable", "cables", "wire", "wires", "conductor", "cord", "cords",
    "bar", "bars", "rod", "rods", "rebar", "reinforcement",
    "sheet", "sheets", "plate", "plates", "coil", "coils", "strip", "sheeting",
    "beam", "beams", "channel", "angle", "sections", "section",
    "powder", "granules", "resin", "pellets", "film", "membrane", "liners",
    "block", "blocks", "brick", "bricks",
    "fitting", "fittings", "socket", "elbow", "flange",
    "helmet", "helmets", "glove", "gloves", "mask", "masks", "respirator",
    "footwear", "boots", "shoes", "harness", "belt", "belts",
    "transformer", "transformers", "cylinder", "cylinders", "valve", "valves",
    "extinguisher", "extinguishers", "furniture", "desk", "desks", "chair", "chairs",
    "light", "lights", "lamp", "lamps", "luminaire", "battery", "batteries",
    "meter", "meters", "switch", "switches", "bucket", "crate", "container",
    "bottle", "bottles", "bag", "bags", "sack", "sacks", "mug",
}

APPLICATION_WORDS = {
    "construction", "building", "infrastructure", "municipal", "industrial",
    "domestic", "household", "residential", "commercial", "agricultural",
    "irrigation", "sewerage", "sewage", "drainage", "mining", "underground",
    "marine", "offshore", "automotive", "vehicular", "railway", "railways",
    "hospital", "medical", "school", "office", "kitchen", "foundry",
    "welding", "chemical", "petrochemical", "pharmaceutical", "food",
    "potable", "drinking", "firefighting",
}

# Subtype qualifiers that NARROW a product noun when they precede it.
SUBTYPE_QUALIFIERS = {
    "industrial", "domestic", "commercial", "distribution", "power",
    "outdoor", "indoor", "heavy", "light", "armoured", "armored",
    "unarmoured", "unarmored", "frls", "flame", "retardant",
    "potable", "sewage", "sewerage", "structural", "reinforced",
    "deformed", "galvanized", "stainless", "seamless", "welded",
    "safety", "mining", "household", "insulated", "insulating",
}

UNIT_WORDS = {
    "bags", "bag", "units", "unit", "nos", "numbers", "no", "pcs", "pieces",
    "meters", "meter", "metres", "metre", "km", "tonnes", "tonne", "tons", "ton",
    "litres", "liters", "litre", "liter", "kg", "quintal", "sets", "set",
    "pairs", "pair", "rolls", "roll", "boxes", "box", "drums", "drum",
}

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "for", "to", "in", "on", "at", "by",
    "with", "is", "are", "be", "should", "shall", "must", "will", "we", "our",
    "need", "needed", "require", "required", "procure", "procurement", "supply",
    "supplied", "supplying", "provide", "providing", "purchase", "buying",
    "minimum", "maximum", "suitable", "between", "from", "this", "that",
    "as", "per", "various", "different", "any", "all", "new",
}

TEMP_RANGE_RE = re.compile(
    r"(-?\d+(?:\.\d+)?)\s*(?:°|deg(?:rees?)?\s*)?c\b\s*(?:to|-|–|and)\s*[-+]?\s*(\d+(?:\.\d+)?)\s*(?:°|deg(?:rees?)?\s*)?c\b",
    re.IGNORECASE,
)
TEMP_SINGLE_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*(?:°|deg(?:rees?)?\s*)?c\b", re.IGNORECASE)
PRESSURE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(mpa|bar|kg/cm2|kg/cm²|psi|kpa)\b", re.IGNORECASE)
VOLTAGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(kv|v)\b", re.IGNORECASE)
LOAD_RE = re.compile(r"(?:load|capacity|withstand)\D{0,20}(\d+(?:\.\d+)?)\s*(kg|kn|tonnes?|t)\b", re.IGNORECASE)
IS_REF_RE = re.compile(r"\bis\s*:?\s*(\d{3,5})(?::(\d{4}))?", re.IGNORECASE)


class ProcurementParser:
    """Converts tender text into a structured procurement model."""

    def _clean(self, text: str) -> str:
        return re.sub(r"\s+", " ", (text or "")).strip()

    def _tokens(self, text: str) -> List[str]:
        cleaned = re.sub(r"[^\w\s]", " ", (text or "").lower(), flags=re.UNICODE)
        return [t for t in cleaned.split() if t]

    def _safe_quantities(self, text: str) -> List[Dict[str, Any]]:
        qty_re = re.compile(
            r"\b(\d{1,3}(?:,\d{3})+|\d{2,7})\s*(bags?|units?|nos?|numbers?|pcs?|pieces?|"
            r"meters?|metres?|kms?|tonnes?|tons?|litres?|liters?|kg|quintals?|sets?|pairs?|rolls?|boxes?|drums?)?\b",
            re.IGNORECASE,
        )
        out: List[Dict[str, Any]] = []
        for m in qty_re.finditer(text or ""):
            num = m.group(1).replace(",", "")
            unit = (m.group(2) or "").lower()
            # Reject values that are clearly technical parameters (load
            # capacity) rather than procurement volumes.
            if unit in {"kg", "tonnes", "tonne", "tons", "ton"} and "load" in text[max(0, m.start() - 30):m.start()].lower():
                continue
            out.append({"quantity": num, "unit": unit or "units"})
        return out

    def _extract_parameters(self, text: str) -> List[Dict[str, str]]:
        parameters: List[Dict[str, str]] = []
        m = TEMP_RANGE_RE.search(text)
        if m:
            parameters.append({"type": "temperature_range", "min": m.group(1),
                               "max": m.group(2), "display": f"{m.group(1)}°C to {m.group(2)}°C"})
        else:
            singles = TEMP_SINGLE_RE.findall(text)
            if singles:
                parameters.append({"type": "temperature", "values": ",".join(singles[:4]),
                                   "display": ", ".join(f"{v}°C" for v in singles[:4])})
        for m in PRESSURE_RE.finditer(text):
            parameters.append({"type": "pressure", "value": m.group(1), "unit": m.group(2).lower(),
                               "display": f"{m.group(1)} {m.group(2)}"})
        for m in VOLTAGE_RE.finditer(text):
            parameters.append({"type": "voltage", "value": m.group(1), "unit": m.group(2).lower(),
                               "display": f"{m.group(1)} {m.group(2).upper()}"})
        for m in LOAD_RE.finditer(text):
            parameters.append({"type": "load", "value": m.group(1), "unit": m.group(2).lower(),
                               "display": f"{m.group(1)} {m.group(2)}"})
        return parameters

    def _missing_specifications(self, raw: str, lower: str, materials: List[str],
                                forms: List[str], applications: List[str],
                                is_refs: List[str]) -> List[str]:
        """Generic, context-driven missing-field detection (no per-domain hacks)."""
        missing: List[str] = []
        has_grade = bool(re.search(r"\b(grade|class|fe\s*\d{3}|m\d{2})\b", lower))
        has_dimension = bool(re.search(r"\b\d+(\.\d+)?\s*(mm|cm|m|in|inch|dia|diameter)\b", lower))
        has_test = bool(re.search(r"\b(test|testing|as per is|compliance)\b", lower))
        has_certification = bool(re.search(r"\b(isi|certified|certification|bis|qco)\b", lower))
        if not applications:
            missing.append("application / intended use")
        if materials and not has_grade:
            missing.append("material grade")
        if forms and not has_dimension:
            missing.append("dimensions / size")
        if not has_test:
            missing.append("testing requirement")
        if not is_refs:
            missing.append("reference standard (IS number)")
        if not has_certification:
            missing.append("certification requirement")
        return missing

    def parse(self, text: str) -> Dict[str, Any]:
        raw = self._clean(text)
        lower = raw.lower()
        words = self._tokens(raw)
        word_set = set(words)

        is_refs = [
            f"IS {m.group(1)}" + (f":{m.group(2)}" if m.group(2) else "")
            for m in IS_REF_RE.finditer(raw)
        ]

        materials = sorted(word_set & MATERIAL_WORDS)
        forms = sorted(word_set & FORM_WORDS)
        applications = sorted(word_set & APPLICATION_WORDS)

        # ---- product identity: head noun of the procurement line -------------
        product = ""
        subtype: List[str] = []
        if forms:
            first_form_idx = next(i for i, w in enumerate(words) if w in FORM_WORDS)
            head = forms[0].rstrip("s") if forms[0].endswith("s") else forms[0]
            window = words[max(0, first_form_idx - 4):first_form_idx + 1]
            product_words = [w for w in window if w not in STOPWORDS]
            product = " ".join(product_words)
            subtype = [w for w in product_words[:-1] if w in SUBTYPE_QUALIFIERS]
        elif materials:
            product = materials[0]
        elif applications:
            product = applications[0]

        quantities = self._safe_quantities(raw)
        quantity = quantities[0]["quantity"] if quantities else None
        unit = quantities[0]["unit"] if quantities else None

        return {
            "raw": raw[:4000],
            "product": product,
            "product_subtype": subtype,
            "materials": materials,
            "product_forms": forms,
            "applications": applications,
            "quantity": quantity,
            "unit": unit,
            "parameters": self._extract_parameters(raw),
            "is_references": is_refs,
            "missing_specifications": self._missing_specifications(
                raw, lower, materials, forms, applications, is_refs
            ),
            "language": self._detect_language_hint(raw),
        }

    @staticmethod
    def _detect_language_hint(text: str) -> str:
        if re.search(r"[\u0900-\u097F]", text or ""):
            return "hi"
        if re.search(r"[\u0C00-\u0C7F]", text or ""):
            return "te"
        return "en"


procurement_parser = ProcurementParser()
