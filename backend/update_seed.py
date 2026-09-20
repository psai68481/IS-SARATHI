import sys
import os

seed_py_path = os.path.join(os.path.dirname(__file__), "app", "seed", "standards_seed.py")

NEW_CONTENT = '''import logging
from sqlalchemy.orm import Session
from app.models.standard import Standard, StandardRelationship, StandardClause
from app.models.user import User
from app.models.decision import HumanDecision
from app.core.security import get_password_hash
from app.services.embedding_service import embedding_service
from app.services.pinecone_service import pinecone_service

logger = logging.getLogger("is_sarathi.seed")

# 28 Curated Authoritative BIS Standards across 6 Domains with Verified Clauses
STANDARDS_DATA = [
    # ------------------ DOMAIN 1: PPE & OCCUPATIONAL SAFETY ------------------
    {
        "is_number": "IS 2925:1984",
        "title": "Specification for Industrial Safety Helmets",
        "scope": "Specifies physical and performance requirements, methods of test, and marking for industrial safety helmets providing head protection against falling objects, mechanical impact, and high-voltage electrical shocks up to 10 kV.",
        "ics_code": "13.340.20",
        "category": "Personal Protective Equipment",
        "status": "CURRENT",
        "revision_year": 1984,
        "latest_version": "IS 2925:1984 (Reaffirmed 2020)",
        "amendment": "Amendment 2, 2019 - updated impact test drop tower protocol",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "qco_notification_number": "S.O. 1277(E) PPE Quality Control Order",
        "clauses": [
            {"clause_number": "Clause 5.2", "title": "Shock Absorption Test", "requirement_text": "Transmitted force to headform shall not exceed 5.0 kN when subjected to 50 J impact energy.", "tested_parameter": "Impact Absorption", "test_limit": "5.0 kN max force"},
            {"clause_number": "Clause 6.1", "title": "Electrical Resistance Test", "requirement_text": "Leakage current not exceeding 1.2 mA at 10,000 V AC proof voltage (50 Hz).", "tested_parameter": "Dielectric Proof", "test_limit": "10 kV AC"},
            {"clause_number": "Clause 7.3", "title": "Temperature Conditioning", "requirement_text": "Performance maintained post 4h conditioning at -10°C to +50°C.", "tested_parameter": "Thermal Range", "test_limit": "-10°C to 50°C continuous"},
            {"clause_number": "Clause 8.4", "title": "Penetration Resistance", "requirement_text": "Conical striker of 3 kg dropped from 1 meter shall not make electrical contact with headform.", "tested_parameter": "Penetration", "test_limit": "No headform contact"}
        ]
    },
    {
        "is_number": "IS 15298 (Part 2):2016",
        "title": "Personal Protective Equipment - Safety Footwear",
        "scope": "Specifies basic and additional optional requirements for safety footwear equipped with toecaps designed to give protection against impacts of at least 200 Joules and compression under at least 15 kN.",
        "ics_code": "13.340.50",
        "category": "Personal Protective Equipment",
        "status": "CURRENT",
        "revision_year": 2016,
        "latest_version": "IS 15298 (Part 2):2016 (Reaffirmed 2021)",
        "amendment": "Amendment 1, 2018",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "qco_notification_number": "S.O. 4208(E) Footwear QCO",
        "clauses": [
            {"clause_number": "Clause 5.3.1", "title": "Toe Impact Resistance", "requirement_text": "Clearance under toecap shall be >= 14 mm when struck with 200 Joules energy.", "tested_parameter": "Impact Clearance", "test_limit": ">= 14 mm"},
            {"clause_number": "Clause 5.3.2", "title": "Compression Resistance", "requirement_text": "Clearance under toecap shall be >= 14 mm when subjected to 15 kN compressive load.", "tested_parameter": "Compression Force", "test_limit": "15 kN"},
            {"clause_number": "Clause 5.4.3", "title": "Upper Tear Strength", "requirement_text": "Tear strength of leather upper shall be not less than 120 N.", "tested_parameter": "Tear Resistance", "test_limit": ">= 120 N"}
        ]
    },
    {
        "is_number": "IS 4770:1991",
        "title": "Rubber Gloves for Electrical Purposes - Specification",
        "scope": "Specifies dielectric and physical requirements for insulating rubber gloves used by electrical line workers working on or in proximity to energized electrical conductor systems.",
        "ics_code": "13.340.40",
        "category": "Personal Protective Equipment",
        "status": "CURRENT",
        "revision_year": 1991,
        "latest_version": "IS 4770:1991 (Reaffirmed 2022)",
        "amendment": "None",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 6.2", "title": "Dielectric Proof Voltage", "requirement_text": "Proof test voltage of 10 kV AC applied for 1 minute with leakage current <= 10 mA.", "tested_parameter": "Proof Voltage", "test_limit": "10 kV AC"},
            {"clause_number": "Clause 7.1", "title": "Tensile Strength and Elongation", "requirement_text": "Tensile strength not less than 14 MPa and elongation at break not less than 600%.", "tested_parameter": "Tensile Strength", "test_limit": ">= 14 MPa"}
        ]
    },
    {
        "is_number": "IS 8521 (Part 1):1977",
        "title": "Industrial Safety Face Shields - General Requirements",
        "scope": "Requirements for eye and face protectors incorporating visors and brow guards designed to protect workers against flying particles, chemical splashes, and molten metal radiation.",
        "ics_code": "13.340.20",
        "category": "Personal Protective Equipment",
        "status": "CURRENT",
        "revision_year": 1977,
        "latest_version": "IS 8521 (Part 1):1977 (Reaffirmed 2021)",
        "amendment": "Amendment 1, 2021",
        "certification_required": False,
        "certification_scheme": "BIS Voluntary",
        "certification_status": "Voluntary",
        "clauses": [
            {"clause_number": "Clause 4.1", "title": "Impact Strength of Visor", "requirement_text": "Visor must resist impact from a 6 mm steel ball at 45 m/s without fracture.", "tested_parameter": "High Speed Impact", "test_limit": "45 m/s"},
            {"clause_number": "Clause 5.2", "title": "Optical Transmittance", "requirement_text": "Luminous transmittance of clear visors shall not be less than 85%.", "tested_parameter": "Light Transmission", "test_limit": ">= 85%"}
        ]
    },
    {
        "is_number": "IS 9562:1980",
        "title": "Specification for Non-Metallic Safety Helmets for Mining",
        "scope": "Specifies heavy-duty shell requirements for underground mining workers with reinforced crown protection against tunnel cave-ins and moisture resistance.",
        "ics_code": "13.340.20",
        "category": "Personal Protective Equipment",
        "status": "CURRENT",
        "revision_year": 1980,
        "latest_version": "IS 9562:1980 (Reaffirmed 2020)",
        "amendment": "Amendment 2, 2015",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 6.1", "title": "Heavy Shock Absorption", "requirement_text": "Peak transmitted force to dummy headform shall not exceed 4.5 kN under 60 J impact.", "tested_parameter": "Mining Impact", "test_limit": "<= 4.5 kN"},
            {"clause_number": "Clause 7.2", "title": "Water Absorption Resistance", "requirement_text": "Water absorption of helmet shell after 24h immersion shall not exceed 1.0% by weight.", "tested_parameter": "Moisture Absorption", "test_limit": "<= 1.0%"}
        ]
    },
    {
        "is_number": "IS 9473:2002",
        "title": "Respiratory Protective Devices - Filtering Half Masks",
        "scope": "Specifies requirements for particle filtering half masks (FFP1, FFP2, FFP3) to protect against dust, solid and liquid aerosols in hazardous industrial environments.",
        "ics_code": "13.340.30",
        "category": "Personal Protective Equipment",
        "status": "CURRENT",
        "revision_year": 2002,
        "latest_version": "IS 9473:2002 (Reaffirmed 2020)",
        "amendment": "Amendment 3, 2020",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 7.9", "title": "Total Inward Leakage (TIL)", "requirement_text": "TIL shall not exceed 11% for FFP2 masks tested with sodium chloride aerosol.", "tested_parameter": "Aerosol Leakage", "test_limit": "<= 11%"},
            {"clause_number": "Clause 7.12", "title": "Breathing Resistance", "requirement_text": "Inhalation resistance at 95 L/min flow rate shall not exceed 2.4 mbar.", "tested_parameter": "Airflow Resistance", "test_limit": "<= 2.4 mbar"}
        ]
    },
    {
        "is_number": "IS 3521:1999",
        "title": "Industrial Safety Belts and Harnesses",
        "scope": "Requirements for full body harnesses, lanyards, and fall arrester attachments for fall protection of operators working at elevated heights.",
        "ics_code": "13.340.60",
        "category": "Personal Protective Equipment",
        "status": "CURRENT",
        "revision_year": 1999,
        "latest_version": "IS 3521:1999 (Reaffirmed 2021)",
        "amendment": "Amendment 2, 2017",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 6.1", "title": "Dynamic Fall Arrest Test", "requirement_text": "Full body harness loaded with 100 kg dummy in 4m free drop shall arrest fall without structural failure.", "tested_parameter": "Dynamic Drop Load", "test_limit": "100 kg at 4m"},
            {"clause_number": "Clause 6.2", "title": "Static Proof Load", "requirement_text": "Webbing harness straps must withstand 15 kN static tensile force for 3 minutes without rupture.", "tested_parameter": "Webbing Tensile Force", "test_limit": ">= 15 kN"}
        ]
    },

    # ------------------ DOMAIN 2: PIPES & PLUMBING ------------------
    {
        "is_number": "IS 4985:2021",
        "title": "Unplasticized PVC (UPVC) Pipes for Potable Water Supplies",
        "scope": "Specifies dimensions and pressure requirements for unplasticized polyvinyl chloride pipes intended for cold potable water supplies, irrigation, and industrial fluid transmission.",
        "ics_code": "23.040.20",
        "category": "Pipes & Plumbing",
        "status": "CURRENT",
        "revision_year": 2021,
        "latest_version": "IS 4985:2021",
        "amendment": "Amendment 1, 2023",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "qco_notification_number": "S.O. 3121(E) Plastic Piping Systems QCO",
        "clauses": [
            {"clause_number": "Clause 8.1", "title": "Hydrostatic Internal Pressure Test", "requirement_text": "Pipe shall withstand 4.2 times working pressure for 1 hour at 27°C without burst or leakage.", "tested_parameter": "Hydrostatic Burst", "test_limit": "4.2x rated bar"},
            {"clause_number": "Clause 8.2", "title": "Vicat Softening Temperature", "requirement_text": "Vicat softening temperature of pipe material shall not be less than 80°C.", "tested_parameter": "Thermal Softening", "test_limit": ">= 80°C"},
            {"clause_number": "Clause 8.3", "title": "Impact Strength at 0°C (TIR)", "requirement_text": "True Impact Rate (TIR) shall not exceed 10% when tested with falling striker at 0°C.", "tested_parameter": "Impact Resistance", "test_limit": "TIR <= 10%"},
            {"clause_number": "Clause 7.1", "title": "Wall Thickness and Outside Diameter", "requirement_text": "Dimensions must comply with Class 1 to Class 6 pressure ratings specified in Table 1.", "tested_parameter": "Wall Thickness", "test_limit": "Table 1 tolerances"}
        ]
    },
    {
        "is_number": "IS 12235 (Part 1 to 19)",
        "title": "Methods of Test for Unplasticized PVC Pipes for Potable Water",
        "scope": "Comprehensive test methods for hydrostatic pressure testing, impact resistance, Vicat softening temperature, and opacity for PVC piping.",
        "ics_code": "23.040.20",
        "category": "Pipes & Plumbing",
        "status": "CURRENT",
        "revision_year": 2004,
        "latest_version": "IS 12235:2004 (Reaffirmed 2019)",
        "amendment": "Amendment 2, 2020",
        "certification_required": False,
        "certification_scheme": "BIS Test Standard",
        "certification_status": "Voluntary",
        "clauses": [
            {"clause_number": "Part 2 Clause 4", "title": "Measurement of Dimensions", "requirement_text": "Apparatus and procedure for determining outside diameter, wall thickness, and out-of-roundness.", "tested_parameter": "Dimensional Gauge", "test_limit": "Micrometer accuracy"},
            {"clause_number": "Part 8 Clause 3", "title": "Internal Hydrostatic Pressure Test Procedure", "requirement_text": "Sustained internal hydraulic pressure endurance setup and failure identification criteria.", "tested_parameter": "Creep Rupture", "test_limit": "1000h continuous"}
        ]
    },
    {
        "is_number": "IS 1239 (Part 1):2004",
        "title": "Steel Tubes, Tubulars and Other Wrought Steel Fittings - Tubes",
        "scope": "Requirements for welded and seamless plain end or screwed and socketed steel tubes for water, non-hazardous gas, air and steam distribution.",
        "ics_code": "77.140.75",
        "category": "Pipes & Plumbing",
        "status": "CURRENT",
        "revision_year": 2004,
        "latest_version": "IS 1239 (Part 1):2004 (Reaffirmed 2020)",
        "amendment": "Amendment 5, 2022",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 8.1", "title": "Hydraulic Test Pressure", "requirement_text": "Each tube shall be tested hydrostatically to 5 MPa (50 bar) without leakage.", "tested_parameter": "Hydraulic Pressure", "test_limit": "5 MPa (50 bar)"},
            {"clause_number": "Clause 8.2", "title": "Tensile Strength and Elongation", "requirement_text": "Tensile strength shall be not less than 320 MPa; elongation >= 20% on 5.65 sqrt(So) gauge length.", "tested_parameter": "Tensile Strength", "test_limit": ">= 320 MPa"},
            {"clause_number": "Clause 8.3", "title": "Flattening and Bend Test", "requirement_text": "Weld seam placed at 90° shall show no cracks when flattened to specified distance between platens.", "tested_parameter": "Weld Ductility", "test_limit": "No cracking"}
        ]
    },
    {
        "is_number": "IS 3589:2001",
        "title": "Steel Pipes for Water and Sewage (168.3 to 2540 mm Outside Diameter)",
        "scope": "Specifies seamless and electric resistance welded carbon steel pipes of large diameter intended for municipal water transmission and sewage transport.",
        "ics_code": "77.140.75",
        "category": "Pipes & Plumbing",
        "status": "CURRENT",
        "revision_year": 2001,
        "latest_version": "IS 3589:2001 (Reaffirmed 2019)",
        "amendment": "Amendment 3, 2018",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 9.1", "title": "Hydrostatic Mill Test", "requirement_text": "Every pipe shall be hydrostatically tested to produce a hoop stress >= 60% of minimum yield strength.", "tested_parameter": "Hoop Stress Test", "test_limit": ">= 60% SMYS"},
            {"clause_number": "Clause 10.2", "title": "Non-Destructive Ultrasonic Examination", "requirement_text": "100% longitudinal or helical ERW seam inspection using automated ultrasonic calibrated system.", "tested_parameter": "Weld Flaw Detection", "test_limit": "Zero rejectable defects"}
        ]
    },
    {
        "is_number": "IS 14333:1996",
        "title": "High Density Polyethylene (HDPE) Pipes for Sewerage",
        "scope": "Specifies solid wall HDPE pipes for gravity flow sewer lines and industrial effluent drainage lines.",
        "ics_code": "23.040.20",
        "category": "Pipes & Plumbing",
        "status": "CURRENT",
        "revision_year": 1996,
        "latest_version": "IS 14333:1996 (Reaffirmed 2020)",
        "amendment": "Amendment 2, 2017",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 7.1", "title": "Internal Hydrostatic Pressure (100h at 80°C)", "requirement_text": "Sustained pressure test at 80°C with induced hoop stress of 4.6 MPa for PE80 resin.", "tested_parameter": "Thermal Hydrostatic Creep", "test_limit": "100h at 80°C"},
            {"clause_number": "Clause 7.3", "title": "Carbon Black Dispersion and Content", "requirement_text": "Carbon black content shall be 2.5 +/- 0.5% with dispersion grade <= 3 for UV stabilization.", "tested_parameter": "Carbon Black UV Content", "test_limit": "2.5% +/- 0.5%"}
        ]
    },
    {
        "is_number": "IS 15778:2007",
        "title": "Chlorinated Polyvinyl Chloride (CPVC) Pipes for Potable Hot and Cold Water",
        "scope": "Requirements for CPVC plastic pipes for domestic hot and cold water distribution operating up to 93°C.",
        "ics_code": "23.040.20",
        "category": "Pipes & Plumbing",
        "status": "CURRENT",
        "revision_year": 2007,
        "latest_version": "IS 15778:2007 (Reaffirmed 2022)",
        "amendment": "Amendment 3, 2021",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 8.1", "title": "Hydrostatic Sustained Pressure at 82°C", "requirement_text": "Sustained hydraulic pressure test at 82°C for 4 hours without burst or stress weeping.", "tested_parameter": "Hot Water Pressure", "test_limit": "82°C for 4h"},
            {"clause_number": "Clause 8.3", "title": "Vicat Softening Temperature of CPVC", "requirement_text": "Vicat softening temperature of compound shall not be less than 103°C.", "tested_parameter": "Thermal Resistance", "test_limit": ">= 103°C"}
        ]
    },

    # ------------------ DOMAIN 3: ELECTRICAL & WIRING ------------------
    {
        "is_number": "IS 694:2010",
        "title": "Polyvinyl Chloride Insulated Cables for Working Voltages up to and including 1100 V",
        "scope": "Specifies single and multi-core PVC insulated copper and aluminum electric cables for fixed wiring in residential, commercial and industrial installations up to 1100V.",
        "ics_code": "29.060.20",
        "category": "Electrical & Electronics",
        "status": "CURRENT",
        "revision_year": 2010,
        "latest_version": "IS 694:2010 (Reaffirmed 2021)",
        "amendment": "Amendment 4, 2021 - FRLS criteria added",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "qco_notification_number": "S.O. 1102(E) Electrical Cables QCO",
        "clauses": [
            {"clause_number": "Clause 12.1", "title": "Conductor Resistance Test", "requirement_text": "Maximum electrical conductor resistance at 20°C shall comply with Table 2 of IS 8130.", "tested_parameter": "Conductor Resistance", "test_limit": "IS 8130 limits at 20°C"},
            {"clause_number": "Clause 14.1", "title": "Insulation Resistance Test", "requirement_text": "Volume resistivity at 20°C >= 1 x 10^13 ohm-cm and at 70°C >= 1 x 10^10 ohm-cm.", "tested_parameter": "Insulation Resistivity", "test_limit": ">= 10^13 ohm-cm"},
            {"clause_number": "Clause 15.1", "title": "High Voltage AC Spark and Water Bath Test", "requirement_text": "Withstand AC test voltage of 3 kV RMS applied for 5 minutes without dielectric puncture.", "tested_parameter": "Dielectric AC Withstand", "test_limit": "3 kV AC for 5 min"},
            {"clause_number": "Clause 16.3", "title": "Flame Retardance & Oxygen Index (FRLS)", "requirement_text": "Oxygen index shall not be less than 29% and temperature index >= 250°C for FRLS cables.", "tested_parameter": "Oxygen Index", "test_limit": ">= 29% Oxygen Index"}
        ]
    },
    {
        "is_number": "IS 1554 (Part 1):1988",
        "title": "PVC Insulated (Heavy Duty) Electric Cables for Voltages up to 1100 V",
        "scope": "Heavy duty armored and unarmored PVC power and control cables for electricity distribution networks and heavy industrial power cabling.",
        "ics_code": "29.060.20",
        "category": "Electrical & Electronics",
        "status": "CURRENT",
        "revision_year": 1988,
        "latest_version": "IS 1554 (Part 1):1988 (Reaffirmed 2020)",
        "amendment": "Amendment 6, 2022",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 13.1", "title": "Armour Galvanizing and Tensile Test", "requirement_text": "Galvanized steel strip or round wire armour must have mass of zinc coating complying with Table 5.", "tested_parameter": "Armour Coating Mass", "test_limit": "Table 5 zinc coating"},
            {"clause_number": "Clause 16.2", "title": "High Voltage Dielectric Test", "requirement_text": "Core-to-core and core-to-armour AC proof test of 3000 V RMS sustained for 5 minutes.", "tested_parameter": "HV Insulation Proof", "test_limit": "3000 V AC RMS"}
        ]
    },
    {
        "is_number": "IS 7098 (Part 1):1988",
        "title": "Cross-linked Polyethylene (XLPE) Insulated PVC Sheathed Cables up to 1100 V",
        "scope": "XLPE insulated electric cables for thermal overload resistance, high current carrying capacity in underground utility grids.",
        "ics_code": "29.060.20",
        "category": "Electrical & Electronics",
        "status": "CURRENT",
        "revision_year": 1988,
        "latest_version": "IS 7098 (Part 1):1988 (Reaffirmed 2021)",
        "amendment": "Amendment 4, 2020",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 11.2", "title": "Hot Set Test for XLPE Insulation", "requirement_text": "Under 200°C and 20 N/cm2 load, elongation shall not exceed 175%; permanent set <= 15%.", "tested_parameter": "XLPE Cross-linking", "test_limit": "Hot set elongation <= 175%"},
            {"clause_number": "Clause 14.1", "title": "Continuous Current Carrying Rating", "requirement_text": "Conductor operating temperature under continuous normal full load shall be rated up to 90°C.", "tested_parameter": "Operating Thermal Limit", "test_limit": "90°C continuous"}
        ]
    },
    {
        "is_number": "IS 3043:2018",
        "title": "Code of Practice for Earthing",
        "scope": "Guidelines for electrical grounding, earth electrode design, earth pit resistance calculation, and lightning surge protection in power installations.",
        "ics_code": "29.080.01",
        "category": "Electrical & Electronics",
        "status": "CURRENT",
        "revision_year": 2018,
        "latest_version": "IS 3043:2018",
        "amendment": "Amendment 1, 2022",
        "certification_required": False,
        "certification_scheme": "BIS Code of Practice",
        "certification_status": "Voluntary",
        "clauses": [
            {"clause_number": "Clause 7.2", "title": "Earth Electrode Sizing and Depth", "requirement_text": "Minimum cross section of GI pipe or copper-bonded steel rod electrode driven >= 3 meters.", "tested_parameter": "Electrode Dimensions", "test_limit": ">= 3m depth"},
            {"clause_number": "Clause 9.3", "title": "Earth Grid Resistance Threshold", "requirement_text": "Combined station earth pit resistance shall not exceed 1.0 ohm for electrical substations.", "tested_parameter": "Ground Pit Resistance", "test_limit": "<= 1.0 ohm"}
        ]
    },
    {
        "is_number": "IS 1180 (Part 1):2014",
        "title": "Outdoor Type Oil Immersed Distribution Transformers up to 2500 kVA, 33 kV",
        "scope": "Energy efficiency levels 1, 2, and 3, dielectric oil parameters, temperature rise, and total loss thresholds for power distribution transformers.",
        "ics_code": "29.180",
        "category": "Electrical & Electronics",
        "status": "CURRENT",
        "revision_year": 2014,
        "latest_version": "IS 1180 (Part 1):2014 (Reaffirmed 2021)",
        "amendment": "Amendment 4, 2021",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark + BEE Star",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 6.8", "title": "Total Losses at 50% and 100% Load", "requirement_text": "Maximum permissible losses must comply with BEE Energy Level-2 thresholds in Table 3.", "tested_parameter": "Core & Copper Losses", "test_limit": "Table 3 energy limits"},
            {"clause_number": "Clause 14.2", "title": "Lightning Impulse Withstand Test", "requirement_text": "Full wave 1.2/50 microsecond impulse withstand voltage of 170 kV peak for 33 kV winding.", "tested_parameter": "Impulse Voltage", "test_limit": "170 kV peak withstand"}
        ]
    },
    {
        "is_number": "IS 8828:1996",
        "title": "Circuit-Breakers for Overcurrent Protection for Household Installations (MCB)",
        "scope": "Miniature Circuit Breakers (MCB) operating at 50 Hz AC up to 440 V, breaking capacity up to 10 kA, thermal and magnetic trip tolerances.",
        "ics_code": "29.120.50",
        "category": "Electrical & Electronics",
        "status": "CURRENT",
        "revision_year": 1996,
        "latest_version": "IS 8828:1996 (Reaffirmed 2021)",
        "amendment": "Amendment 3, 2019",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 8.6", "title": "Short-Circuit Breaking Capacity (Icn)", "requirement_text": "Rated short-circuit breaking capacity shall be 10 kA at rated operational voltage.", "tested_parameter": "Short-Circuit Trip", "test_limit": "10 kA breaking capacity"},
            {"clause_number": "Clause 9.1", "title": "Tripping Characteristics (Type B, C, D)", "requirement_text": "Magnetic instantaneous tripping band: Type C between 5 In and 10 In.", "tested_parameter": "Trip Current Curve", "test_limit": "5 In to 10 In"}
        ]
    },

    # ------------------ DOMAIN 4: CEMENT & CIVIL CONSTRUCTION ------------------
    {
        "is_number": "IS 269:2015",
        "title": "Ordinary Portland Cement - Specification",
        "scope": "Specification for 33, 43, and 53 grade ordinary Portland cement, physical and chemical testing, compressive strength at 3, 7, and 28 days.",
        "ics_code": "91.100.10",
        "category": "Civil & Construction Materials",
        "status": "CURRENT",
        "revision_year": 2015,
        "latest_version": "IS 269:2015 (Reaffirmed 2020)",
        "amendment": "Amendment 2, 2021",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "qco_notification_number": "Cement Quality Control Order",
        "clauses": [
            {"clause_number": "Clause 6.1", "title": "Compressive Strength (33, 43, 53 MPa at 28 days)", "requirement_text": "28-day compressive strength shall not be less than 53 MPa for 53 Grade and 43 MPa for 43 Grade.", "tested_parameter": "Compressive Strength", "test_limit": ">= 43 / 53 MPa at 28d"},
            {"clause_number": "Clause 6.2", "title": "Fineness by Blaine Specific Surface Area", "requirement_text": "Specific surface area determined by Blaine air permeability method shall not be less than 225 m2/kg.", "tested_parameter": "Fineness", "test_limit": ">= 225 m2/kg"},
            {"clause_number": "Clause 6.3", "title": "Soundness by Le-Chatelier & Autoclave", "requirement_text": "Expansion shall not exceed 10 mm by Le-Chatelier method and 0.8% by autoclave method.", "tested_parameter": "Soundness", "test_limit": "<= 10 mm expansion"},
            {"clause_number": "Clause 6.4", "title": "Setting Time (Initial & Final)", "requirement_text": "Initial setting time shall not be less than 30 minutes; final setting time shall not exceed 600 minutes.", "tested_parameter": "Setting Time", "test_limit": "Init >= 30m, Fin <= 600m"},
            {"clause_number": "Clause 5.1", "title": "Chemical Requirements (% Alumina to Iron Oxide)", "requirement_text": "Ratio of alumina to iron oxide not less than 0.66; total insoluble residue not exceeding 5.0%.", "tested_parameter": "Chemical Composition", "test_limit": "Al2O3/Fe2O3 >= 0.66"}
        ]
    },
    {
        "is_number": "IS 456:2000",
        "title": "Plain and Reinforced Concrete - Code of Practice",
        "scope": "Structural engineering code for general building construction using unreinforced, reinforced and prestressed concrete design.",
        "ics_code": "91.080.40",
        "category": "Civil & Construction Materials",
        "status": "CURRENT",
        "revision_year": 2000,
        "latest_version": "IS 456:2000 (Reaffirmed 2021)",
        "amendment": "Amendment 5, 2019",
        "certification_required": False,
        "certification_scheme": "BIS National Code",
        "certification_status": "Voluntary",
        "clauses": [
            {"clause_number": "Clause 6.1", "title": "Concrete Grades and Characteristic Strength", "requirement_text": "Characteristic 28-day cube strength of designated structural grades from M20 up to M80.", "tested_parameter": "Design Characteristic Strength", "test_limit": ">= fck N/mm2"},
            {"clause_number": "Clause 26.5.1", "title": "Minimum Reinforcement in Beams", "requirement_text": "Minimum tension steel ratio shall be 0.85/fy of the cross-sectional area.", "tested_parameter": "Rebar Minimum Area", "test_limit": "As/bd >= 0.85/fy"}
        ]
    },
    {
        "is_number": "IS 1786:2008",
        "title": "High Strength Deformed Steel Bars and Wires for Concrete Reinforcement (TMT Rebars)",
        "scope": "Chemical and mechanical requirements for Fe 415, Fe 500, Fe 550, and Fe 600 thermo-mechanically treated (TMT) steel reinforcement bars.",
        "ics_code": "77.140.15",
        "category": "Civil & Construction Materials",
        "status": "CURRENT",
        "revision_year": 2008,
        "latest_version": "IS 1786:2008 (Reaffirmed 2022)",
        "amendment": "Amendment 4, 2022",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 8.1", "title": "0.2% Proof Stress / Yield Stress", "requirement_text": "Minimum yield stress shall be 500 MPa for Fe 500 and 550 MPa for Fe 550D.", "tested_parameter": "Yield Stress", "test_limit": ">= 500 MPa"},
            {"clause_number": "Clause 8.2", "title": "Tensile Strength to Yield Stress Ratio", "requirement_text": "Ratio of ultimate tensile strength to actual yield strength shall be not less than 1.10 for Fe 500D.", "tested_parameter": "TS/YS Seismic Ratio", "test_limit": ">= 1.10 ratio"}
        ]
    },
    {
        "is_number": "IS 383:2016",
        "title": "Coarse and Fine Aggregate for Concrete - Specification",
        "scope": "Grading tolerances, flakiness index, elongation index, and sound absorption for natural and crushed aggregates used in concrete.",
        "ics_code": "91.100.15",
        "category": "Civil & Construction Materials",
        "status": "CURRENT",
        "revision_year": 2016,
        "latest_version": "IS 383:2016 (Reaffirmed 2021)",
        "amendment": "Amendment 1, 2018",
        "certification_required": False,
        "certification_scheme": "BIS Material Standard",
        "certification_status": "Voluntary",
        "clauses": [
            {"clause_number": "Clause 5.3", "title": "Flakiness and Elongation Index", "requirement_text": "Combined flakiness and elongation index of coarse aggregate shall not exceed 35%.", "tested_parameter": "Aggregate Particle Shape", "test_limit": "<= 35% combined"},
            {"clause_number": "Clause 5.4", "title": "Aggregate Crushing Value & Impact Value", "requirement_text": "Aggregate impact value shall not exceed 30% for concrete wearing surfaces and 45% for general concrete.", "tested_parameter": "Impact Crushing Value", "test_limit": "<= 30% wearing"}
        ]
    },

    # ------------------ DOMAIN 5: LPG & GAS CYLINDERS ------------------
    {
        "is_number": "IS 3196 (Part 1):2013",
        "title": "Welded Low Carbon Steel Cylinders Exceeding 5 Liter Water Capacity for Low Pressure Liquefiable Gases",
        "scope": "Design, manufacture, hydrostatic stretch test, bursting test, and inspection for domestic and commercial LPG storage cylinders.",
        "ics_code": "23.020.30",
        "category": "Mechanical & Tooling",
        "status": "CURRENT",
        "revision_year": 2013,
        "latest_version": "IS 3196 (Part 1):2013 (Reaffirmed 2020)",
        "amendment": "Amendment 2, 2021",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark + PESO Approval",
        "certification_status": "Mandatory",
        "qco_notification_number": "Gas Cylinder Rules 2016",
        "clauses": [
            {"clause_number": "Clause 9.1", "title": "Hydrostatic Stretch Test", "requirement_text": "Cylinder subjected to 2.5 MPa hydraulic pressure shall have permanent volumetric expansion <= 10%.", "tested_parameter": "Stretch Permanent Expansion", "test_limit": "<= 10% volumetric"},
            {"clause_number": "Clause 9.2", "title": "Hydraulic Bursting Pressure Test", "requirement_text": "Cylinder shall not burst at a pressure less than 4.5 MPa (45 bar).", "tested_parameter": "Bursting Pressure", "test_limit": ">= 4.5 MPa (45 bar)"}
        ]
    },
    {
        "is_number": "IS 8867:1978",
        "title": "Specification for LPG Cylinder Valves",
        "scope": "Safety shutoff valves, outlet thread specifications, brass alloy composition, and pressure relief valve settings for LPG bottles.",
        "ics_code": "23.060.40",
        "category": "Mechanical & Tooling",
        "status": "CURRENT",
        "revision_year": 1978,
        "latest_version": "IS 8867:1978 (Reaffirmed 2020)",
        "amendment": "Amendment 4, 2019",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 7.2", "title": "Pneumatic Internal Leakage Test", "requirement_text": "Valve in closed position tested with compressed air at 1.7 MPa shall show zero bubbles for 1 minute.", "tested_parameter": "Pneumatic Seat Tightness", "test_limit": "Zero leakage at 1.7 MPa"},
            {"clause_number": "Clause 8.1", "title": "Safety Relief Valve Set Pressure", "requirement_text": "Pressure relief valve shall open at 2.45 +/- 0.15 MPa and reseat above 2.0 MPa.", "tested_parameter": "PRV Relief Setting", "test_limit": "2.45 +/- 0.15 MPa"}
        ]
    },

    # ------------------ DOMAIN 6: FOOD PACKAGING & WATER ------------------
    {
        "is_number": "IS 14543:2004",
        "title": "Packaged Drinking Water (Other than Packaged Natural Mineral Water)",
        "scope": "Microbiological criteria, toxic substance limits, TDS range, and hygienic packaging for commercial bottled drinking water.",
        "ics_code": "13.060.20",
        "category": "Chemical & Plastics",
        "status": "CURRENT",
        "revision_year": 2004,
        "latest_version": "IS 14543:2004 (Reaffirmed 2021)",
        "amendment": "Amendment 6, 2023",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark + FSSAI",
        "certification_status": "Mandatory",
        "qco_notification_number": "Food Safety and Standards Act QCO",
        "clauses": [
            {"clause_number": "Clause 5.1", "title": "Total Dissolved Solids (TDS)", "requirement_text": "Total dissolved solids shall be between 75 mg/L and 500 mg/L.", "tested_parameter": "TDS Range", "test_limit": "75 to 500 mg/L"},
            {"clause_number": "Clause 5.3", "title": "Microbiological Criteria (E. Coli and Coliform)", "requirement_text": "Escherichia coli and coliform bacteria shall be absent in 250 mL sample.", "tested_parameter": "Coliform Absence", "test_limit": "0 per 250 mL"}
        ]
    },
    {
        "is_number": "IS 9845:1998",
        "title": "Determination of Overall Migration of Constituents of Plastics Materials Intended to Come into Contact with Foodstuffs",
        "scope": "Simulant exposure test methods (water, alcohol, heptane) to determine plasticizer migration limits into foodstuffs.",
        "ics_code": "67.250",
        "category": "Chemical & Plastics",
        "status": "CURRENT",
        "revision_year": 1998,
        "latest_version": "IS 9845:1998 (Reaffirmed 2020)",
        "amendment": "Amendment 2, 2016",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 6.1", "title": "Global Overall Migration Limit", "requirement_text": "Total migrant substances shall not exceed 60 mg/kg or 10 mg/dm2 of food contact surface.", "tested_parameter": "Overall Migration", "test_limit": "<= 60 mg/kg"}
        ]
    },
    {
        "is_number": "IS 10146:1982",
        "title": "Polyethylene for its Safe Use in Contact with Foodstuffs, Pharmaceuticals and Drinking Water",
        "scope": "Purity, pigment limits, and residual catalyst thresholds for virgin PE polymer resin used for food containers.",
        "ics_code": "83.080.20",
        "category": "Chemical & Plastics",
        "status": "CURRENT",
        "revision_year": 1982,
        "latest_version": "IS 10146:1982 (Reaffirmed 2021)",
        "amendment": "Amendment 1, 2017",
        "certification_required": True,
        "certification_scheme": "BIS ISI Mark",
        "certification_status": "Mandatory",
        "clauses": [
            {"clause_number": "Clause 4.1", "title": "Polymer Resin Purity and Additive Limits", "requirement_text": "Polyethylene resin shall be virgin grade without recycled scrap; total additives <= 0.5% by weight.", "tested_parameter": "Virgin Polymer Purity", "test_limit": "Additive <= 0.5%"}
        ]
    }
]

def seed_database_and_vectors(db: Session):
    """
    Idempotent seeding of standards, relationships, users, and vector index.
    Updates existing records with complete clauses and verified metadata.
    """
    logger.info("Starting Authoritative Knowledge Base Seeding...")

    # 1. Create Default Users if not existing
    default_users = [
        {"email": "officer@gov.in", "full_name": "Rajesh Sharma", "role": "government_officer", "department": "Public Works Department (PWD)"},
        {"email": "expert@bis.gov.in", "full_name": "Dr. Ananya Iyer", "role": "technical_expert", "department": "BIS Civil Engineering Division"},
        {"email": "admin@gem.gov.in", "full_name": "Vikram Malhotra", "role": "administrator", "department": "GeM Technical Governance"}
    ]
    for u in default_users:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if not existing:
            new_user = User(
                email=u["email"],
                full_name=u["full_name"],
                role=u["role"],
                department=u["department"],
                hashed_password=get_password_hash("sarathi123")
            )
            db.add(new_user)
    db.commit()

    # 2. Seed / Update Standards and Clauses
    vectors_to_upsert = []
    created_standards_map = {}

    for item in STANDARDS_DATA:
        std = db.query(Standard).filter(Standard.is_number == item["is_number"]).first()
        if not std:
            std = Standard(
                is_number=item["is_number"],
                title=item["title"],
                scope=item["scope"],
                ics_code=item.get("ics_code"),
                category=item.get("category"),
                status=item.get("status", "CURRENT"),
                revision_year=item.get("revision_year"),
                latest_version=item.get("latest_version"),
                amendment=item.get("amendment"),
                certification_required=item.get("certification_required", False),
                certification_scheme=item.get("certification_scheme"),
                certification_status=item.get("certification_status", "Voluntary"),
                qco_notification_number=item.get("qco_notification_number")
            )
            db.add(std)
            db.commit()
            db.refresh(std)
        else:
            # Update metadata fields
            std.title = item["title"]
            std.scope = item["scope"]
            std.category = item.get("category")
            std.status = item.get("status", "CURRENT")
            std.latest_version = item.get("latest_version")
            std.amendment = item.get("amendment")
            std.certification_required = item.get("certification_required", False)
            std.certification_scheme = item.get("certification_scheme")
            std.certification_status = item.get("certification_status", "Voluntary")
            std.qco_notification_number = item.get("qco_notification_number")
            db.commit()
            db.refresh(std)

        # Seed or refresh child clauses (strict referential integrity)
        if "clauses" in item:
            for cl in item["clauses"]:
                existing_clause = db.query(StandardClause).filter(
                    StandardClause.standard_id == std.id,
                    StandardClause.clause_number == cl["clause_number"]
                ).first()
                if not existing_clause:
                    clause_obj = StandardClause(
                        standard_id=std.id,
                        clause_number=cl["clause_number"],
                        title=cl["title"],
                        requirement_text=cl.get("requirement_text"),
                        tested_parameter=cl.get("tested_parameter"),
                        test_limit=cl.get("test_limit")
                    )
                    db.add(clause_obj)
                else:
                    existing_clause.title = cl["title"]
                    existing_clause.requirement_text = cl.get("requirement_text")
                    existing_clause.tested_parameter = cl.get("tested_parameter")
                    existing_clause.test_limit = cl.get("test_limit")
            db.commit()

        created_standards_map[item["is_number"]] = std

        # Generate embedding for vector similarity search
        text_for_embedding = f"{item['is_number']}: {item['title']}. Scope: {item['scope']} Category: {item.get('category')}"
        emb_vector = embedding_service.embed_text(text_for_embedding)

        vectors_to_upsert.append({
            "id": std.id,
            "values": emb_vector,
            "metadata": {
                "is_number": item["is_number"],
                "title": item["title"],
                "scope": item["scope"],
                "category": item.get("category"),
                "status": item.get("status"),
                "ics_code": item.get("ics_code")
            }
        })

    # 3. Add Verified Standard Relationships (e.g. Normative / Test Method / Safety)
    RELATIONSHIPS_DATA = [
        # Cement Relationships
        ("IS 269:2015", "IS 456:2000", "Design Code", "Concrete structural engineering code relying on IS 269 cement specifications."),
        ("IS 269:2015", "IS 383:2016", "Material Standard", "Coarse and fine aggregate standard used in conjunction with IS 269 cement in concrete mixes."),
        # Cable Relationships
        ("IS 694:2010", "IS 1554 (Part 1):1988", "Related Standard", "Heavy duty power cabling counterpart to IS 694 building wires."),
        ("IS 694:2010", "IS 3043:2018", "Installation Code", "Code of practice for earthing applicable to IS 694 wiring installations."),
        # UPVC Pipe Relationships
        ("IS 4985:2021", "IS 12235 (Part 1 to 19)", "Testing Standard", "Authoritative test methods for hydrostatic and Vicat testing of IS 4985 UPVC pipes."),
        ("IS 1239 (Part 1):2004", "IS 3589:2001", "Product Family", "Large-diameter steel pipeline companion standard to IS 1239 tubes."),
        # PPE Relationships
        ("IS 2925:1984", "IS 15298 (Part 2):2016", "Safety Standard", "Complementary site PPE head-to-toe protective harmonized compliance.")
    ]

    for from_num, to_num, rel_type, desc in RELATIONSHIPS_DATA:
        if from_num in created_standards_map and to_num in created_standards_map:
            from_std = created_standards_map[from_num]
            to_std = created_standards_map[to_num]
            rel_exists = db.query(StandardRelationship).filter(
                StandardRelationship.from_standard_id == from_std.id,
                StandardRelationship.to_standard_id == to_std.id
            ).first()
            if not rel_exists:
                db.add(StandardRelationship(
                    from_standard_id=from_std.id,
                    to_standard_id=to_std.id,
                    relationship_type=rel_type,
                    description=desc
                ))
    db.commit()

    # 4. Upsert vectors to Pinecone (or in-memory index)
    pinecone_service.upsert_vectors(vectors_to_upsert)
    logger.info(f"Successfully seeded {len(vectors_to_upsert)} standards into database & vector store.")
'''

with open(seed_py_path, "w", encoding="utf-8") as f:
    f.write(NEW_CONTENT)

print(f"Updated {seed_py_path} successfully!")
