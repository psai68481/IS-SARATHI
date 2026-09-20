// Multi-Case Mock Dataset for IS-SARATHI (UI Showcase & Static Deployment)

export const TENDER_CASES = {
  helmet: {
    id: "helmet",
    title: "Construction Worker Industrial Helmet (<250g)",
    department: "Public Works Department (PWD)",
    sampleFile: "Tender_Notice_PWD_Helmets_2024.pdf",
    fileType: "PDF",
    tenderQuery: "We need industrial helmets for construction workers with impact resistance and electrical insulation ultra weight less than 250",
    
    extractedRequirements: [
      { field: "Product Type", value: "Industrial Safety Helmet", category: "Classification", confidence: 98 },
      { field: "Impact Resistance", value: "Required (50J Drop Test)", category: "Mechanical Safety", confidence: 96 },
      { field: "Electrical Insulation", value: "Required (10kV Dielectric)", category: "Electrical Safety", confidence: 94 },
      { field: "Weight Limit", value: "< 250g (Ultra-Lightweight)", category: "Physical Ergonomics", confidence: 95 },
      { field: "Operating Temp", value: "-10°C to 50°C", category: "Environmental", confidence: 90 }
    ],

    recommendations: [
      {
        isNumber: "IS 2925:1984",
        title: "Industrial Safety Helmets - Specification",
        type: "Primary Standard",
        confidence: 91,
        status: "Current",
        latestVersion: "IS 2925:1984 (Reaffirmed 2020)",
        amendment: "Amendment 2, 2019 - updated impact test method",
        certification: {
          required: true,
          scheme: "BIS ISI Mark",
          status: "Mandatory"
        },
        category: "Personal Protective Equipment",
        description: "Specifies requirements for materials, construction, finish, and performance of industrial safety helmets intended to provide head protection against falling objects and electrical hazards.",
        keyClauses: [
          { clause: "Clause 5.2", title: "Shock Absorption Test (Impact Energy: 50 Joules)" },
          { clause: "Clause 6.1", title: "Electrical Resistance Test (Proof Voltage 10kV)" },
          { clause: "Clause 4.3", title: "Shell Weight Limit (Nominal 340g - 420g)" },
          { clause: "Clause 7.3", title: "Temperature Conditioning (-10°C to +50°C)" }
        ],
        relatedStandards: [
          {
            type: "Test Method",
            isNumber: "IS 2925 (Part 2)",
            title: "Methods of Test for Safety Helmets",
            description: "Details drop-tower test protocols, calibration of accelerometers, and dummy headform compliance."
          },
          {
            type: "Safety Standard",
            isNumber: "IS 15298",
            title: "Personal Protective Equipment - Safety Standard",
            description: "Harmonized standards for ergonomics, testing protocols, and occupational safety equipment classification."
          },
          {
            type: "Material Standard",
            isNumber: "IS 7016",
            title: "Methods of Test for Plastics Used in Helmets",
            description: "High-density polyethylene (HDPE) and polycarbonate polymer testing for UV resistance and degradation."
          }
        ],
        coverageMap: [
          {
            requirement: "Impact Resistance",
            evidence: "Clause 5.2",
            detail: "Transmitted force shall not exceed 5.0 kN when subjected to 50 J impact energy.",
            covered: true
          },
          {
            requirement: "Electrical Insulation",
            evidence: "Clause 6.1",
            detail: "Leakage current not exceeding 1.2 mA at 10,000 V AC (50 Hz).",
            covered: true
          },
          {
            requirement: "Weight Limit (< 250g)",
            evidence: "Clause 4.3",
            detail: "Standard specifies nominal weight 340g - 420g. Requested <250g is below certified structural threshold.",
            covered: false
          },
          {
            requirement: "Operating Temperature",
            evidence: "Clause 7.3",
            detail: "Performance maintained post 4h conditioning at -10°C and +50°C.",
            covered: true
          },
          {
            requirement: "Installation Requirement",
            evidence: null,
            detail: "Tender mentions site assembly guidelines, not covered under PPE standard scope.",
            covered: false
          }
        ],
        whyNotAlternatives: [
          {
            isNumber: "IS 4770",
            title: "Rubber Gloves for Electrical Purposes",
            confidence: 67,
            reason: "Covers rubber gloves, not helmets - different product scope and safety zone."
          },
          {
            isNumber: "IS 4151",
            title: "Protective Helmets for Two-Wheeler Motorcyclists",
            confidence: 58,
            reason: "Automotive vehicular helmet specification; lacks industrial high-voltage electrical insulation."
          },
          {
            isNumber: "IS 9562",
            title: "Non-Metallic Safety Helmets for Mining",
            confidence: 72,
            reason: "Mining standard excludes surface construction lightweight shell ergonomic profiles."
          }
        ]
      },
      {
        isNumber: "IS 15298 (Part 2)",
        title: "Personal Protective Equipment - Head Protection",
        type: "Related Standard",
        confidence: 78,
        status: "Current",
        latestVersion: "2019",
        amendment: "None",
        certification: {
          required: false,
          scheme: "N/A",
          status: "Voluntary"
        },
        category: "Personal Protective Equipment",
        description: "Covers general head protection apparatus criteria conforming with ISO alignment for international export compliance.",
        keyClauses: [
          { clause: "Clause 4.1", title: "General Shell Ergonomics" },
          { clause: "Clause 6.3", title: "Lateral Deformation Testing" }
        ],
        relatedStandards: [],
        coverageMap: [],
        whyNotAlternatives: []
      }
    ],

    conflicts: [
      {
        tenderSpec: "Weight limit: < 250 grams total weight (ultra-light)",
        standardSpec: "IS 2925 Clause 4.3 specifies nominal weight 340g - 420g to ensure structural shock absorption",
        severity: "Warning - Human review recommended",
        impact: "Ultra-lightweight shells below 250g fail the 50 Joule impact penetration test unless carbon-fiber reinforced and specifically type-tested under BIS special certification."
      },
      {
        tenderSpec: "Operating temperature: 100°C continuous",
        standardSpec: "IS 2925 maximum rated: 80°C (Clause 7.3 specifies -10°C to +50°C standard, 80°C special grade)",
        severity: "Warning - Human review recommended",
        impact: "Polymer breakdown risk under sustained 100°C heat exposure without specialized aerospace composite formulation."
      }
    ],

    gaps: [
      "Testing method for chin-strap durability and retention release force not specified in tender document.",
      "Environmental exposure rating (prolonged UV degradation / solar UV index > 8) not mentioned in baseline specs."
    ],

    historicalDecisions: [
      {
        caseId: "PROC-2024-0231",
        title: "High-Voltage Thermal Power Plant Headgear",
        department: "NTPC Procurement Division",
        date: "2024-03-14",
        aiRecommendation: "IS 2925:1984 (91%)",
        humanDecision: "IS 15298 (Part 2) (73%)",
        reason: "Application-specific requirement - high-voltage site required IEC/ISO aligned dielectric testing beyond 15kV.",
        validationStatus: "Validated"
      },
      {
        caseId: "PROC-2024-0189",
        title: "Highway Infrastructure Worker Protective Kit",
        department: "NHAI Regional Office",
        date: "2024-02-28",
        aiRecommendation: "IS 2925:1984 (94%)",
        humanDecision: "IS 2925:1984 (94%)",
        reason: "Standard highway civil construction specs; direct match with Clause 5.2 impact rating.",
        validationStatus: "Validated"
      }
    ]
  },

  cable: {
    id: "cable",
    title: "Fire-Resistant Building Wiring (FRLS)",
    department: "Health Infrastructure Board",
    sampleFile: "Hospital_FRLS_Wiring_Specs.pdf",
    fileType: "PDF",
    tenderQuery: "Procurement of low-smoke zero-halogen (FRLS) copper wiring cables for commercial hospital buildings with 1100V rating",
    
    extractedRequirements: [
      { field: "Product Type", value: "Low-Smoke FRLS Copper Cable", category: "Classification", confidence: 97 },
      { field: "Voltage Grade", value: "1100V Rated Working Voltage", category: "Electrical Rating", confidence: 95 },
      { field: "Fire Property", value: "Zero Halogen Acid Gas Emission (<0.5%)", category: "Fire Safety", confidence: 94 },
      { field: "Conductor Material", value: "High-Purity Electrolytic Copper", category: "Material Grade", confidence: 96 },
      { field: "Oxygen Index", value: "Minimum 29% Critical Oxygen Index", category: "Flammability", confidence: 92 }
    ],

    recommendations: [
      {
        isNumber: "IS 694:2010",
        title: "PVC Insulated Cables for Working Voltages up to 1100 V - Specification",
        type: "Primary Standard",
        confidence: 94,
        status: "Current",
        latestVersion: "IS 694:2010 (Reaffirmed 2021)",
        amendment: "Amendment 3, 2020 - FRLS compound testing",
        certification: {
          required: true,
          scheme: "BIS ISI Mark",
          status: "Mandatory"
        },
        category: "Electrical Cables & Conductors",
        description: "Covers single core and multicore unsheathed and sheathed electric cables with copper conductors for electric power and lighting up to 1100 Volts.",
        keyClauses: [
          { clause: "Clause 5.1", title: "Voltage Grade & Insulation Resistance Test" },
          { clause: "Clause 6.2", title: "Conductor Resistance & Electrolytic Purity" },
          { clause: "Clause 14.3", title: "Flame Retardant Low Smoke (FRLS) Index" },
          { clause: "Clause 15.1", title: "Smoke Density & Acid Gas Generation" }
        ],
        relatedStandards: [
          {
            type: "Test Method",
            isNumber: "IS 10810 (Part 58)",
            title: "Methods of Test for Cables - Oxygen Index Test",
            description: "Standardized test procedure to evaluate minimum oxygen concentration for polymer combustion."
          },
          {
            type: "Safety Standard",
            isNumber: "IS 1554",
            title: "Heavy Duty Armoured Power Cables",
            description: "Harmonized criteria for sub-main underground distribution and switchboard risers."
          },
          {
            type: "Material Standard",
            isNumber: "IS 8130",
            title: "Conductors for Insulated Electric Cables",
            description: "Specifies conductivity and tensile strength parameters for annealed copper wire."
          }
        ],
        coverageMap: [
          {
            requirement: "Voltage Grade (1100V)",
            evidence: "Clause 5.1",
            detail: "Tested for 3.0 kV AC spark test and dielectric withstand at 1100V continuous.",
            covered: true
          },
          {
            requirement: "Conductor Material",
            evidence: "Clause 6.2",
            detail: "Class 1 & 2 high conductivity annealed copper conforming to IS 8130.",
            covered: true
          },
          {
            requirement: "Fire Property (FRLS)",
            evidence: "Clause 14.3",
            detail: "Halogen acid gas emission restricted to <= 0.5% by weight during thermal decomposition.",
            covered: true
          },
          {
            requirement: "Oxygen Index (>=29%)",
            evidence: "Clause 15.1",
            detail: "Oxygen index shall not be less than 29 when tested per IS 10810 Part 58.",
            covered: true
          },
          {
            requirement: "Conduit Pulling Guide",
            evidence: null,
            detail: "Contractual installation guideline; not governed by product manufacturing standard.",
            covered: false
          }
        ],
        whyNotAlternatives: [
          {
            isNumber: "IS 1554 (Part 1)",
            title: "PVC Armoured Heavy Power Cables",
            confidence: 71,
            reason: "Armoured underground feeder cable; excessive outer diameter and weight for internal conduit branch wiring."
          },
          {
            isNumber: "IS 9968",
            title: "Elastomer Insulated Cables for Mines",
            confidence: 62,
            reason: "Heavy rubber sheath cable for wet mining machinery; not suitable for hospital dry wall cavities."
          }
        ]
      },
      {
        isNumber: "IS 7098 (Part 1)",
        title: "Cross-linked Polyethylene (XLPE) Insulated Cables",
        type: "Related Standard",
        confidence: 82,
        status: "Current",
        latestVersion: "2019",
        amendment: "None",
        certification: {
          required: false,
          scheme: "BIS ISI",
          status: "Voluntary"
        },
        category: "Electrical Cables",
        description: "Alternative high thermal-capacity XLPE insulation standard for heavy feeder trunks.",
        keyClauses: [
          { clause: "Clause 3.1", title: "Thermal Aging" }
        ],
        relatedStandards: [],
        coverageMap: [],
        whyNotAlternatives: []
      }
    ],

    conflicts: [
      {
        tenderSpec: "Halogen gas emission: 0.0% absolute zero acid release",
        standardSpec: "IS 694 Appendix G specifies maximum permissible halogen acid gas <= 0.5% by weight",
        severity: "Warning - Human review recommended",
        impact: "Zero percent halogen release (0.00%) is chemically impossible for standard PVC; requires specialized LSZH polymer compound certification."
      }
    ],

    gaps: [
      "Tender does not specify conductor Class (Class 1 solid vs Class 2 stranded vs Class 5 flexible).",
      "Color-coding sequence for 3-phase hospital emergency power circuits not mentioned in BoQ."
    ],

    historicalDecisions: [
      {
        caseId: "PROC-2024-0312",
        title: "AIIMS Medical College Hospital Wiring",
        department: "Ministry of Health & Family Welfare",
        date: "2024-04-18",
        aiRecommendation: "IS 694:2010 (94%)",
        humanDecision: "IS 694:2010 (94%)",
        reason: "Standard hospital tender; compliant with Fire Safety QCO 2023.",
        validationStatus: "Validated"
      }
    ]
  },

  pipe: {
    id: "pipe",
    title: "Potable Water UPVC Pressure Pipes (Class 3)",
    department: "State Jal Nigam Water Board",
    sampleFile: "UPVC_Potable_Water_Pipes_Tender.pdf",
    fileType: "PDF",
    tenderQuery: "Procurement of high pressure unplasticized UPVC pipes class 3 for municipal potable drinking water distribution network with lead-free certification",
    
    extractedRequirements: [
      { field: "Product Type", value: "UPVC Pressure Pipe", category: "Classification", confidence: 99 },
      { field: "Application", value: "Potable Drinking Water Supply", category: "Sanitary", confidence: 97 },
      { field: "Pressure Rating", value: "Class 3 (0.6 MPa / 6 kgf/cm²)", category: "Mechanical Rating", confidence: 95 },
      { field: "Chemical Safety", value: "Lead-Free Heavy Metal Stabilizer", category: "Health & Toxicological", confidence: 96 },
      { field: "Nominal Diameter", value: "110mm to 200mm Outer Diameter", category: "Dimensional", confidence: 93 }
    ],

    recommendations: [
      {
        isNumber: "IS 4985:2021",
        title: "Unplasticized PVC Pipes for Potable Water Supplies - Specification",
        type: "Primary Standard",
        confidence: 96,
        status: "Current",
        latestVersion: "IS 4985:2021 (Fifth Revision)",
        amendment: "Gazette Notification 2022 - Lead Free Mandatory",
        certification: {
          required: true,
          scheme: "BIS ISI Mark",
          status: "Mandatory"
        },
        category: "Pipes, Fittings & Water Sanitation",
        description: "Specifies requirements for unplasticized polyvinyl chloride (uPVC) pipes intended for municipal potable water supply and agricultural piping systems.",
        keyClauses: [
          { clause: "Clause 5.3", title: "Heavy Metal & Lead Extraction Limits (< 0.05 mg/L)" },
          { clause: "Clause 8.1", title: "Internal Hydrostatic Pressure Test" },
          { clause: "Clause 7.2", title: "Opacity & Visual Wall Uniformity" },
          { clause: "Clause 8.3", title: "Longitudinal Reversion Test (Hot Air Oven)" }
        ],
        relatedStandards: [
          {
            type: "Test Method",
            isNumber: "IS 12235 (Part 1)",
            title: "Methods of Test for UPVC Pipes - Measurement of Dimensions",
            description: "Procedures to measure nominal outside diameter, wall thickness, and ovality."
          },
          {
            type: "Safety Standard",
            isNumber: "IS 10500",
            title: "Drinking Water - Specification",
            description: "Indian national water quality standard governing maximum allowable toxic limits."
          },
          {
            type: "Material Standard",
            isNumber: "IS 10124",
            title: "Fabricated PVC Fittings for Potable Water",
            description: "Jointing couplers, elbows, and flanged connections for IS 4985 pipes."
          }
        ],
        coverageMap: [
          {
            requirement: "Lead-Free Chemical Safety",
            evidence: "Clause 5.3",
            detail: "Maximum lead extraction limit must not exceed 0.05 ppm by weight per test protocol.",
            covered: true
          },
          {
            requirement: "Pressure Rating (Class 3)",
            evidence: "Clause 8.1",
            detail: "Tested to withstand 2.16 MPa hydrostatic pressure test for 1 hour at 27°C.",
            covered: true
          },
          {
            requirement: "Potable Application",
            evidence: "Clause 7.2",
            detail: "Opacity percentage shall exceed 0.2% to prevent algal growth in drinking water.",
            covered: true
          },
          {
            requirement: "Longitudinal Stability",
            evidence: "Clause 8.3",
            detail: "Reversion shall not exceed 5% after immersion in hot air bath at 150°C.",
            covered: true
          },
          {
            requirement: "Trench Excavation",
            evidence: null,
            detail: "Civil works guideline; outside scope of pipe product specification.",
            covered: false
          }
        ],
        whyNotAlternatives: [
          {
            isNumber: "IS 12818",
            title: "UPVC Pipes for Deep Tubewell Casing",
            confidence: 64,
            reason: "Slotted rib casing pipes for underground aquifers; cannot sustain pressurized municipal distribution."
          },
          {
            isNumber: "IS 13592",
            title: "UPVC Pipes for Soil and Waste Discharge",
            confidence: 55,
            reason: "Gravity flow drainage pipe; not pressure rated and contains stabilizers not approved for drinking water."
          }
        ]
      }
    ],

    conflicts: [
      {
        tenderSpec: "Operating pressure: 1.6 MPa (Class 5) with thin wall 2.2mm",
        standardSpec: "IS 4985 Table 2 requires minimum wall thickness 4.2mm for Class 5 pipes",
        severity: "Warning - Human review recommended",
        impact: "A 2.2mm wall cannot withstand 1.6 MPa surge pressure and will burst under water hammer conditions."
      }
    ],

    gaps: [
      "Pipe socket type (Solvent Cement Joint vs Elastomeric Sealing Ring Socket) not specified.",
      "Effective laying length per pipe unit (3m vs 6m) omitted in BoQ schedule."
    ],

    historicalDecisions: [
      {
        caseId: "PROC-2024-0105",
        title: "Rural Drinking Water Mission Pipeline",
        department: "Jal Jeevan Mission (JJM)",
        date: "2024-01-22",
        aiRecommendation: "IS 4985:2021 (96%)",
        humanDecision: "IS 4985:2021 (96%)",
        reason: "Mandatory lead-free UPVC pipe QCO compliance verified.",
        validationStatus: "Validated"
      }
    ]
  }
};

// Global default mock data pointing to the primary helmet case
export const GLOBAL_MOCK_DATA = {
  ...TENDER_CASES.helmet,

  stats: {
    totalTendersAnalyzed: 47,
    avgConfidence: 84,
    standardsInKB: 62,
    pendingReviews: 5,
    accuracyRate: 94.2,
    avgProcessingTime: "1.4s"
  },

  confidenceDistribution: [
    { range: "90-100% (High)", count: 24, fill: "#10B981" },
    { range: "80-89% (Optimal)", count: 14, fill: "#028090" },
    { range: "70-79% (Moderate)", count: 6, fill: "#F59E0B" },
    { range: "< 70% (Review Req.)", count: 3, fill: "#EF4444" }
  ],

  domainBreakdown: [
    { domain: "PPE & Occupational Safety", count: 18, share: "29%" },
    { domain: "Electrical & Electronics", count: 15, share: "24%" },
    { domain: "Civil & Construction Materials", count: 14, share: "23%" },
    { domain: "Pipes & Water Sanitation", count: 9, share: "15%" },
    { domain: "Chemical & Plastics", count: 6, share: "9%" }
  ],

  tenderPresets: [
    {
      id: "helmet",
      title: "1. Construction Worker Helmets (<250g)",
      query: TENDER_CASES.helmet.tenderQuery,
      department: TENDER_CASES.helmet.department,
      sampleFile: "Tender_Notice_PWD_Helmets_2024.pdf",
      fileType: "PDF"
    },
    {
      id: "cable",
      title: "2. Fire-Resistant Building Cables (FRLS)",
      query: TENDER_CASES.cable.tenderQuery,
      department: TENDER_CASES.cable.department,
      sampleFile: "Hospital_FRLS_Wiring_Specs.pdf",
      fileType: "PDF"
    },
    {
      id: "pipe",
      title: "3. Potable Water UPVC Pressure Pipes",
      query: TENDER_CASES.pipe.tenderQuery,
      department: TENDER_CASES.pipe.department,
      sampleFile: "UPVC_Potable_Water_Pipes_Tender.pdf",
      fileType: "PDF"
    }
  ],

  ocrSamples: [
    {
      id: "ocr-helmet-pdf",
      name: "Tender_Notice_PWD_Helmets_2024.pdf",
      type: "PDF",
      size: "248 KB",
      presetId: "helmet",
      department: "Public Works Dept (PWD)",
      extractedText: TENDER_CASES.helmet.tenderQuery,
      previewSnippet: "TENDER NOTICE NO: PWD/ELECT/2026/089\nItem 01: Industrial Safety Helmets for construction labor\nKey Specs: Impact resistance (50J drop test), Electrical insulation (proof voltage), Ultra-weight requirement: Less than 250 grams total weight for extended overhead shift wear."
    },
    {
      id: "ocr-helmet-png",
      name: "Scanned_BoQ_Helmets_Spec.png",
      type: "PNG",
      size: "612 KB",
      presetId: "helmet",
      department: "Central Vigilance Division",
      extractedText: TENDER_CASES.helmet.tenderQuery,
      previewSnippet: "[SCANNED DOCUMENT OCR RECOGNIZED]\nSection B.2: Personnel Protective Gear (Head Protection)\nSpecifications: Impact resistance shock absorption; Dielectric electrical resistance; Ultra-lightweight shell under 250 grams."
    },
    {
      id: "ocr-cable-pdf",
      name: "Hospital_FRLS_Wiring_Specs.pdf",
      type: "PDF",
      size: "340 KB",
      presetId: "cable",
      department: "Health Infrastructure Board",
      extractedText: TENDER_CASES.cable.tenderQuery,
      previewSnippet: "HOSPITAL ELECTRICAL INFRASTRUCTURE SPECIFICATION\nScope: Fire Retardant Low Smoke (FRLS) multi-strand copper cables 1100V rated with zero halogen acid gas release."
    },
    {
      id: "ocr-pipe-png",
      name: "UPVC_Potable_Water_Pipes.png",
      type: "PNG",
      size: "420 KB",
      presetId: "pipe",
      department: "State Jal Nigam Board",
      extractedText: TENDER_CASES.pipe.tenderQuery,
      previewSnippet: "[SCANNED DRAWING & SPECIFICATION]\nMunicipal Potable Drinking Water Distribution: UPVC pressure pipes Class 3 with lead-free certification."
    }
  ]
};
