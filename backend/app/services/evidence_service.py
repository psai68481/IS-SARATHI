"""
IS-SARATHI Evidence-First Recommendation Engine
================================================
Dataset-bound recommendation pipeline. NO hardcoded product arrays.

Pipeline (per SIH26108 spec):
  1. Multilingual normalization + language detection
  2. Generic hybrid retrieval: keyword (BM25-style) + semantic (embeddings) + metadata
  3. Requirement <-> clause evidence scoring (every clause match = evidence)
  4. Coverage map (requirement -> clause evidence), gap detection, conflict detection
  5. Standards relationship graph traversal (test method / safety / material / normative)
  6. Confidence calibration from measurable signals (not LLM-generated)
  7. Honest abstention when evidence is insufficient
"""

import re
import math
import unicodedata
import uuid
import logging
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.standard import Standard, StandardClause
from app.services.embedding_service import embedding_service
from app.services.nlp_service import nlp_service
from app.services.procurement_parser import procurement_parser, APPLICATION_WORDS
from app.services.compatibility_service import compatibility_engine, CONTRAST_FAMILY_WORDS, FORM_WORDS

logger = logging.getLogger("is_sarathi.evidence")

# ---------------------------------------------------------------------------
# Generic multilingual term map. Canonical English term -> language variants.
# Used ONLY for normalization, never for direct product -> standard mapping.
# ---------------------------------------------------------------------------
MULTILINGUAL_TERMS: Dict[str, List[str]] = {
    "helmet": ["helmet", "headgear", "hard hat", "हेलमेट", "हैलमेट", "टोपी", "హెల్మెట్", "తలంతో గట్టి"],
    "pipe": ["pipe", "pipes", "pipeline", "tubular", "पाइप", "పైప్", "గొట్టం"],
    "cement": ["cement", "opc", "ppc", "portland", "सीमेंट", "సిమెంట్"],
    "cable": ["cable", "cables", "wiring", "wire", "wires", "conductor", "केबल", "तार", "केबुल", "కేబుల్", "వైర్"],
    "transformer": ["transformer", "ट्रांसफॉर्मर", "ट्रान्सफार्मर", "ट्रांसफार्मर", "ट्रांसफ़ॉर्मर", "ట్రాన్స్‌ఫార్మర్", "ట్రాన్స్‌ఫార్మర్"],
    "glove": ["glove", "gloves", "दस्ताने", "గ్లవ్స్", "చేతి రక్షణ"],
    "mask": ["mask", "masks", "respirator", "मास्क", "मुखौटा", "మాస్క్", "రెస్పిరేటర్"],
    "footwear": ["footwear", "shoes", "boots", "जूते", "बूट", "బూట్లు", "జుత్తు"],
    "harness": ["harness", "belt", "belts", "fall protection", "पट्टा", "हार्नेस", "హార్నెస్"],
    "cylinder": ["cylinder", "cylinders", "गैस सिलेंडर", "सिलेंडर", "సిలిండర్"],
    "fire extinguisher": ["fire extinguisher", "अग्निशामक", "అగ్నిమాపక", "ఫైర్ ఎక్స్టింగ్విషర్"],
    "street light": ["street light", "street lights", "streetlight", "स्ट्रीट लाइट", "స్ట్రీట్ లైట్", "లైట్"],
    "water": ["water", "पानी", "నీరు", "నీళ్లు"],  # no bare "जल": substring inside बिजली (electricity)
    "safety": ["safety", "सुरक्षा", "భద్రత", "రక్షణ"],
    "electrical": ["electrical", "electric", "बिजली", "विद्युत", "ఎలక్ట్రికల్", "విద్యుత్"],
    "construction": ["construction", "निर्माण", "निर्माण कार्य", "నిర్మాణం"],
    "furniture": ["furniture", "desk", "desks", "chair", "chairs", "फर्नीचर", "मेज", "कुर्सी", "ఫర్నిచర్", "బల్ల", "కుర్చీ"],
    "steel": ["steel", "इस्पात", "स्टील", "స్టీల్"],
    "lead": ["lead", "सीसा", "లెడ్"],
    "zinc": ["zinc", "जस्ता", "जिंक", "జింక్"],
    "switch": ["switch", "स्विच", "స్విచ్"],
    "plywood": ["plywood", "प्लाईवुड", "ప్లైవుడ్"],
}

# Language detection hints (script + common word cues)
LANGUAGE_HINTS: Dict[str, List[str]] = {
    "hi": ["हेलमेट", "पाइप", "सीमेंट", "केबल", "ट्रांसफॉर्मर", "स्ट्रीट लाइट", "खरीद", "नगरपालिका", "प्राप्त", "आवश्यकता", "सुरक्षा", "के लिए"],
    "te": ["హెల్మెట్", "పైప్", "సిమెంట్", "కేబుల్", "ట్రాన్స్‌ఫార్మర్", "స్ట్రీట్ లైట్", "కొనుగోలు", "మున్సిపాలిటీ", "కోసం", "అవసరం"],
}


def normalize_text(value: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace. Keeps Unicode letters."""
    if not value:
        return ""
    value = value.lower().strip()
    value = value.replace("–", "-").replace("—", "-")
    value = value.replace("\u200c", "").replace("\u200d", "")  # ZWJ/ZWNJ
    cleaned: List[str] = []
    for ch in value:
        if ch.isalnum() or unicodedata.category(ch).startswith(("L", "N", "M")):
            cleaned.append(ch)
        else:
            cleaned.append(" ")
    return re.sub(r"\s+", " ", "".join(cleaned)).strip()


def detect_language(query: str) -> str:
    lowered = (query or "").lower()
    for lang, hints in LANGUAGE_HINTS.items():
        if any(h in lowered for h in hints):
            return lang
    return "en"


def _tokenize(text: str) -> List[str]:
    return [t for t in normalize_text(text).split() if len(t) > 1]


STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "for", "to", "in", "on", "at", "by", "with",
    "is", "are", "be", "should", "shall", "must", "will", "we", "our", "need", "needed",
    "require", "required", "requires", "procure", "procurement", "supply", "supplied",
    "minimum", "maximum", "suitable", "between", "from", "this", "that", "these", "those",
    "all", "any", "which", "what", "who", "how", "per", "as", "it", "its", "no", "not",
    # Generic standards-vocabulary words that carry no product discrimination
    "specification", "specifications", "standard", "standards", "code", "practice",
    "methods", "method", "general", "requirements", "requirement", "part", "parts",
    "grade", "type", "types", "class", "series", "including", "up",
}


def _stem(token: str) -> str:
    """Crude but symmetric stemmer: strip trailing plural 's'. Applied to both
    tender and standard tokens so 'helmets' matches 'helmet' and Hindi-injected
    canonical terms can match English titles."""
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss") and not token.endswith("us"):
        return token[:-1]
    return token


def _content_tokens(text: str) -> List[str]:
    return [_stem(t) for t in _tokenize(text) if t not in STOPWORDS]


# ---------------------------------------------------------------------------
# Numeric requirement extraction (temperature, pressure, voltage, load, etc.)
# ---------------------------------------------------------------------------
_TEMP_RANGE_RE = re.compile(
    r"(-?\d+(?:\.\d+)?)\s*(?:°|deg(?:rees?)?\s*)?c\b\s*(?:to|-|–|and)\s*[-+]?\s*(\d+(?:\.\d+)?)\s*(?:°|deg(?:rees?)?\s*)?c\b",
    re.IGNORECASE,
)
_TEMP_SINGLE_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*(?:°|deg(?:rees?)?\s*)?c\b", re.IGNORECASE)
_PRESSURE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(mpa|bar|kg/cm2|kg/cm²|psi|kpa)\b", re.IGNORECASE)
_VOLTAGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(kv|v)\b", re.IGNORECASE)
_LOAD_RE = re.compile(r"(?:load|capacity|withstand)\D{0,20}(\d+(?:\.\d+)?)\s*(kg|kn|tonnes?|t)\b", re.IGNORECASE)
_SIZE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(mm|cm|m)\b")
_BULK_RE = re.compile(r"\b(\d{1,3}(?:,\d{3})+|\d{2,7})\s*(bags?|units?|nos?|numbers?|meters?|pcs?|pieces?|tonnes?|litres?|liters?)?\b")


def _extract_numeric_requirements(text: str) -> List[Dict[str, str]]:
    """Extract measurable numeric requirements used for conflict detection + coverage."""
    out: List[Dict[str, str]] = []
    norm = normalize_text(text)

    m = _TEMP_RANGE_RE.search(norm)
    if m:
        out.append({"type": "temperature_range", "min": m.group(1), "max": m.group(2),
                    "display": f"{m.group(1)}°C to {m.group(2)}°C"})
    else:
        singles = _TEMP_SINGLE_RE.findall(norm)
        if singles:
            out.append({"type": "temperature", "values": ",".join(singles),
                        "display": ", ".join(f"{v}°C" for v in singles[:4])})

    for m in _PRESSURE_RE.finditer(norm):
        out.append({"type": "pressure", "value": m.group(1), "unit": m.group(2).lower(),
                    "display": f"{m.group(1)} {m.group(2)}"})
    for m in _VOLTAGE_RE.finditer(norm):
        out.append({"type": "voltage", "value": m.group(1), "unit": m.group(2).lower(),
                    "display": f"{m.group(1)} {m.group(2).upper()}"})
    for m in _LOAD_RE.finditer(norm):
        out.append({"type": "load", "value": m.group(1), "unit": m.group(2).lower(),
                    "display": f"{m.group(1)} {m.group(2)}"})
    for m in _SIZE_RE.finditer(norm):
        out.append({"type": "size", "value": m.group(1), "unit": m.group(2).lower(),
                    "display": f"{m.group(1)} {m.group(2)}"})
    return out


def _extract_clauses_numbers(query: str) -> List[str]:
    """Detect explicit IS standard references in the tender text, e.g. 'IS 2925:1984'."""
    refs = []
    for m in re.finditer(r"\bis\s*:?\s*(\d{3,5})", query, re.IGNORECASE):
        refs.append(f"IS {m.group(1)}")
    return refs


def _parse_limit_number(limit_text: Optional[str]) -> Optional[Tuple[str, float]]:
    """Parse a clause test_limit into (unit_kind, value) for numeric conflict checks.
    For temperature ranges, the MAXIMUM (rating ceiling) is returned."""
    if not limit_text:
        return None
    t = normalize_text(limit_text)
    temps = [float(m.group(1)) for m in _TEMP_SINGLE_RE.finditer(t)]
    if temps:
        return ("temperature", max(temps))
    for m in _VOLTAGE_RE.finditer(t):
        return ("voltage", float(m.group(1)))
    for m in _PRESSURE_RE.finditer(t):
        return ("pressure", float(m.group(1)))
    return None


# Domain/aspect words that must NEVER act as product-noun scope gates: they are
# adjectives or context words, not product identities (e.g. "Rubber Gloves for
# Electrical Purposes" must not match a transformer tender via "electrical").
DOMAIN_ASPECT_WORDS = {
    "safety", "electrical", "electric", "water", "construction", "general",
    "purpose", "purposes", "equipment", "system", "supply", "working",
}

# Tender requirement aspect -> clause token vocabulary that can evidence it
ASPECT_TOKENS: Dict[str, set] = {
    "Mechanical Test Requirement": {"impact", "shock", "absorption", "penetration", "puncture", "tensile", "crush", "compressive", "flexural", "strength"},
    "Fire Safety Requirement": {"fire", "flame", "frls", "smoke", "halogen", "retardant", "oxygen"},
    "Electrical Insulation": {"electrical", "dielectric", "insulation", "insulated", "voltage", "kv", "resistivity"},
    "Electrical Rating": {"electrical", "dielectric", "insulation", "voltage", "kv", "withstand"},
    "Compressive Strength Grade": {"compressive", "strength", "mpa", "grade"},
    "Pressure Rating": {"pressure", "hydrostatic", "hydraulic", "bar", "mpa"},
    "Operating Temperature": {"temperature", "thermal", "conditioning", "vicat"},
    "Operating Temperature Range": {"temperature", "thermal", "conditioning", "vicat"},
}

# Application qualifiers: a standard titled for application A should be demoted
# when the tender clearly targets a DIFFERENT application B (e.g. a mining helmet
# standard for a construction tender). Each qualifier lists its cue words in
# title/scope space AND the multilingual canonical cues that trigger it.
APPLICATION_QUALIFIERS: Dict[str, Dict[str, Any]] = {
    "mining": {"doc_words": {"mining", "underground", "tunnel", "mine"}, "cues": {"mining", "underground", "tunnel"}},
    "construction_industrial": {"doc_words": {"construction", "industrial", "building", "general"}, "cues": {"construction", "industrial", "building"}},
    "automotive": {"doc_words": {"motorcyclist", "automotive", "two wheeler", "vehicular"}, "cues": {"motorcycle", "automotive", "vehicle"}},
    "domestic": {"doc_words": {"household", "domestic"}, "cues": {"household", "domestic"}},
}


def _query_qualifiers(canonical_terms: List[str], norm_query: str) -> set:
    found = set()
    for q_name, q_def in APPLICATION_QUALIFIERS.items():
        for cue in q_def["cues"]:
            if cue in canonical_terms or cue in norm_query:
                found.add(q_name)
                break
    return found


def _doc_qualifiers(std_norm: str) -> set:
    found = set()
    for q_name, q_def in APPLICATION_QUALIFIERS.items():
        for word in q_def["doc_words"]:
            if word in std_norm:
                found.add(q_name)
                break
    return found


# ---------------------------------------------------------------------------
# Recommendation Stability Check (SIH26108 feature #24)
# Perturbs the tender one requirement at a time and re-runs the pipeline to
# measure how sensitive the recommendation is to each specification line.
# ---------------------------------------------------------------------------

# Requirement phrases that can be safely dropped when testing sensitivity.
# Anchored to the same aspect vocabulary the NLP extractor uses.
_PERTURB_PATTERNS: List[Tuple[str, str]] = [
    ("Electrical Insulation", r"\b(?:with|and|including)?\s*(?:high[-\s]voltage\s+)?(?:electrical\s+)?(?:insulation|insulated|dielectric)\b"),
    ("Mechanical Test Requirement", r"\b(?:with|and|including)?\s*(?:impact|shock|puncture|penetration|tensile|crush)\s+(?:resistance|strength)\b"),
    ("Mechanical Test Requirement", r"\bwith\s+impact\s+resistance\b"),
    ("Fire Safety Requirement", r"\b(?:with|and)?\s*flame\s*retardant\b|\bFRLS\b"),
    ("Operating Temperature", r"\boperating\s+(?:at\s+)?(?:-?\d+\s*°?\s*C(?:\s*(?:to|-|–)\s*[+-]?\d+\s*°?\s*C)?)\b"),
    ("Pressure Rating", r"\b(?:rated|working|pressure)\s+(?:of\s+|to\s+)?\d+(?:\.\d+)?\s*(?:mpa|bar|kg/cm2|psi|kpa)\b"),
    ("Electrical Rating", r"\b(?:rated\s+)?\d+\s*(?:kv|v)\b"),
]


def _trim_punctuation(fragment: str) -> str:
    return fragment.strip(" ,.;:\t\n-")


def build_perturbations(text: str) -> List[Dict[str, str]]:
    """Generate one-at-a-time tender variants used by the stability check.

    For each recognized requirement we emit two variants:
      remove     — the requirement phrase is deleted (does the rec survive?)
      emphasized — the requirement phrase is stated twice (does the ranking lock in?)
    """
    variants: List[Dict[str, str]] = []
    seen_labels = set()
    for label, pattern in _PERTURB_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if not m:
            continue
        if label in seen_labels:
            continue
        seen_labels.add(label)
        fragment = _trim_punctuation(m.group(0))
        if not fragment or len(fragment) < 4:
            continue
        removed = (text[:m.start()] + " " + text[m.end():])
        removed = re.sub(r"\s+", " ", removed).replace(" ,", ",").replace(" .", ".").strip(" ,.")
        if removed:
            variants.append({"kind": "remove", "label": label, "fragment": fragment, "text": removed})
        variants.append({"kind": "emphasize", "label": label, "fragment": fragment,
                         "text": f"{text} {fragment}. {fragment}."})
    return variants[:8]  # cap: at most 8 perturbation runs


class EvidenceService:
    """Evidence-first analysis. All output is derived from DB rows — never invented."""

    # Confidence weights (presented as OUR system design, not official BIS probabilities)
    W_SEMANTIC = 0.25
    W_KEYWORD = 0.35
    W_COVERAGE = 0.20
    W_VALIDITY = 0.10
    W_GRAPH = 0.10

    MIN_CONFIDENCE = 50.0   # below this -> abstain
    MIN_SEMANTIC = 0.30     # semantic floor for candidates with no keyword support
    MIN_KEYWORD = 0.15      # keyword floor for candidates with no semantic support

    def analyze_requirement(self, db: Optional[Session], query: str) -> Dict[str, Any]:
        text = (query or "").strip()
        if not text:
            return self._abstain("Empty input. Provide a procurement specification.",
                                 detected_product="Unspecified", language="en")

        language = detect_language(text)
        norm_query = normalize_text(text)
        query_tokens = _content_tokens(text)
        numeric_reqs = _extract_numeric_requirements(text)
        explicit_refs = _extract_clauses_numbers(text)

        # Canonicalize multilingual terms into the query so English KB matches.
        # The canonical tokens are injected into the semantic/keyword text so a
        # Hindi or Telugu tender can match an English standard title.
        canonical_terms: List[str] = []
        for canonical, variants in MULTILINGUAL_TERMS.items():
            for v in variants:
                if v in norm_query:
                    canonical_terms.append(canonical)
                    break
        if canonical_terms:
            text_for_match = f"{text} {' '.join(canonical_terms)}"
            norm_query = normalize_text(text_for_match)
            query_tokens = _content_tokens(text_for_match)

        # ------------------------------------------------------------------
        # STRUCTURED PROCUREMENT MODEL (generic, domain-independent)
        # ------------------------------------------------------------------
        model = procurement_parser.parse(text_for_match if canonical_terms else text)
        detected_product = model.get("product") or "Unspecified"

        standards: List[Standard] = []
        if db is not None:
            try:
                standards = db.query(Standard).all()
            except Exception as exc:
                logger.warning("Could not query standards: %s", exc)

        if not standards:
            return self._abstain(
                "Knowledge base is empty. Seed verified standards before analysis.",
                detected_product="Unspecified", language=language,
            )

        # ------------------------------------------------------------------
        # HYBRID RETRIEVAL + EVIDENCE SCORING over every standard
        # ------------------------------------------------------------------
        # Corpus-derived product nouns: query tokens that appear in >= 1 standard
        # title, excluding generic domain/aspect words. Used as a scope gate — a
        # standard about a DIFFERENT product must not win the ranking.
        title_token_counts: Dict[str, int] = {}
        for std in standards:
            for t in set(_content_tokens(std.title or "")):
                title_token_counts[t] = title_token_counts.get(t, 0) + 1
        product_nouns = {
            t for t in set(query_tokens)
            if title_token_counts.get(t, 0) >= 1 and t not in DOMAIN_ASPECT_WORDS
        }

        query_embedding = embedding_service.embed_text(text_for_match if canonical_terms else text)
        # For multilingual tenders the canonical English terms ARE the common technical
        # representation: score keyword overlap against them only, so Devanagari/Telugu
        # noise tokens do not dilute the overlap denominator.
        if canonical_terms:
            query_token_set = set(_content_tokens(" ".join(canonical_terms)))
        else:
            query_token_set = set(query_tokens)
        # Broadened token set for clause-level evidence: adds the full query so clause
        # rows written in English can still match a Hindi/Telugu tender's details.
        expanded_token_set = query_token_set | set(_content_tokens(text))

        scored: List[Dict[str, Any]] = []
        for std in standards:
            title = std.title or ""
            scope = std.scope or ""
            std_text = f"{std.is_number} {title} {scope}"
            std_norm = normalize_text(std_text)
            std_tokens = set(_content_tokens(std_text))
            title_tokens = set(_content_tokens(title))

            # -- Keyword score: token overlap with TITLE weighted higher than scope,
            #    then penalized for title terms the tender never mentions (BM25-style
            #    title precision). This stops a niche sibling standard (e.g. a mining
            #    helmet) from outranking the exact product-title match.
            overlap_tokens = query_token_set & std_tokens
            keyword_score = len(overlap_tokens) / max(len(query_token_set), 1)
            title_overlap = query_token_set & title_tokens
            title_covered = len(title_overlap) / max(len(title_tokens), 1) if title_tokens else 0.0
            keyword_score += 0.45 * title_covered
            title_miss = 1.0 - title_covered
            keyword_score *= (1.0 - 0.45 * title_miss)
            keyword_score = min(keyword_score, 1.0)

            # -- Semantic (embedding cosine via shared service) --
            std_emb = embedding_service.embed_text(std_text)
            semantic_score = max(0.0, embedding_service.compute_similarity(query_embedding, std_emb))

            # -- Scope gate: standard is about a different product --
            scope_tokens = std_tokens  # title + scope already tokenized
            scope_mismatch = bool(product_nouns) and not (product_nouns & scope_tokens)
            if scope_mismatch:
                keyword_score *= 0.25
                semantic_score *= 0.50

            # -- Metadata boosts (transparent, dataset-driven) --
            # Multilingual signal: canonical product terms are matched against the
            # standard's TITLE (strong signal) and full text (weak signal), including
            # native-language title variants (title_ml) for Hindi/Telugu standards.
            std_ml_norm = normalize_text(getattr(std, "title_ml", None) or "")
            std_ml_tokens = set(_content_tokens(std_ml_norm)) if std_ml_norm else set()
            canonical_in_title = sum(
                1 for c in canonical_terms
                if _stem(c) in title_tokens or _stem(c) in std_ml_tokens
            )
            canonical_in_scope = sum(1 for c in canonical_terms if c in std_norm)
            multilingual_hit = canonical_in_scope > 0
            explicit_hit = any(ref.lower() in std_norm for ref in explicit_refs)

            ml_boost = 0.18 * min(canonical_in_scope, 2) + 0.30 * min(canonical_in_title, 2)
            keyword_score = min(1.0, keyword_score + ml_boost
                                + (0.60 if explicit_hit else 0.0))

            # Validity penalty at retrieval stage: superseded/withdrawn standards are
            # demoted so a CURRENT standard with equal evidence always wins.
            validity_factor = self._validity_factor(std)
            if validity_factor < 0.5:
                keyword_score *= 0.35
                semantic_score = semantic_score * 0.60

            # Application-qualifier contrast: standard for application A vs tender for
            # application B (e.g. mining helmet standard vs construction tender).
            # Only applies when BOTH sides carry a distinct qualifier.
            q_quals = _query_qualifiers(canonical_terms, norm_query)
            if q_quals:
                d_quals = _doc_qualifiers(std_norm)
                if d_quals and not (q_quals & d_quals):
                    # Document is qualified for a DIFFERENT application -> demote
                    keyword_score *= 0.30
                    semantic_score = semantic_score * 0.70

            # Clause-level evidence
            clauses: List[StandardClause] = []
            if db is not None:
                try:
                    clauses = db.query(StandardClause).filter(
                        StandardClause.standard_id == std.id).all()
                except Exception:
                    clauses = []

            # -- Evidence scoring: each clause matching a query token/number = evidence --
            clause_evidence: List[Dict[str, Any]] = []
            clause_semantic_total = 0.0
            for clause in clauses:
                clause_text = f"{clause.title} {clause.requirement_text or ''} {clause.tested_parameter or ''}"
                clause_norm = normalize_text(clause_text)
                clause_emb = embedding_service.embed_text(clause_text)
                clause_sem = max(0.0, embedding_service.compute_similarity(query_embedding, clause_emb))
                clause_kw = len(expanded_token_set & set(_content_tokens(clause_text))) / max(len(expanded_token_set), 1)

                # Numeric requirement satisfied by clause limit?
                numeric_match = self._numeric_evidence(numeric_reqs, clause.test_limit, clause.requirement_text)
                evidence_strength = 0.55 * clause_sem + 0.20 * clause_kw + (0.25 if numeric_match else 0.0)
                if evidence_strength >= 0.30:
                    clause_evidence.append({
                        "clause_number": clause.clause_number,
                        "title": clause.title,
                        "requirement_text": clause.requirement_text or "",
                        "test_limit": clause.test_limit or "",
                        "tested_parameter": clause.tested_parameter or "",
                        "strength": round(evidence_strength, 3),
                        "numeric_match": numeric_match,
                        "semantic": clause_sem,
                    })
                    clause_semantic_total += clause_sem

            n_clauses = len(clauses) or 1
            clause_semantic_boost = min(0.20, (clause_semantic_total / n_clauses) * 0.40)
            semantic_score = min(1.0, semantic_score + clause_semantic_boost)

            base_keyword_overlap = len(overlap_tokens) / max(len(query_token_set), 1)
            if not (semantic_score >= self.MIN_SEMANTIC
                    or base_keyword_overlap >= self.MIN_KEYWORD
                    or explicit_hit):
                continue  # not a candidate at all

            scored.append({
                "standard": std,
                "semantic": semantic_score,
                "keyword": keyword_score,
                "clauses": clauses,
                "clause_evidence": clause_evidence,
                "explicit_hit": explicit_hit,
                "multilingual_hit": multilingual_hit,
                "scope_mismatch": scope_mismatch,
            })

        # ------------------------------------------------------------------
        # COMPATIBILITY GATE + REJECTION RECORD (generic, 8-check engine)
        # Retrieval similarity only generated candidates. Compatibility decides.
        # ------------------------------------------------------------------
        # Rerank retrieval candidates first: the gate only needs to run on the
        # most similar standards, in line with retrieval -> gates -> evidence.
        scored.sort(key=lambda x: (0.65 * x["semantic"] + 0.35 * x["keyword"]), reverse=True)
        retrieval_candidates = scored[:10]

        rejected: List[Dict[str, Any]] = []
        compatible: List[Dict[str, Any]] = []
        for cand in retrieval_candidates:
            std = cand["standard"]
            verdict = compatibility_engine.evaluate(model, std, cand["clauses"], cand["clause_evidence"])
            cand["compatibility"] = verdict
            if verdict["compatible"]:
                compatible.append(cand)
            else:
                rejected.append({
                    "standard": std,
                    "verdict": verdict,
                    "confidence": round(min(0.65 * cand["semantic"] + 0.35 * cand["keyword"], 1.0) * 100, 1),
                })

        # Keep top 8 compatible candidates for deep analysis
        compatible.sort(key=lambda x: (0.65 * x["semantic"] + 0.35 * x["keyword"]), reverse=True)
        candidates = compatible[:8]

        if not candidates:
            # Distinguish "nothing retrieved" from "retrieved but rejected by gates"
            if rejected:
                det = detected_product if detected_product != "Unspecified" else "Unspecified"
                return self._abstain(
                    "Candidate standards were retrieved by similarity but rejected by the "
                    "product/scope compatibility gates — their verified scope does not cover "
                    "the requested product.",
                    detected_product=det,
                    language=language,
                    gaps=[
                        f"{len(rejected)} similar standard(s) evaluated; none compatible with the detected product '{det}'.",
                        "No verified applicable Indian Standard was found in the current IS-SARATHI knowledge base.",
                    ],
                    rejected_candidates=rejected,
                    status="REJECTED_SCOPE_INCOMPATIBLE",
                )
            return self._abstain(
                "No standard in the verified knowledge base matches this specification.",
                detected_product=detected_product,
                language=language,
                gaps=["No candidate standard passed the hybrid semantic + keyword retrieval gate.",
                      "No verified applicable Indian Standard was found in the current IS-SARATHI knowledge base.",
                      "Provide the intended application, material, operating conditions or testing requirement."],
                status="NOT_FOUND_IN_DATASET",
            )

        # Clause lookup: standard_id -> {clause_number -> clause} for keyClause mapping
        clauses_by_number: Dict[str, Dict[str, StandardClause]] = {}
        for cand in candidates:
            clauses_by_number[cand["standard"].id] = {
                cl.clause_number: cl for cl in cand["clauses"]
            }

        # ------------------------------------------------------------------
        # DEEP ANALYSIS per candidate: coverage, conflicts, related standards
        # ------------------------------------------------------------------
        analyzed: List[Dict[str, Any]] = []
        for cand in candidates:
            std = cand["standard"]
            coverage, uncovered, conflicts = self._analyze_coverage(
                text_for_match if canonical_terms else text, norm_query, numeric_reqs, cand)
            related = self._related_standards(db, std)
            validity = self._validity_factor(std)
            graph_factor = min(1.0, 0.5 + 0.5 * min(len(related), 3) / 3)

            confidence = self._calibrate_confidence(
                semantic=cand["semantic"],
                keyword=cand["keyword"],
                coverage=coverage,
                validity=validity,
                graph=graph_factor,
                explicit=cand["explicit_hit"],
            )

            analyzed.append({
                "standard": std,
                "semantic": cand["semantic"],
                "keyword": cand["keyword"],
                "confidence": confidence,
                "coverage": coverage,
                "uncovered": uncovered,
                "conflicts": conflicts,
                "related": related,
                "validity": validity,
                "clause_evidence": cand["clause_evidence"],
                "explicit_hit": cand["explicit_hit"],
                "scope_mismatch": cand["scope_mismatch"],
            })

        analyzed.sort(key=lambda x: x["confidence"], reverse=True)
        top = analyzed[0]

        # ------------------------------------------------------------------
        # ABSTENTION GATE: honest "I don't know" instead of forcing an answer
        # ------------------------------------------------------------------
        if top["confidence"] < self.MIN_CONFIDENCE:
            why_not = [self._why_not(a, top) for a in analyzed[1:4]]
            return {
                "status": "LOW_CONFIDENCE",
                "recommendations": [],
                "gaps": self._abstention_gaps(analyzed),
                "conflicts": [],
                "why_not_alternatives": why_not,
                "audit_id": str(uuid.uuid4()),
                "detected_product": self._product_label(top["standard"]),
                "language": language,
                "human_verification_required": True,
                "abstention_reason": (
                    f"Best candidate {top['standard'].is_number} reached only "
                    f"{top['confidence']:.0f}% applicability confidence — below the "
                    f"{self.MIN_CONFIDENCE:.0f}% evidence threshold."
                ),
                "semantic_score": top["semantic"],
                "rejected_candidates": self._rejected_payload(rejected),
                "procurement_model": self._model_payload(model),
                "missing_specifications": model.get("missing_specifications", []),
            }

        # ------------------------------------------------------------------
        # BUILD RECOMMENDATIONS
        # ------------------------------------------------------------------
        recommendations: List[Dict[str, Any]] = []
        qualified = [a for a in analyzed
                     if a["confidence"] >= self.MIN_CONFIDENCE and not a.get("scope_mismatch")]
        for rank, a in enumerate(qualified[:3]):
            std = a["standard"]
            is_primary = rank == 0
            rec_type = "Primary Standard" if is_primary else "Related Standard"
            why_not = [self._why_not(other, top) for other in analyzed[1:4]] if is_primary else []

            # keyClauses reflect the clauses that actually map to tender requirements
            coverage_clauses = [c["evidence"] for c in a["coverage"] if c["covered"] and c["evidence"] and c["evidence"] != std.is_number]
            std_clauses = clauses_by_number.get(std.id, {})
            key_clause_objs = [
                {"clause": cl.clause_number, "title": cl.title}
                for cc in coverage_clauses
                if (cl := std_clauses.get(cc)) is not None
            ][:4]
            if not key_clause_objs:
                key_clause_objs = [
                    {"clause": ev["clause_number"], "title": ev["title"]}
                    for ev in sorted(a["clause_evidence"], key=lambda e: e["strength"], reverse=True)[:4]
                ]

            recommendations.append({
                "isNumber": std.is_number,
                "title": std.title,
                "type": rec_type,
                "confidence": round(a["confidence"], 1),
                "status": std.status or "CURRENT",
                "latestVersion": std.latest_version or std.is_number,
                "amendment": std.amendment or "None on record",
                "certification": {
                    "required": bool(std.certification_required) or (std.certification_status or "").lower() == "mandatory",
                    "scheme": std.certification_scheme or ("BIS ISI Mark" if std.certification_required else "Voluntary"),
                    "status": std.certification_status or "Voluntary",
                },
                "category": std.category or "General",
                "description": std.scope or "",
                "keyClauses": key_clause_objs,
                "relatedStandards": [
                    {"type": r["relationship_type"], "isNumber": r["is_number"],
                     "title": r["title"], "description": r["description"]}
                    for r in a["related"]
                ],
                "coverageMap": a["coverage"],
                "whyNotAlternatives": why_not,
                "evidenceTier": self._evidence_tier(a["confidence"], len(a["clause_evidence"])),
                "whyRecommended": self._why_recommended(a),
                "matchedRequirements": len([c for c in a["coverage"] if c["covered"]]),
                "totalRequirements": len(a["coverage"]),
            })

        if not recommendations:
            return self._abstain(
                "All candidate standards failed the product-scope or confidence gate.",
                detected_product=detected_product, language=language,
                gaps=["No standard matching the tender's product type cleared the evidence threshold.",
                      "Verify the product description or extend the knowledge base."],
                rejected_candidates=rejected,
                status="REJECTED_SCOPE_INCOMPATIBLE",
            )

        detected_label = self._product_label(top["standard"])
        partial = top["confidence"] < 70.0 or bool(top["conflicts"])
        return {
            "status": "FOUND_PARTIAL_MATCH" if partial else "FOUND_VERIFIED_MATCH",
            "recommendations": recommendations,
            "gaps": self._global_gaps(analyzed),
            "conflicts": self._merge_conflicts(analyzed),
            "audit_id": str(uuid.uuid4()),
            "detected_product": detected_label,
            "language": language,
            "human_verification_required": top["confidence"] < 75.0,
            "abstention_reason": None,
            "semantic_score": top["semantic"],
            "rejected_candidates": self._rejected_payload(rejected),
            "procurement_model": self._model_payload(model),
            "missing_specifications": model.get("missing_specifications", []),
        }

    # ------------------------------------------------------------------
    # Recommendation Stability Check (feature #24)
    # ------------------------------------------------------------------
    def analyze_with_stability(self, db: Optional[Session], query: str, max_variants: int = 6) -> Dict[str, Any]:
        """Run the base analysis, then re-run it under one-at-a-time perturbations
        of the tender requirements to measure ranking stability.

        Sensitivity per requirement is the max confidence drop observed across its
        variants; a requirement is 'critical' when removing it either drops the
        top recommendation by >= 15 points, flips to another standard, or causes
        the engine to abstain entirely.
        """
        base = self.analyze_requirement(db, query)
        if base.get("status") not in ("FOUND_VERIFIED_MATCH", "FOUND_PARTIAL_MATCH",
                                      "LOW_CONFIDENCE", "REQUIRES_HUMAN_VERIFICATION"):
            # No usable baseline (out-of-corpus / empty / empty KB): nothing to perturb.
            base["stability"] = self._empty_stability()
            return base

        baseline_top = (base["recommendations"][0]["isNumber"]
                        if base.get("recommendations") else None)
        baseline_conf = (float(base["recommendations"][0]["confidence"])
                         if base.get("recommendations") else float(base.get("semantic_score") or 0.0) * 100.0)

        variants = build_perturbations(query)[:max_variants]
        results: List[Dict[str, Any]] = []
        for var in variants:
            vres = self.analyze_requirement(db, var["text"])
            v_top = (vres["recommendations"][0]["isNumber"]
                     if vres.get("recommendations") else None)
            v_conf = (float(vres["recommendations"][0]["confidence"])
                      if vres.get("recommendations") else 0.0)
            delta = round(v_conf - baseline_conf, 1)
            abstained = vres.get("status") in ("NOT_FOUND_IN_DATASET", "LOW_CONFIDENCE")
            flipped = bool(baseline_top) and (v_top != baseline_top)
            critical = (delta <= -15.0) or (flipped and var["kind"] == "remove") or (abstained and var["kind"] == "remove")
            results.append({
                "kind": var["kind"],
                "requirement": var["label"],
                "fragment": var["fragment"],
                "perturbedQuery": var["text"][:200],
                "topStandard": v_top,
                "topConfidence": v_conf,
                "confidenceDelta": delta,
                "flipped": flipped,
                "abstained": abstained,
                "sensitivity": max(0.0, -delta) if var["kind"] == "remove" else 0.0,
                "critical": critical,
                "verdict": (
                    "Recommendation collapses without this requirement."
                    if critical and var["kind"] == "remove" else
                    "Ranking locks in further when this requirement is emphasized."
                    if var["kind"] == "emphasize" and delta > 3.0 and not flipped else
                    "Emphasizing this requirement shifts the recommendation."
                    if var["kind"] == "emphasize" and flipped else
                    "Ranking unchanged under this perturbation."
                    if not flipped and abs(delta) < 5.0 else
                    "Ranking shifts moderately under this perturbation."
                ),
            })

        # Aggregate per requirement: worst-case remove drop decides criticality
        by_req: Dict[str, Dict[str, Any]] = {}
        for r in results:
            entry = by_req.setdefault(r["requirement"], {
                "requirement": r["requirement"],
                "fragment": r["fragment"],
                "maxDrop": 0.0,
                "flippedOnRemove": False,
                "abstainedOnRemove": False,
                "emphasizeGain": 0.0,
                "critical": False,
            })
            if r["kind"] == "remove":
                entry["maxDrop"] = max(entry["maxDrop"], r["sensitivity"])
                entry["flippedOnRemove"] = entry["flippedOnRemove"] or r["flipped"]
                entry["abstainedOnRemove"] = entry["abstainedOnRemove"] or r["abstained"]
            else:
                entry["emphasizeGain"] = max(entry["emphasizeGain"], r["confidenceDelta"])
            entry["critical"] = bool(
                entry["maxDrop"] >= 15.0 or entry["flippedOnRemove"] or entry["abstainedOnRemove"]
            )

        summary = sorted(by_req.values(), key=lambda e: e["maxDrop"], reverse=True)
        if any(e["critical"] for e in summary):
            overall = "FRAGILE"
        elif summary and max(e["maxDrop"] for e in summary) >= 8.0:
            overall = "MODERATE"
        else:
            overall = "STABLE"

        base["stability"] = {
            "baselineTop": baseline_top,
            "baselineConfidence": baseline_conf,
            "overall": overall,
            "checkedRequirements": len(summary),
            "summary": summary,
            "variants": results,
            "note": (
                "Requirement removal/emphasis re-runs the full evidence pipeline. "
                "A fragile rating means the recommendation is highly sensitive to "
                "the listed specification — human review should confirm it."
            ),
        }
        return base

    @staticmethod
    def _empty_stability() -> Dict[str, Any]:
        return {
            "baselineTop": None,
            "baselineConfidence": 0.0,
            "overall": "NOT_APPLICABLE",
            "checkedRequirements": 0,
            "summary": [],
            "variants": [],
            "note": "Stability check requires a baseline recommendation; none was produced for this tender.",
        }

    # ------------------------------------------------------------------
    # Coverage / conflict analysis
    # ------------------------------------------------------------------
    def _analyze_coverage(
        self,
        raw_query: str,
        norm_query: str,
        numeric_reqs: List[Dict[str, str]],
        cand: Dict[str, Any],
    ) -> Tuple[List[Dict[str, Any]], List[str], List[Dict[str, Any]]]:
        std = cand["standard"]
        clauses = cand["clauses"]
        coverage: List[Dict[str, Any]] = []

        # 1. Scope coverage entry (product identity matched to standard scope)
        coverage.append({
            "requirement": "Product scope & applicability",
            "evidence": std.is_number,
            "detail": f"Standard scope: {(std.scope or '')[:200]}",
            "covered": True,
        })

        # 2. Requirement-side coverage (SIH feature #16): each structured tender
        #    requirement is mapped to the clause evidence supporting it.
        tender_requirements = nlp_service.extract_requirements(raw_query)
        query_token_set = set(_content_tokens(raw_query))

        for req in tender_requirements:
            req_field = req.get("field", "")
            req_value = req.get("value", "")
            if req_field in {"Procurement Quantity", "Referenced Standard", "Product Domain", "Product Category"}:
                continue  # administrative / already covered by the scope row

            matched_clause = None
            numeric_match = None

            # (a) Numeric evidence: clause limit carries the tender's value
            for clause in clauses:
                nm = self._numeric_evidence(numeric_reqs, clause.test_limit, clause.requirement_text)
                if nm:
                    matched_clause = clause
                    numeric_match = nm
                    break

            # (b) Aspect vocabulary: clause whose wording addresses the requirement aspect
            if not matched_clause:
                aspect_vocab = ASPECT_TOKENS.get(req_field, set())
                for clause in clauses:
                    clause_text = f"{clause.title} {clause.requirement_text or ''} {clause.tested_parameter or ''}"
                    clause_tokens = set(_content_tokens(clause_text))
                    if aspect_vocab and aspect_vocab & clause_tokens:
                        matched_clause = clause
                        break

            # (c) Fallback: direct token overlap between tender value and clause text
            if not matched_clause:
                req_tokens = set(_content_tokens(req_value))
                for clause in clauses:
                    clause_text = f"{clause.title} {clause.requirement_text or ''}"
                    if req_tokens & set(_content_tokens(clause_text)):
                        matched_clause = clause
                        break

            if matched_clause is not None:
                detail = matched_clause.requirement_text or matched_clause.title
                if numeric_match:
                    detail = f"{detail} (Matches tender spec: {numeric_match['display']})"
                coverage.append({
                    "requirement": f"{req_field}: {req_value}",
                    "evidence": matched_clause.clause_number,
                    "detail": detail[:250],
                    "covered": True,
                })
            else:
                coverage.append({
                    "requirement": f"{req_field}: {req_value}",
                    "evidence": None,
                    "detail": "No verified clause evidence in this standard addresses this requirement.",
                    "covered": False,
                })

        # 3. Conflict detection — tender value vs clause rating ceiling
        conflicts: List[Dict[str, Any]] = []
        seen_conflicts = set()
        for num in numeric_reqs:
            tender_val = self._conflict_tender_value(numeric_reqs, num["type"])
            if tender_val is None:
                continue
            for clause in clauses:
                parsed = _parse_limit_number(clause.test_limit or clause.requirement_text)
                if not parsed:
                    continue
                kind, limit_val = parsed
                if num["type"] == kind and tender_val > limit_val:
                    key = (num["type"], clause.clause_number)
                    if key in seen_conflicts:
                        continue
                    seen_conflicts.add(key)
                    conflicts.append({
                        "tenderSpec": f"Tender requirement: {num['display']}",
                        "standardSpec": f"{std.is_number} {clause.clause_number} limit: {clause.test_limit or f'{limit_val:g}'}",
                        "severity": "Warning - Human review recommended",
                        "impact": (
                            f"Tender requires {num['display']} but the verified clause evidence for "
                            f"{clause.clause_number} is rated to {clause.test_limit or limit_val}. "
                            "Potential technical inconsistency; human verification recommended."
                        ),
                    })
                    break  # one conflict per requirement is enough

        uncovered = [c["requirement"] for c in coverage if not c["covered"]]
        return coverage, uncovered, conflicts

    def _conflict_tender_value(self, numeric_reqs: List[Dict[str, str]], kind: str) -> Optional[float]:
        """Extract the tender's numeric value for a given kind (temperature/voltage/pressure)."""
        for num in numeric_reqs:
            if num["type"] == "temperature" and kind == "temperature":
                try:
                    return float(num["values"].split(",")[0])
                except (KeyError, ValueError, IndexError):
                    return None
            if num["type"] == kind:
                try:
                    return float(num["value"])
                except (KeyError, ValueError):
                    return None
        return None

    def _numeric_evidence(
        self,
        numeric_reqs: List[Dict[str, str]],
        limit_text: Optional[str],
        req_text: Optional[str] = None,
    ) -> Optional[Dict[str, str]]:
        """Return the tender numeric requirement satisfied by this clause limit, if any."""
        if not numeric_reqs or not limit_text:
            return None
        norm_limit = normalize_text(limit_text)
        norm_req = normalize_text(req_text or "")
        for num in numeric_reqs:
            if num["type"] in {"temperature", "temperature_range"}:
                vals = [float(v) for v in num.get("values", "").split(",") if v] if num["type"] == "temperature" else \
                       [float(num["min"]), float(num["max"])]
                for v in vals:
                    if f"{v:g}" in norm_limit or f"{v:g}" in norm_req:
                        return num
            elif num["type"] == "voltage":
                v = float(num["value"])
                if num["unit"] == "kv" and f"{v:g} kv" in norm_limit:
                    return num
                if num["unit"] == "v" and f"{int(v)} v" in norm_limit:
                    return num
            elif num["type"] == "pressure":
                v = float(num["value"])
                if f"{v:g} {num['unit']}" in norm_limit:
                    return num
        return None

    # ------------------------------------------------------------------
    # Relationship graph traversal (allied standards discovery)
    # ------------------------------------------------------------------
    def _related_standards(self, db: Optional[Session], std: Standard, max_hops: int = 1) -> List[Dict[str, Any]]:
        """Traverse outgoing relationships (normative/test_method/safety/material/etc)."""
        if db is None:
            return []
        from app.models.standard import StandardRelationship
        out: List[Dict[str, Any]] = []
        visited_ids = {std.id}

        def visit(current: Standard, depth: int) -> None:
            if depth > max_hops:
                return
            rels = db.query(StandardRelationship).filter(
                StandardRelationship.from_standard_id == current.id).all()
            for rel in rels:
                target = db.query(Standard).filter(Standard.id == rel.to_standard_id).first()
                if not target or target.id in visited_ids:
                    continue
                visited_ids.add(target.id)
                out.append({
                    "relationship_type": rel.relationship_type or "Related",
                    "is_number": target.is_number,
                    "title": target.title,
                    "description": rel.description or "",
                    "status": target.status or "CURRENT",
                })
                visit(target, depth + 1)

        visit(std, 0)
        return out

    # ------------------------------------------------------------------
    # Confidence calibration (measurable signals, not LLM-generated)
    # ------------------------------------------------------------------
    def _validity_factor(self, std: Standard) -> float:
        status = (std.status or "CURRENT").upper()
        if status == "SUPERSEDED":
            return 0.0
        if status == "WITHDRAWN":
            return 0.1
        if status == "REAFFIRMED":
            return 1.0
        return 0.95

    def _calibrate_confidence(
        self,
        semantic: float,
        keyword: float,
        coverage: List[Dict[str, Any]],
        validity: float,
        graph: float,
        explicit: bool = False,
    ) -> float:
        covered = sum(1 for c in coverage if c["covered"])
        total = max(len(coverage), 1)
        coverage_ratio = covered / total

        raw = (
            self.W_SEMANTIC * min(semantic * 1.35, 1.0)
            + self.W_KEYWORD * keyword
            + self.W_COVERAGE * coverage_ratio
            + self.W_VALIDITY * validity
            + self.W_GRAPH * graph
        )
        if explicit:
            raw = max(raw, 0.80)  # tender cites the IS number itself -> strong signal
        return round(min(raw * 100, 96.0), 1)

    def _evidence_tier(self, confidence: float, n_evidence: int) -> str:
        if confidence >= 80 and n_evidence >= 2:
            return "HIGH EVIDENCE"
        if confidence >= 60:
            return "MEDIUM EVIDENCE"
        return "LOW EVIDENCE"

    # ------------------------------------------------------------------
    # Explanation builders
    # ------------------------------------------------------------------
    def _why_recommended(self, a: Dict[str, Any]) -> str:
        std = a["standard"]
        matched = [c for c in a["coverage"] if c["covered"]]
        ev = a["clause_evidence"]
        parts = [
            f"Hybrid retrieval ranked {std.is_number} highest (semantic {a['semantic']:.2f}, "
            f"keyword {a['keyword']:.2f}).",
            f"{len(matched)} of {len(a['coverage'])} specification items have clause-level evidence.",
        ]
        if ev:
            best = max(ev, key=lambda e: e["strength"])
            parts.append(
                f"Strongest evidence: {best['clause_number']} ({best['title']}) — {best['requirement_text'][:120]}"
            )
        if a["explicit_hit"]:
            parts.append("Tender explicitly cites this standard.")
        return " ".join(parts)

    def _why_not(self, a: Dict[str, Any], top: Dict[str, Any]) -> Dict[str, Any]:
        std = a["standard"]
        reasons: List[str] = []
        gap = top["confidence"] - a["confidence"]
        if a.get("scope_mismatch"):
            reasons.append("Different product scope: the standard's title and scope do not cover the tender's product type.")
        if a["semantic"] < top["semantic"] - 0.10:
            reasons.append("Weaker semantic alignment with the tender's product description.")
        if not a["clause_evidence"] and top["clause_evidence"]:
            reasons.append("No clause-level evidence supports the specific tender requirements.")
        covered_a = sum(1 for c in a["coverage"] if c["covered"])
        covered_top = sum(1 for c in top["coverage"] if c["covered"])
        if covered_a < covered_top:
            reasons.append(
                f"Covers {covered_a} of {len(a['coverage'])} specification items vs "
                f"{covered_top} for the recommended standard."
            )
        if a["validity"] < 0.5:
            reasons.append("Standard is superseded or withdrawn — a newer version exists.")
        if not reasons:
            reasons.append(f"Ranked {gap:.0f} points below the recommended standard on combined evidence signals.")
        return {
            "isNumber": std.is_number,
            "title": std.title,
            "confidence": round(a["confidence"], 1),
            "reason": " ".join(reasons),
        }

    def _product_label(self, std: Standard) -> str:
        t = (std.title or "").strip()
        return t if t else std.is_number

    def _global_gaps(self, analyzed: List[Dict[str, Any]]) -> List[str]:
        """Requirements the top recommendation fails to cover (gap detection)."""
        top = analyzed[0]
        gaps: List[str] = []
        seen = set()
        for c in top["uncovered"]:
            if c in seen:
                continue
            seen.add(c)
            gaps.append(f"Not covered by {top['standard'].is_number}: {c}")
        return gaps

    def _abstention_gaps(self, analyzed: List[Dict[str, Any]]) -> List[str]:
        gaps = [
            "Insufficient verified evidence to confidently recommend a standard.",
            "Provide the intended application, material, operating temperature, or testing requirement.",
        ]
        if analyzed:
            best = analyzed[0]
            gaps.append(
                f"Closest candidate was {best['standard'].is_number} "
                f"({best['confidence']:.0f}%) but it did not meet the evidence threshold."
            )
        return gaps

    def _merge_conflicts(self, analyzed: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        merged: List[Dict[str, Any]] = []
        for a in analyzed[:3]:
            for c in a["conflicts"]:
                key = (c["tenderSpec"], c["standardSpec"])
                if key not in seen:
                    seen.add(key)
                    merged.append(c)
        return merged

    def _model_payload(self, model: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Structured procurement model surfaced for transparency/provenance."""
        if not model:
            return None
        return {
            "product": model.get("product") or "",
            "productSubtype": model.get("product_subtype") or [],
            "materials": model.get("materials") or [],
            "productForms": model.get("product_forms") or [],
            "applications": model.get("applications") or [],
            "quantity": model.get("quantity"),
            "unit": model.get("unit"),
            "parameters": model.get("parameters") or [],
            "isReferences": model.get("is_references") or [],
            "language": model.get("language") or "en",
        }

    def _rejected_payload(self, rejected: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Why-not records for candidates rejected by the compatibility gates."""
        out: List[Dict[str, Any]] = []
        for r in rejected[:6]:
            out.append({
                "isNumber": r["standard"].is_number,
                "title": r["standard"].title,
                "similarityScore": r["confidence"],
                "status": r["verdict"]["status"],
                "reasons": r["verdict"]["reasons"],
                "failedChecks": r["verdict"]["failed_checks"],
            })
        return out

    def _abstain(
        self,
        reason: str,
        detected_product: str = "Unspecified",
        language: str = "en",
        gaps: Optional[List[str]] = None,
        rejected_candidates: Optional[List[Dict[str, Any]]] = None,
        status: str = "NOT_FOUND_IN_DATASET",
    ) -> Dict[str, Any]:
        return {
            "status": status,
            "recommendations": [],
            "gaps": gaps or ["No verified applicable standard was found in the current knowledge base."],
            "conflicts": [],
            "audit_id": str(uuid.uuid4()),
            "detected_product": detected_product,
            "language": language,
            "human_verification_required": True,
            "abstention_reason": reason,
            "rejected_candidates": [
                {
                    "isNumber": r["standard"].is_number,
                    "title": r["standard"].title,
                    "similarityScore": r["confidence"],
                    "status": r["verdict"]["status"],
                    "reasons": r["verdict"]["reasons"],
                    "failedChecks": r["verdict"]["failed_checks"],
                }
                for r in (rejected_candidates or [])
            ][:6],
            "procurement_model": None,
            "missing_specifications": [],
        }


evidence_service = EvidenceService()
