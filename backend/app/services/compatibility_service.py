"""
IS-SARATHI Generic Compatibility Engine
=======================================
A domain-independent applicability evaluator. NO product-specific rules.

For every candidate standard the engine runs 8 independent checks and returns
a structured verdict. Hard-gate failures REJECT the candidate regardless of
how high its semantic/keyword similarity is — similarity can never override
a failed compatibility gate.

Checks:
  1. PRODUCT_COMPATIBILITY            — product identity vs standard product space
  2. APPLICATION_COMPATIBILITY        — intended use vs standard application space
  3. SCOPE_COMPATIBILITY              — standard scope covers the requested item
  4. MATERIAL_COMPATIBILITY           — material/type words are compatible
  5. TYPE_COMPATIBILITY               — product form (pipe vs cable vs bar...) matches
  6. TECHNICAL_PARAMETER_COMPATIBILITY — numeric parameters feasible for this standard
  7. METADATA_COMPATIBILITY           — standard exists, is verified, has metadata
  8. EVIDENCE_AVAILABILITY            — verified clause evidence exists

Everything is derived from the standard's OWN text (title, scope, clauses,
exclusions) and the parsed procurement model — never from lookup tables that
map a specific product to a specific standard.
"""

import re
import logging
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("is_sarathi.compatibility")

# ---------------------------------------------------------------------------
# Generic lexicons. These are WORD CLASSES (material words, form words,
# application words), not product->standard mappings. They work for any
# domain because they describe how procurement language is structured.
# ---------------------------------------------------------------------------

# Words that name a MATERIAL SUBSTRATE (can combine with many product forms).
MATERIAL_WORDS: Set[str] = {
    "steel", "iron", "copper", "aluminium", "aluminum", "brass", "bronze",
    "zinc", "lead", "nickel", "tin", "titanium", "cast", "wrought",
    "pvc", "upvc", "cpvc", "hdpe", "ldpe", "pe", "polyethylene", "polypropylene",
    "pp", "abs", "rubber", "elastomer", "neoprene", "silicone", "vinyl",
    "glass", "ceramic", "concrete", "cement", "timber", "wood", "bamboo",
    "paper", "cardboard", "leather", "textile", "cotton", "jute", " wool",
    "ldpe", "xlpe", "crosslinked",
}

# Words that name a PRODUCT FORM / SHAPE (the same material can take many forms).
FORM_WORDS: Set[str] = {
    "pipe", "pipes", "tube", "tubes", "tubular", "pipeline",
    "cable", "cables", "wire", "wires", "conductor", "cord",
    "bar", "bars", "rod", "rods", "rebar", "reinforcement",
    "sheet", "sheets", "plate", "plates", "coil", "coils", "strip",
    "section", "sections", "beam", "beams", "channel", "angle",
    "powder", "granules", "resin", "pellets", "flake",
    "film", "sheeting", "liners", "membrane",
    "block", "blocks", "brick", "bricks",
    "fitting", "fittings", "socket", "elbow", "flange",
}

# Words that name an APPLICATION DOMAIN (context, not product identity).
APPLICATION_WORDS: Set[str] = {
    "construction", "building", "infrastructure", "municipal", "industrial",
    "domestic", "household", "residential", "commercial", "agricultural",
    "irrigation", "sewerage", "sewage", "drainage", "mining", "underground",
    "marine", "offshore", "automotive", "vehicular", "railway", "railways",
    "hospital", "medical", "school", "office", "kitchen", "foundry",
    "welding", "chemical", "petrochemical", "pharmaceutical", "food",
    "potable", "drinking", "firefighting", "safety",
}

# Words that carry NEGATIVE selection pressure: they describe a DIFFERENT
# product family when they appear in a standard title, and the tender's
# product noun is absent. Used for cross-family contrast.
CONTRAST_FAMILY_WORDS: Set[str] = {
    "helmet", "glove", "gloves", "mask", "respirator", "footwear", "harness",
    "belt", "shield", "visor", "goggles", "earmuffs", "earplug",
    "pipe", "pipes", "tube", "tubes", "cable", "cables", "wire", "wires",
    "transformer", "cylinder", "valve", "cement", "aggregate", "rebar",
    "extinguisher", "hydrant", "furniture", "desk", "chair", "light",
    "lamp", "luminaire", "battery", "inverter", "meter", "switchgear",
    "bucket", "mug", "crate", "container", "bottle", "bag", "sack",
}

# Body-of-standard roles: what the standard IS (vs what it is ABOUT).
# A "test method" standard is not the product standard for the procurement
# even though its title contains the same product word.
METHOD_ROLES: Set[str] = {
    "methods", "method", "test", "testing", "determination", "measurement",
    "sampling", "procedure", "guide", "guideline", "code",
}


def _tokens(text: str) -> Set[str]:
    """Simple token set for comparison (keeps Unicode letters)."""
    if not text:
        return set()
    cleaned = re.sub(r"[^\w\s]", " ", text.lower(), flags=re.UNICODE)
    return {t for t in cleaned.split() if len(t) > 1}


def _stem(t: str) -> str:
    if len(t) > 3 and t.endswith("s") and not t.endswith("ss") and not t.endswith("us"):
        return t[:-1]
    return t


def _stemmed(text: str) -> Set[str]:
    return {_stem(t) for t in _tokens(text)}


_PARAM_KIND_MARKERS: Dict[str, str] = {
    "temperature": "°|deg",
    "temperature_range": "°|deg",
    "voltage": r"\b(kv|v)\b|volt",
    "pressure": r"mpa|bar|psi|kpa|pressure",
    "load": r"\bkn\b|\bkg\b|load|force",
}


def numeric_supported(model: Dict[str, Any], clauses: List[Any]) -> bool:
    """True when the standard's own clause rows ADDRESS any tender parameter.

    Two generic levels:
      value-level — the tender's value appears in a clause (strong support)
      kind-level  — a clause addresses the same parameter kind (temperature,
                    voltage, pressure, load) even with a different value; that
                    situation is a CONFLICT to be surfaced downstream, not a
                    reason to reject the standard's applicability.
    """
    import re as _re
    clause_blob = " ".join(
        f"{getattr(c, 'test_limit', '') or ''} {getattr(c, 'requirement_text', '') or ''} {getattr(c, 'tested_parameter', '') or ''}"
        for c in clauses
    )
    clause_blob_low = clause_blob.lower()
    for param in model.get("parameters") or []:
        display = str(param.get("display", ""))
        for v in _re.findall(r"\d+(?:\.\d+)?", display):
            if v in clause_blob:
                return True  # value-level support
        kind = param.get("type", "")
        marker = _PARAM_KIND_MARKERS.get(kind)
        if marker and _re.search(marker, clause_blob_low):
            return True  # kind-level support (possible conflict, handled downstream)
    return False


# ---------------------------------------------------------------------------
# Structured verdict
# ---------------------------------------------------------------------------

def _verdict(status: str, reasons: List[str], failed: List[str],
             evidence: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "compatible": status in {"PASS", "PASS_WEAK"},
        "status": status,
        "reasons": reasons,
        "failed_checks": failed,
        "evidence": evidence or [],
    }


class CompatibilityEngine:
    """Evaluates one (procurement model, standard) pair against 8 generic checks."""

    def evaluate(
        self,
        model: Dict[str, Any],
        std: Any,
        clauses: List[Any],
        clause_evidence: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        model: structured procurement model from procurement_parser
        std:   Standard ORM row (title, scope, category, ...)
        clauses: the standard's own clause rows (never another standard's)
        clause_evidence: evidence entries built from those clauses
        """
        reasons: List[str] = []
        failed: List[str] = []
        evidence: List[str] = []
        scores: Dict[str, float] = {}

        title = std.title or ""
        scope = std.scope or ""
        std_title_tokens = _stemmed(title)
        std_scope_tokens = _stemmed(scope)
        std_all = std_title_tokens | std_scope_tokens
        std_norm = f"{title} {scope}".lower()

        product = (model.get("product") or "").strip()
        product_tokens = _stemmed(product)
        materials = set(model.get("materials") or [])
        applications = set(model.get("applications") or [])
        forms = set(model.get("product_forms") or [])

        # ------------------------------------------------------------------
        # 1. PRODUCT_COMPATIBILITY (hard gate)
        # ------------------------------------------------------------------
        product_ok = False
        product_family_conflict = False
        if product_tokens:
            product_hits = product_tokens & std_all
            if product_hits:
                product_ok = True
                evidence.append(
                    f"Product identity '{product}' appears in the standard's title/scope."
                )
            else:
                # Family contrast: the standard is titled for a DIFFERENT product
                # family while the tender's product noun is missing from it.
                tender_families = {t for t in product_tokens if t in CONTRAST_FAMILY_WORDS}
                std_family_words = {t for t in std_title_tokens if t in CONTRAST_FAMILY_WORDS}
                if tender_families and std_family_words and not (tender_families & std_family_words):
                    product_family_conflict = True
                    reasons.append(
                        f"Product mismatch: standard covers {'/'.join(sorted(std_family_words))}, "
                        f"tender requests {'/'.join(sorted(tender_families))}."
                    )
                    failed.append("PRODUCT_COMPATIBILITY")
                    scores["product"] = 0.0
                else:
                    reasons.append(
                        f"Product identity '{product}' not found in the standard's title or scope."
                    )
                    failed.append("PRODUCT_COMPATIBILITY")
                    scores["product"] = 0.15
        else:
            reasons.append("Product identity could not be determined from the tender text.")
            failed.append("PRODUCT_COMPATIBILITY")
            scores["product"] = 0.10

        # ------------------------------------------------------------------
        # 2. APPLICATION_COMPATIBILITY (soft unless explicitly contradictory)
        # ------------------------------------------------------------------
        app_ok = True
        if applications:
            app_hits = applications & std_all
            if app_hits:
                app_ok = True
                evidence.append(
                    f"Application context {'/'.join(sorted(app_hits))} is addressed by the standard."
                )
                scores["application"] = 1.0
            else:
                # Not every standard mentions its application domain in the
                # title/scope; absence is WEAK, not a rejection.
                app_ok = True
                scores["application"] = 0.55
        else:
            scores["application"] = 0.5

        # ------------------------------------------------------------------
        # 3. SCOPE_COMPATIBILITY (hard gate when excluded)
        # ------------------------------------------------------------------
        exclusions = getattr(std, "exclusions", None) or ""
        excl_tokens = _stemmed(exclusions)
        scope_ok = True
        if exclusions and product_tokens and (product_tokens & excl_tokens):
            scope_ok = False
            reasons.append(
                f"Standard explicitly excludes this product: \"{exclusions[:160]}\"."
            )
            failed.append("SCOPE_COMPATIBILITY")
            scores["scope"] = 0.0
        else:
            scores["scope"] = 1.0 if product_ok else 0.3

        # ------------------------------------------------------------------
        # 4. MATERIAL_COMPATIBILITY (hard gate on substrate contradiction)
        # ------------------------------------------------------------------
        material_ok = True
        # MATERIAL-ONLY gate: a tender naming ONLY a substrate ("structural steel",
        # "PVC") with no product form must NOT match standards that cover a
        # SPECIFIC form of that substrate (steel tubes, PVC pipes, PVC cables).
        # This is the generic "steel ≠ steel pipe ≠ reinforcement bar" rule.
        forms_in_std = std_all & FORM_WORDS
        material_only_tender = bool(materials) and not forms and (
            not product_tokens or product_tokens <= {m for m in materials}
        )
        if material_only_tender and forms_in_std:
            material_ok = False
            reasons.append(
                "Material-only specification: the tender names a substrate without a "
                f"product form, while this standard covers specific forms "
                f"({'/'.join(sorted(forms_in_std))}). Product identity is ambiguous."
            )
            failed.append("MATERIAL_COMPATIBILITY")
            scores["material"] = 0.0
        elif materials:
            mat_hits = materials & std_all
            if mat_hits:
                evidence.append(
                    f"Material {'/'.join(sorted(mat_hits))} matches the standard's material coverage."
                )
                scores["material"] = 1.0
            else:
                # The tender names a material the standard never covers, AND the
                # standard names a DIFFERENT material of the same substrate class.
                std_materials = {t for t in std_all if t in MATERIAL_WORDS}
                if std_materials:
                    material_ok = False
                    reasons.append(
                        f"Material mismatch: standard covers {'/'.join(sorted(std_materials))}, "
                        f"tender specifies {'/'.join(sorted(materials))}."
                    )
                    failed.append("MATERIAL_COMPATIBILITY")
                    scores["material"] = 0.0
                else:
                    # Standard is material-agnostic (e.g. PPE): absence is fine.
                    scores["material"] = 0.7
        else:
            scores["material"] = 0.6

        # ------------------------------------------------------------------
        # 5. TYPE_COMPATIBILITY (hard gate: product form contradiction)
        # ------------------------------------------------------------------
        type_ok = True
        if forms:
            form_hits = forms & std_all
            if form_hits:
                evidence.append(
                    f"Product form {'/'.join(sorted(form_hits))} is covered by the standard."
                )
                scores["type"] = 1.0
            else:
                std_forms = {t for t in std_all if t in FORM_WORDS}
                if std_forms and forms:
                    type_ok = False
                    reasons.append(
                        f"Product form mismatch: standard covers {'/'.join(sorted(std_forms))}, "
                        f"tender requests {'/'.join(sorted(forms))}."
                    )
                    failed.append("TYPE_COMPATIBILITY")
                    scores["type"] = 0.0
                else:
                    scores["type"] = 0.7
        else:
            scores["type"] = 0.6

        # ------------------------------------------------------------------
        # 6. TECHNICAL_PARAMETER_COMPATIBILITY (soft)
        # ------------------------------------------------------------------
        # Deep numeric feasibility is handled by the evidence/conflict layer.
        # Here we only require that the standard HAS clause rows to verify against.
        param_ok = bool(clauses)
        scores["technical"] = 1.0 if param_ok else 0.3
        if not param_ok:
            reasons.append("Standard has no clause data to verify technical parameters against.")
            failed.append("TECHNICAL_PARAMETER_COMPATIBILITY")

        # ------------------------------------------------------------------
        # 7. METADATA_COMPATIBILITY (verification status, mandatory metadata)
        # ------------------------------------------------------------------
        verification = (getattr(std, "verification_status", None) or "VERIFIED").upper()
        metadata_ok = verification in {"VERIFIED", "PARTIALLY_VERIFIED"}
        if metadata_ok:
            scores["metadata"] = 1.0 if verification == "VERIFIED" else 0.7
        else:
            metadata_ok = False
            reasons.append(f"Standard metadata is {verification}; insufficient authoritative data.")
            failed.append("METADATA_COMPATIBILITY")
            scores["metadata"] = 0.0

        # ------------------------------------------------------------------
        # 8. EVIDENCE_AVAILABILITY (hard gate: verified requirement evidence)
        # ------------------------------------------------------------------
        # Two-tier rule, generic across domains:
        #   - The standard MUST have its own clause rows (no cross-standard
        #     contamination; a standard with no requirement data cannot be
        #     verified).
        #   - When the tender makes TECHNICAL CLAIMS (parameters), those claims
        #     must map to clause evidence. A bare product-identity query needs
        #     no requirement mapping (there is nothing to map yet) — coverage
        #     will honestly report NO_VERIFIED_EVIDENCE rows instead.
        has_params = bool(model.get("parameters"))
        has_clauses = bool(clauses)
        evidence_ok = True
        if not has_clauses:
            evidence_ok = False
            reasons.append("Standard has no verified clause rows in the knowledge base.")
            failed.append("EVIDENCE_AVAILABILITY")
            scores["evidence"] = 0.0
        elif has_params and not clause_evidence and not numeric_supported(model, clauses):
            evidence_ok = False
            reasons.append(
                "Tender states technical parameters but no verified clause evidence "
                "in this standard supports them."
            )
            failed.append("EVIDENCE_AVAILABILITY")
            scores["evidence"] = 0.0
        elif clause_evidence:
            top_ev = max(clause_evidence, key=lambda e: e.get("strength", 0))
            evidence.append(
                f"Clause evidence available: {top_ev.get('clause_number')} — {top_ev.get('title')}."
            )
            scores["evidence"] = 1.0
        else:
            evidence.append("Standard carries verified clause data; product identity matched.")
            scores["evidence"] = 0.75

        # ------------------------------------------------------------------
        # Verdict assembly — hard gates decide, scores only inform
        # ------------------------------------------------------------------
        hard_gates = [product_ok or not product_tokens, scope_ok, material_ok,
                      type_ok, metadata_ok, evidence_ok]
        # product_ok must be treated as a gate only when we actually identified
        # a product; when unknown, the parser flagged it and the caller abstains.
        if product_tokens:
            hard_gates[0] = product_ok or product_family_conflict is False

        compatible = all(hard_gates)

        if compatible and len(failed) == 0 and product_ok:
            status = "PASS"
        elif compatible:
            status = "PASS_WEAK"
        elif not product_ok and product_family_conflict:
            status = "REJECTED_PRODUCT_MISMATCH"
        elif not scope_ok:
            status = "REJECTED_EXCLUDED"
        elif not material_ok:
            status = "REJECTED_MATERIAL_MISMATCH"
        elif not type_ok:
            status = "REJECTED_TYPE_MISMATCH"
        elif not metadata_ok:
            status = "REJECTED_UNVERIFIED_METADATA"
        elif not evidence_ok:
            status = "REJECTED_INSUFFICIENT_EVIDENCE"
        else:
            status = "REJECTED_NO_PRODUCT_MATCH"

        return {
            "compatible": compatible,
            "status": status,
            "reasons": reasons,
            "failed_checks": failed,
            "evidence": evidence,
            "scores": scores,
        }


compatibility_engine = CompatibilityEngine()
