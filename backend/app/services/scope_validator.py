"""
IS-SARATHI Scope Compatibility and Domain Validation Engine
Enforces strict domain gating, scope compatibility checks, and why-not disqualifications.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger("is_sarathi.scope_validator")

# Domain classification rules with strict keywords
DOMAIN_DEFINITIONS = {
    "Electrical & Electronics": {
        "keywords": [
            r"\bcables?\b", r"\bwiring\b", r"\bconductor\b", r"\bcopper\s+wire\b",
            r"\btransformer\b", r"\btransformers?\b", r"\bmcb\b", r"\bcircuit\s+breaker\b",
            r"\bearthing\b", r"\belectrical\b", r"\bvoltage\b", r"\bfrls\b", r"\bxlpe\b",
            r"\bpower\s+distribution\b", r"\bdielectric\b", r"\binsulated\s+cable\b",
            r"\blszh\b", r"\blow[\s-]+smoke\b", r"\bzero[\s-]+halogen\b"
        ],
        "incompatible_categories": [
            "Pipes & Plumbing", "Civil & Construction Materials", "Mechanical & Tooling",
            "Chemical & Plastics", "Personal Protective Equipment", "Furniture & Fixtures",
            "Firefighting & Safety Equipment"
        ],
        "incompatible_scopes": [
            "pipe", "plumbing", "water supply", "sewerage", "tube", "cement", "concrete",
            "cylinder", "packaged water", "helmet", "footwear", "desk", "chair", "furniture",
            "fire extinguisher"
        ]
    },
    "Civil & Construction Materials": {
        "keywords": [
            r"\bcement\b", r"\bportland\b", r"\bopc\b", r"\bppc\b", r"\bconcrete\b",
            r"\brebars?\b", r"\btmt\b", r"\bsteel\s+bars?\b", r"\baggregates?\b",
            r"\bmortar\b", r"\broad\s+construction\b", r"\bpavement\b", r"\bstructural\s+concrete\b"
        ],
        "incompatible_categories": [
            "Electrical & Electronics", "Pipes & Plumbing", "Personal Protective Equipment",
            "Mechanical & Tooling", "Chemical & Plastics", "Furniture & Fixtures",
            "Firefighting & Safety Equipment"
        ],
        "incompatible_scopes": [
            "cable", "wiring", "pipe", "tubular", "glove", "helmet", "face shield", "cylinder",
            "desk", "chair", "furniture", "fire extinguisher"
        ]
    },
    "Pipes & Plumbing": {
        "keywords": [
            r"\bpipes?\b", r"\bplumbing\b", r"\bupvc\b", r"\bcpvc\b", r"\bhdpe\s+pipe\b",
            r"\bpotable\s+water\b", r"\bwater\s+distribution\b", r"\bsewerage\b",
            r"\bsteel\s+tubes?\b", r"\btubulars?\b", r"\bfittings\b", r"\bconduit\b"
        ],
        "incompatible_categories": [
            "Personal Protective Equipment", "Electrical & Electronics",
            "Civil & Construction Materials", "Furniture & Fixtures",
            "Mechanical & Tooling", "Chemical & Plastics",
            "Firefighting & Safety Equipment"
        ],
        "incompatible_scopes": [
            "helmet", "gloves", "cement", "respiratory", "transformer", "cable",
            "desk", "chair", "furniture", "fire extinguisher"
        ]
    },
    "Personal Protective Equipment": {
        "keywords": [
            r"\bhelmets?\b", r"\bheadgear\b", r"\bmasks?\b", r"\brespirators?\b",
            r"\bgloves?\b", r"\bfootwear\b", r"\bsafety\s+shoes?\b", r"\bharnesses?\b",
            r"\bface\s+shields?\b", r"\bppe\b", r"\bprotective\s+equipment\b"
        ],
        "incompatible_categories": [
            "Pipes & Plumbing", "Civil & Construction Materials", "Mechanical & Tooling",
            "Chemical & Plastics", "Furniture & Fixtures", "Electrical & Electronics",
            "Firefighting & Safety Equipment"
        ],
        "incompatible_scopes": [
            "pipe", "tube", "cement", "concrete", "cylinder", "transformer",
            "desk", "chair", "furniture", "fire extinguisher", "cable", "wiring"
        ]
    },
    "Mechanical & Tooling": {
        "keywords": [
            r"\blpg\b", r"\bgas\s+cylinders?\b", r"\bcylinder\s+valves?\b", r"\bpressure\s+vessels?\b"
        ],
        "incompatible_categories": [
            "Personal Protective Equipment", "Civil & Construction Materials",
            "Furniture & Fixtures", "Electrical & Electronics", "Pipes & Plumbing",
            "Chemical & Plastics", "Firefighting & Safety Equipment"
        ],
        "incompatible_scopes": [
            "helmet", "cement", "footwear", "cable", "desk", "chair", "furniture", "fire extinguisher"
        ]
    },
    "Chemical & Plastics": {
        "keywords": [
            r"\bpackaged\s+water\b", r"\bbottled\s+water\b", r"\bdrinking\s+water\b",
            r"\bplastic\s+migration\b", r"\bfood\s+grade\s+polyethylene\b"
        ],
        "incompatible_categories": [
            "Electrical & Electronics", "Personal Protective Equipment",
            "Civil & Construction Materials", "Furniture & Fixtures",
            "Pipes & Plumbing", "Mechanical & Tooling", "Firefighting & Safety Equipment"
        ],
        "incompatible_scopes": [
            "cable", "helmet", "cement", "pipe", "steel", "desk", "chair", "furniture", "fire extinguisher"
        ]
    },
    "Furniture & Fixtures": {
        "keywords": [
            r"\bdesks?\b", r"\bchairs?\b", r"\bfurniture\b", r"\btables?\b",
            r"\bcupboards?\b", r"\bshelves\b", r"\bshelving\b", r"\bbench(es)?\b",
            r"\bseat(ing|s)?\b", r"\bschool\s+furniture\b", r"\boffice\s+furniture\b",
            r"\bclassroom\b", r"\bblackboards?\b", r"\bwhiteboards?\b",
            r"\bwardrobe\b", r"\bcabinet\b", r"\bstorage\s+rack\b"
        ],
        "incompatible_categories": [
            "Personal Protective Equipment", "PPE & Safety Equipment",
            "Electrical & Electronics", "Building & Industrial Cables",
            "Pipes & Plumbing", "Pipes & Fittings",
            "Mechanical & Tooling", "Chemical & Plastics",
            "Civil & Construction Materials", "Firefighting & Safety Equipment"
        ],
        "incompatible_scopes": [
            "helmet", "cable", "pipe", "cement", "glove", "face shield",
            "cylinder", "transformer", "footwear", "respirator", "wiring",
            "concrete", "aggregate", "rebar", "harness", "mask",
            "water supply", "sewerage", "dielectric", "fire extinguisher"
        ]
    },
    "Firefighting & Safety Equipment": {
        "keywords": [
            r"\bfire\s+extinguishers?\b", r"\bfire\s+fighting\b", r"\bfire\s+suppression\b",
            r"\bsmoke\s+detectors?\b", r"\bfire\s+alarm\b", r"\bfire\s+hose\b", r"\bfire\s+hydrant\b"
        ],
        "incompatible_categories": [
            "Personal Protective Equipment", "PPE & Safety Equipment",
            "Electrical & Electronics", "Building & Industrial Cables",
            "Pipes & Plumbing", "Pipes & Fittings",
            "Mechanical & Tooling", "Chemical & Plastics",
            "Civil & Construction Materials", "Furniture & Fixtures"
        ],
        "incompatible_scopes": [
            "helmet", "cable", "pipe", "cement", "glove", "face shield",
            "cylinder", "transformer", "footwear", "respirator", "wiring",
            "concrete", "aggregate", "rebar", "harness", "mask", "desk", "chair"
        ]
    }
}


# Generic non-discriminative words that must NEVER count as product-specific overlap.
GENERIC_NON_DISCRIMINATIVE_WORDS = {
    # Quality/performance descriptors
    'safety', 'safe', 'durability', 'durable', 'quality', 'protection', 'protective',
    'resistant', 'resistance', 'compliance', 'performance', 'ergonomic', 'ergonomics',
    # Specification/standards terminology
    'standard', 'standards', 'specification', 'specifications', 'requirements',
    'requirement', 'code', 'practice', 'method', 'methods', 'clause', 'clauses',
    # Testing terminology
    'testing', 'test', 'tests', 'verification', 'inspection', 'certified',
    'certification', 'conformity',
    # Generic design/engineering
    'design', 'industrial', 'general', 'technical', 'engineering',
    'material', 'materials', 'grade', 'class', 'type', 'series', 'part',
    # Contextual location/facility words
    'building', 'buildings', 'facility', 'facilities', 'office', 'offices',
    'hospital', 'hospitals', 'school', 'schools', 'site', 'structure', 'structures',
    'work', 'works', 'commercial', 'residential', 'department', 'board', 'corp',
    'corporation', 'government', 'procurement', 'need', 'require', 'supply',
    'project', 'tender', 'india', 'indian', 'section', 'applicable', 'related', 'identify',
    # Common verbs/adjectives that leak across domains
    'used', 'high', 'heavy', 'duty', 'strength', 'density', 'procure', 'requiring'
}


class ScopeValidator:
    """
    Evaluates semantic and structural scope compatibility between procurement requirements
    and Indian Standards candidates.
    """

    def detect_domain(self, query_text: str, extracted_params: List[Dict[str, Any]]) -> Optional[str]:
        """
        Determines the primary procurement domain using regex and extracted parameters.
        """
        lower_query = query_text.lower()
        domain_scores: Dict[str, int] = {}

        # Check extracted product type
        product_type = ""
        for p in extracted_params:
            if p.get("field") == "Product Type":
                product_type = p.get("value", "").lower()

        for domain, rules in DOMAIN_DEFINITIONS.items():
            score = 0
            for kw in rules["keywords"]:
                if re.search(kw, lower_query):
                    score += 2
                if product_type and re.search(kw, product_type):
                    score += 5
            if score > 0:
                domain_scores[domain] = score

        if not domain_scores:
            return None

        # Return domain with highest score
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_domains[0][0]

    def evaluate_candidate_compatibility(
        self,
        query_text: str,
        domain: Optional[str],
        std_title: str,
        std_scope: str,
        std_category: str
    ) -> Tuple[str, float, str]:
        """
        Returns:
            decision: 'COMPATIBLE', 'PARTIALLY_COMPATIBLE', 'INCOMPATIBLE'
            scope_score: float (0.0 to 1.0)
            reason: explanatory rationale
        """
        title_lower = std_title.lower()
        scope_lower = std_scope.lower()
        cat_lower = (std_category or "").lower()
        query_lower = query_text.lower()

        # If a domain is identified, verify category and scope compatibility
        if domain and domain in DOMAIN_DEFINITIONS:
            rules = DOMAIN_DEFINITIONS[domain]

            # 1. Check for hard category incompatibility
            if any(incompat.lower() == cat_lower for incompat in rules["incompatible_categories"]):
                return (
                    "INCOMPATIBLE",
                    0.0,
                    f"Candidate standard belongs to category '{std_category}', "
                    f"which is incompatible with the detected '{domain}' procurement requirement."
                )

            # 2. Check for incompatible target keywords in title and scope
            for bad_kw in rules["incompatible_scopes"]:
                if re.search(rf"\b{bad_kw}\b", title_lower) and not re.search(rf"\b{bad_kw}\b", query_lower):
                    return (
                        "INCOMPATIBLE",
                        0.0,
                        f"Standard title specifies '{bad_kw}', which is outside the "
                        f"procurement scope for '{domain}'."
                    )

            # 3. Category match check
            if domain.lower() in cat_lower or cat_lower in domain.lower():
                matched_kws = [kw for kw in rules["keywords"] if re.search(kw, title_lower) or re.search(kw, scope_lower)]
                query_matches = [kw for kw in rules["keywords"] if re.search(kw, query_lower)]
                common_matches = set(matched_kws) & set(query_matches)

                if common_matches or any(re.search(kw, title_lower) for kw in query_matches):
                    return (
                        "COMPATIBLE",
                        1.0,
                        f"Directly satisfies '{domain}' requirement. "
                        f"Standard scope matches procurement specifications."
                    )
                else:
                    return (
                        "PARTIALLY_COMPATIBLE",
                        0.60,
                        f"Standard belongs to domain '{domain}', but title/scope "
                        f"does not match specific product keywords."
                    )

            # If domain detected, but standard category does not match domain, HARD REJECT
            return (
                "INCOMPATIBLE",
                0.0,
                f"Standard category '{std_category}' does not match detected procurement domain '{domain}'."
            )

        # ---------------------------------------------------------------
        # Domain NOT identified (unrecognized product type)
        # Use PRODUCT-SPECIFIC lexical overlap, filtering out generic words
        # ---------------------------------------------------------------
        q_tokens = set(re.findall(r"\b\w{4,}\b", query_lower)) - GENERIC_NON_DISCRIMINATIVE_WORDS
        title_tokens = set(re.findall(r"\b\w{4,}\b", title_lower)) - GENERIC_NON_DISCRIMINATIVE_WORDS
        scope_tokens = set(re.findall(r"\b\w{4,}\b", scope_lower)) - GENERIC_NON_DISCRIMINATIVE_WORDS
        overlap = q_tokens & (title_tokens | scope_tokens)

        if len(overlap) >= 2:
            return (
                "COMPATIBLE",
                0.85,
                f"Product-specific overlap confirmed across terms: "
                f"{', '.join(list(overlap)[:3])}."
            )
        elif len(overlap) == 1:
            return (
                "PARTIALLY_COMPATIBLE",
                0.40,
                f"Weak single-term match on '{list(overlap)[0]}'. "
                f"Insufficient for confident product scope matching."
            )
        else:
            return (
                "INCOMPATIBLE",
                0.0,
                "No product-specific scope overlap between tender requirements and "
                "standard scope. Generic terms (safety, building, durability, etc.) "
                "are insufficient for product matching."
            )


scope_validator = ScopeValidator()
