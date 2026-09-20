import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.standard import Standard, StandardClause, StandardRelationship
from app.services.evidence_service import evidence_service


def _build_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    standards = [
        Standard(
            id="helmet-std",
            is_number="IS 2925:1984",
            title="Specification for Industrial Safety Helmets",
            scope="Head protection against falling objects, mechanical impact, and electrical shocks up to 10 kV.",
            category="Personal Protective Equipment",
            title_ml="औद्योगिक सुरक्षा हेलमेट",
            status="CURRENT",
            certification_status="Mandatory",
            certification_scheme="BIS ISI Mark",
            qco_notification_number="QCO",
        ),
        Standard(
            id="helmet-mining-std",
            is_number="IS 9562:1980",
            title="Non-Metallic Safety Helmets for Mining",
            scope="Heavy-duty helmet shells for underground mining workers with reinforced crown protection.",
            category="Personal Protective Equipment",
            status="CURRENT",
            certification_status="Mandatory",
            certification_scheme="BIS ISI Mark",
        ),
        Standard(
            id="pipe-std",
            is_number="IS 4985:2021",
            title="Unplasticized PVC (UPVC) Pipes for Potable Water Supplies",
            scope="PVC pipes for potable water and irrigation systems.",
            category="Pipes & Plumbing",
            status="CURRENT",
            certification_status="Mandatory",
            certification_scheme="BIS ISI Mark",
            qco_notification_number="QCO",
        ),
        Standard(
            id="cable-std",
            is_number="IS 694:2010",
            title="PVC Insulated Cables for Working Voltages up to and including 1100 V",
            scope="Electrical power and control cables for building and industrial installations.",
            category="Electrical & Electronics",
            status="CURRENT",
            certification_status="Mandatory",
            certification_scheme="BIS ISI Mark",
            qco_notification_number="QCO",
        ),
        Standard(
            id="cement-std",
            is_number="IS 269:2015",
            title="Ordinary Portland Cement - Specification",
            scope="Cement for concrete applications and building work.",
            category="Civil & Construction Materials",
            status="CURRENT",
            certification_status="Mandatory",
            certification_scheme="BIS ISI Mark",
            qco_notification_number="QCO",
        ),
        Standard(
            id="transformer-std",
            is_number="IS 1180 (Part 1):2014",
            title="Outdoor Type Oil Immersed Distribution Transformers up to 2500 kVA, 33 kV",
            scope="Oil immersed distribution transformers for power distribution applications.",
            category="Electrical & Electronics",
            title_ml="तेल जलित वितरण ट्रांसफॉर्मर",
            status="CURRENT",
            certification_status="Mandatory",
            certification_scheme="BIS ISI Mark",
            qco_notification_number="QCO",
        ),
        Standard(
            id="old-helmet-std",
            is_number="IS 1234:1901",
            title="Obsolete Helmet Standard",
            scope="Superseded helmet specification.",
            category="Personal Protective Equipment",
            status="SUPERSEDED",
            certification_status="Voluntary",
        ),
    ]
    session.add_all(standards)
    session.commit()

    clauses = [
        # Helmet clauses
        ("helmet-std", "Clause 5.2", "Shock Absorption Test", "Transmitted force shall not exceed 5.0 kN at 50 J impact.", "Impact Absorption", "5.0 kN max"),
        ("helmet-std", "Clause 6.1", "Electrical Resistance Test", "Leakage current not exceeding 1.2 mA at 10 kV AC proof voltage.", "Dielectric Proof", "10 kV AC"),
        ("helmet-std", "Clause 7.3", "Temperature Conditioning", "Performance maintained post 4h conditioning at -10°C to +50°C.", "Thermal Range", "-10°C to 50°C"),
        ("helmet-mining-std", "Clause 6.1", "Heavy Shock Absorption", "Peak transmitted force shall not exceed 4.5 kN under 60 J impact.", "Mining Impact", "<= 4.5 kN"),
        # Pipe clauses
        ("pipe-std", "Clause 8.1", "Hydrostatic Internal Pressure Test", "Pipe shall withstand 4.2 times working pressure for 1 hour.", "Hydrostatic Burst", "4.2x rated bar"),
        ("pipe-std", "Clause 8.2", "Vicat Softening Temperature", "Vicat softening temperature shall not be less than 80°C.", "Thermal Softening", ">= 80°C"),
        # Cable clauses
        ("cable-std", "Clause 14.1", "Insulation Resistance Test", "Volume resistivity at 20°C >= 1 x 10^13 ohm-cm.", "Insulation Resistivity", ">= 10^13 ohm-cm"),
        ("cable-std", "Clause 15.1", "High Voltage AC Test", "Withstand AC test voltage of 3 kV RMS for 5 minutes without puncture.", "Dielectric AC Withstand", "3 kV AC"),
        # Cement clauses
        ("cement-std", "Clause 6.1", "Compressive Strength", "28-day compressive strength shall not be less than 53 MPa for 53 Grade.", "Compressive Strength", ">= 53 MPa"),
        # Transformer clauses
        ("transformer-std", "Clause 14.2", "Lightning Impulse Withstand Test", "Full wave impulse withstand voltage of 170 kV peak for 33 kV winding.", "Impulse Voltage", "170 kV peak"),
    ]
    for sid, num, title, req, param, limit in clauses:
        session.add(StandardClause(
            standard_id=sid, clause_number=num, title=title,
            requirement_text=req, tested_parameter=param, test_limit=limit,
        ))

    # Relationship: helmet -> mining helmet (related), helmet -> test method
    session.add(StandardRelationship(
        from_standard_id="helmet-std", to_standard_id="helmet-mining-std",
        relationship_type="Safety Standard", description="Complementary mining head protection.",
    ))
    session.commit()
    return session


def _top_is_number(result):
    assert result["recommendations"], f"Expected recommendations, got: {result['status']} — {result.get('abstention_reason')}"
    return result["recommendations"][0]["isNumber"]


# --------------------------------------------------------------------------
# Core product matching (regression)
# --------------------------------------------------------------------------

def test_helmet_query_matches_helmet_standard():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "Procure industrial safety helmets for construction workers.")
    assert result["status"] == "FOUND_VERIFIED_MATCH"
    assert _top_is_number(result) == "IS 2925:1984"


def test_helmet_query_with_spec_details_ranks_true_helmet_first():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session,
        "We need industrial helmets suitable for construction workers with impact resistance and electrical insulation.",
    )
    assert result["status"] == "FOUND_VERIFIED_MATCH"
    assert _top_is_number(result) == "IS 2925:1984"


def test_upvc_query_matches_pipe_standard():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "Procure UPVC pipes for potable water.")
    assert result["status"] == "FOUND_VERIFIED_MATCH"
    assert _top_is_number(result) == "IS 4985:2021"


def test_pvc_cable_query_matches_cable_standard():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "Procure PVC electrical cables.")
    assert result["status"] == "FOUND_VERIFIED_MATCH"
    assert _top_is_number(result) == "IS 694:2010"


def test_portland_cement_query_matches_cement_standard():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "Procure Portland cement.")
    assert result["status"] == "FOUND_VERIFIED_MATCH"
    assert _top_is_number(result) == "IS 269:2015"


def test_distribution_transformer_query_matches_transformer_standard():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "Procure oil immersed distribution transformers.")
    assert result["status"] == "FOUND_VERIFIED_MATCH"
    assert _top_is_number(result) == "IS 1180 (Part 1):2014"


# --------------------------------------------------------------------------
# Abstention: never hallucinate when out-of-corpus
# --------------------------------------------------------------------------

def test_fire_extinguisher_is_not_found_in_dataset():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "Procure fire extinguishers for the office.")
    assert result["status"] == "NOT_FOUND_IN_DATASET"
    assert result["recommendations"] == []
    assert result["abstention_reason"]


def test_school_desks_are_not_found_in_dataset():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "Procure school desks and chairs.")
    assert result["status"] == "NOT_FOUND_IN_DATASET"
    assert result["recommendations"] == []


def test_led_street_lights_do_not_recommend_transformer():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session,
        "Procure 2,000 LED street lights for a municipal project with energy efficiency, weather resistance and outdoor installation.",
    )
    assert result["status"] == "NOT_FOUND_IN_DATASET"
    assert result["recommendations"] == []


def test_random_unrelated_text_does_not_hallucinate_std():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "Plan a mountain hiking trip with hiking boots and a campsite.")
    assert result["status"] == "NOT_FOUND_IN_DATASET"
    assert result["recommendations"] == []


def test_empty_query_abstains():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "")
    assert result["status"] == "NOT_FOUND_IN_DATASET"
    assert result["recommendations"] == []


# --------------------------------------------------------------------------
# Multilingual input
# --------------------------------------------------------------------------

def test_hindi_query_matches_equivalent_product_classification():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "नगरपालिका के लिए बिजली के ट्रांसफॉर्मर खरीदें।")
    assert result["status"] in {"FOUND_VERIFIED_MATCH", "FOUND_PARTIAL_MATCH"}
    assert _top_is_number(result) == "IS 1180 (Part 1):2014"


def test_hindi_helmet_query_matches_helmet_standard():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "निर्माण कार्य के लिए हेलमेट खरीदें।")
    assert result["status"] in {"FOUND_VERIFIED_MATCH", "FOUND_PARTIAL_MATCH"}
    assert _top_is_number(result) == "IS 2925:1984"


# --------------------------------------------------------------------------
# Explicit IS reference & version awareness
# --------------------------------------------------------------------------

def test_explicit_is_reference_boosts_that_standard():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Supply cables as per IS 694 with PVC insulation for building wiring."
    )
    assert result["status"] == "FOUND_VERIFIED_MATCH"
    assert _top_is_number(result) == "IS 694:2010"


def test_superseded_standard_never_recommended_first():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "Procure industrial safety helmets for construction workers.")
    is_numbers = [r["isNumber"] for r in result["recommendations"]]
    assert "IS 1234:1901" not in is_numbers[:1]  # never first
    # If present at all, flagged with lower confidence
    for rec in result["recommendations"]:
        if rec["isNumber"] == "IS 1234:1901":
            assert rec["confidence"] < result["recommendations"][0]["confidence"]


# --------------------------------------------------------------------------
# Evidence features: coverage, related standards, why-not, conflicts
# --------------------------------------------------------------------------

def test_coverage_map_has_clause_evidence():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session,
        "We need industrial helmets for construction workers with impact resistance and electrical insulation.",
    )
    rec = result["recommendations"][0]
    assert rec["coverageMap"], "Coverage map must not be empty"
    assert any(c["covered"] for c in rec["coverageMap"])
    assert rec["matchedRequirements"] >= 1
    assert rec["totalRequirements"] == len(rec["coverageMap"])


def test_related_standards_discovered_through_graph():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Procure industrial safety helmets for construction workers."
    )
    rec = result["recommendations"][0]
    related_numbers = [r["isNumber"] for r in rec["relatedStandards"]]
    assert "IS 9562:1980" in related_numbers  # graph edge helmet -> mining helmet


def test_why_not_explains_runner_up():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Procure industrial safety helmets for construction workers with electrical insulation."
    )
    rec = result["recommendations"][0]
    if len(result["recommendations"]) > 1 or rec.get("whyNotAlternatives"):
        candidates = rec.get("whyNotAlternatives", [])
        for c in candidates:
            assert c["reason"], "Why-not entries must carry a reason"
            assert c["isNumber"] != rec["isNumber"]


def test_temperature_conflict_detected():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session,
        "Industrial helmets for foundry workers operating at 100°C continuous with impact resistance.",
    )
    rec = result["recommendations"][0]
    assert rec["isNumber"] == "IS 2925:1984"
    # The tender's 100°C exceeds clause 7.3's +50°C rating -> must be flagged somewhere
    conflict_text = " ".join(
        c["tenderSpec"] + " " + c["standardSpec"] for c in result["conflicts"]
    )
    assert "100" in conflict_text, "Temperature conflict (100°C vs 50°C) must be detected"


def test_certification_details_surfaced():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "Procure industrial safety helmets.")
    rec = result["recommendations"][0]
    assert rec["certification"]["required"] is True
    assert rec["certification"]["scheme"] == "BIS ISI Mark"
    assert rec["certification"]["status"].lower() == "mandatory"


def test_confidence_is_bounded_and_calibrated():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Procure industrial safety helmets with impact resistance."
    )
    for rec in result["recommendations"]:
        assert 0 < rec["confidence"] <= 96.0


def test_version_and_amendment_fields_populated():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "Procure industrial safety helmets.")
    rec = result["recommendations"][0]
    assert rec["latestVersion"]
    assert rec["amendment"]
    assert rec["status"] in {"CURRENT", "REAFFIRMED", "SUPERSEDED", "WITHDRAWN"}


# --------------------------------------------------------------------------
# NLP extraction service
# --------------------------------------------------------------------------

def test_nlp_extracts_numeric_requirements():
    from app.services.nlp_service import nlp_service
    reqs = nlp_service.extract_requirements(
        "The product should withstand a minimum load of 500 kg and operate between -10°C and 50°C."
    )
    fields = {r["field"] for r in reqs}
    assert "Operating Temperature Range" in fields or "Operating Temperature" in fields
    assert any("Load Capacity" in f or "500" in r["value"] for f in fields for r in reqs if r["field"] == f)


def test_nlp_extracts_is_reference():
    from app.services.nlp_service import nlp_service
    reqs = nlp_service.extract_requirements("Cables must comply with IS 694:2010 for building wiring.")
    refs = [r for r in reqs if r["field"] == "Referenced Standard"]
    assert refs and "IS 694" in refs[0]["value"]


# ==========================================================================
# GENERIC TEST MATRIX (SIH26108 acceptance criteria)
# Proves the compatibility framework, not per-product behavior.
# ==========================================================================

# --------------------------------------------------------------------------
# Adversarial: misleading generic words must not cause unrelated matches
# --------------------------------------------------------------------------

def test_material_only_structural_steel_rejects_form_specific_standards():
    """'structural steel' must NOT resolve to steel TUBES (IS 1239) — a material
    word alone cannot establish applicability to a form-specific standard."""
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Procure 5000 metres structural steel for bridge construction."
    )
    assert result["status"] in {"NOT_FOUND_IN_DATASET", "REJECTED_SCOPE_INCOMPATIBLE", "LOW_CONFIDENCE"}
    for rec in result["recommendations"]:
        assert rec["isNumber"] != "IS 4985:2021"  # pipe standard must not win


def test_hospital_electrical_equipment_does_not_recommend_transformer():
    """'hospital electrical equipment' — generic domain words must not drive applicability."""
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Procure electrical equipment for hospital use.",
    )
    # Either abstains or, if any standard is surfaced, it must NOT be the transformer
    if result["recommendations"]:
        assert result["recommendations"][0]["isNumber"] != "IS 1180 (Part 1):2014"
    else:
        assert result["status"] in {"NOT_FOUND_IN_DATASET", "REJECTED_SCOPE_INCOMPATIBLE", "LOW_CONFIDENCE"}


def test_steel_water_pipe_prefers_pipe_family_not_rebar():
    """Material + form: steel + water + pipe should not match unrelated steel products."""
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Procure steel water pipes for municipal water transmission."
    )
    if result["recommendations"]:
        assert result["recommendations"][0]["isNumber"] != "IS 269:2015"  # not cement
        assert result["recommendations"][0]["isNumber"] != "IS 1786:2008"  # not rebar


def test_construction_safety_helmet_never_matches_pipe_standards():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Construction safety helmets for site workers."
    )
    assert result["recommendations"], "Helmet query should still find the helmet standard"
    assert result["recommendations"][0]["isNumber"] == "IS 2925:1984"


def test_very_short_query_does_not_hallucinate():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "pipes")
    if result["recommendations"]:
        # only pipe standards may surface for a bare product noun
        assert result["recommendations"][0]["isNumber"].startswith("IS 4985") or \
               "pipe" in result["recommendations"][0]["title"].lower()
    else:
        assert result["status"] in {"NOT_FOUND_IN_DATASET", "LOW_CONFIDENCE", "REJECTED_SCOPE_INCOMPATIBLE"}


def test_vague_query_abstains_or_reports_honestly():
    session = _build_session()
    result = evidence_service.analyze_requirement(session, "We need some good quality stuff for the office.")
    assert result["recommendations"] == []
    assert result["status"] in {"NOT_FOUND_IN_DATASET", "LOW_CONFIDENCE", "REQUIRES_HUMAN_VERIFICATION"}


def test_noisy_tender_text_with_typos_still_honest():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "procure  industrail safty helmts  with impct resistence for constrction wrkers"
    )
    # OCR-typo text must never invent a standard; abstain or find the real one
    if result["recommendations"]:
        assert result["recommendations"][0]["isNumber"] in {"IS 2925:1984", "IS 9562:1980"}
    else:
        assert result["status"] in {"NOT_FOUND_IN_DATASET", "LOW_CONFIDENCE", "REQUIRES_HUMAN_VERIFICATION"}


def test_duplicate_requirements_do_not_break_pipeline():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session,
        "Industrial safety helmets with impact resistance. Helmets must have impact resistance. Impact resistance required.",
    )
    assert result["recommendations"][0]["isNumber"] == "IS 2925:1984"


# --------------------------------------------------------------------------
# Dataset boundary + provenance
# --------------------------------------------------------------------------

def test_no_standard_outside_database_is_ever_returned():
    """Every recommended IS number must exist in the session's standards table."""
    session = _build_session()
    known = {s.is_number for s in session.query(Standard).all()}
    for query in (
        "Procure industrial safety helmets.",
        "Procure UPVC pipes for potable water.",
        "Procure PVC electrical cables.",
        "Procure Portland cement.",
        "Procure distribution transformers.",
    ):
        result = evidence_service.analyze_requirement(session, query)
        for rec in result["recommendations"]:
            assert rec["isNumber"] in known, f"Hallucinated standard {rec['isNumber']}"


def test_rejected_candidates_carry_structured_reasons():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Procure PVC electrical cables for building wiring."
    )
    # rejected_candidates field exists and every entry is structured
    for rc in result.get("rejected_candidates", []):
        assert rc["status"].startswith("REJECTED_")
        assert rc["reasons"]
        assert rc["failedChecks"]


def test_missing_specifications_are_detected_generically():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Procure industrial safety helmets."
    )
    assert isinstance(result.get("missing_specifications"), list)
    # A bare product query should flag context gaps (application / testing / certification)
    assert result["missing_specifications"]


def test_procurement_model_is_returned():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Procure 100 UPVC pipes for potable water supply."
    )
    model = result.get("procurement_model")
    if model and result["recommendations"]:
        assert model["product"]
        assert model["quantity"] == "100"


def test_partial_match_status_on_weaker_evidence():
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Industrial helmets with impact resistance and electrical insulation for construction workers."
    )
    assert result["status"] in {"FOUND_VERIFIED_MATCH", "FOUND_PARTIAL_MATCH"}
    assert result["recommendations"][0]["isNumber"] == "IS 2925:1984"


def test_no_cross_standard_clause_contamination():
    """Every key clause returned must belong to the recommended standard itself."""
    session = _build_session()
    result = evidence_service.analyze_requirement(
        session, "Industrial safety helmets with impact resistance."
    )
    std_clause_owners = {}
    for cl in session.query(StandardClause).all():
        std_clause_owners[(cl.standard_id, cl.clause_number)] = True
    for rec in result["recommendations"]:
        std = session.query(Standard).filter(Standard.is_number == rec["isNumber"]).first()
        for kc in rec["keyClauses"]:
            assert (std.id, kc["clause"]) in std_clause_owners, \
                f"Clause {kc['clause']} does not belong to {rec['isNumber']}"
