// Global mock data structure for IS-SARATHI (UI Showcase & Static Deployment)

export const GLOBAL_MOCK_DATA = {
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
        { clause: "Clause 4.3", title: "Shell Weight & Thickness Limit (Nominal 340g - 420g)" },
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
          reason: "Automotive vehicular helmet specification; lacks industrial high-voltage electrical insulation and side ventilation requirements."
        },
        {
          isNumber: "IS 9562",
          title: "Non-Metallic Safety Helmets for Mining",
          confidence: 72,
          reason: "Mining standard excludes surface construction lightweight shell ergonomic profiles required in tender."
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
    },
    {
      isNumber: "IS 8521 (Part 1)",
      title: "Industrial Safety Face Shields and Visor Attachments",
      type: "Related Standard",
      confidence: 71,
      status: "Current",
      latestVersion: "2018",
      amendment: "Amendment 1, 2021",
      certification: {
        required: false,
        scheme: "BIS Voluntary",
        status: "Voluntary"
      },
      category: "Personal Protective Equipment",
      description: "Optional accessory standard for face shield mounts compatible with IS 2925 helmet brim slots.",
      keyClauses: [
        { clause: "Clause 3.2", title: "Optical Clarity and Impact" }
      ],
      relatedStandards: [],
      coverageMap: [],
      whyNotAlternatives: []
    }
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
    },
    {
      caseId: "PROC-2024-0142",
      title: "Metro Tunnel Underground Excavation Helmets",
      department: "DMRC Safety Wing",
      date: "2024-01-19",
      aiRecommendation: "IS 2925:1984 (88%)",
      humanDecision: "IS 9562 (Mining Grade) (85%)",
      reason: "Underground tunnel bore environment deemed equivalent to underground coal mining dampness.",
      validationStatus: "Validated"
    },
    {
      caseId: "PROC-2023-0902",
      title: "Municipal Water Supply Pipeline Maintenance",
      department: "Jal Board Technical Cell",
      date: "2023-11-05",
      aiRecommendation: "IS 2925:1984 (92%)",
      humanDecision: "Pending Officer Verification",
      reason: "Awaiting clarification on chemical splash resistance addendum.",
      validationStatus: "Unverified"
    },
    {
      caseId: "PROC-2023-0784",
      title: "Solar Substation Maintenance Crew Gear",
      department: "SECI Engineering Unit",
      date: "2023-09-12",
      aiRecommendation: "IS 4770 (Rubber PPE)",
      humanDecision: "IS 2925 + IS 4770 (Combo)",
      reason: "Tender mixed helmet and glove requirements; rejected single-standard classification.",
      validationStatus: "Rejected"
    }
  ],

  gaps: [
    "Testing method for chin-strap durability and retention release force not specified in tender document.",
    "Environmental exposure rating (prolonged UV degradation / solar UV index > 8) not mentioned in baseline specs."
  ],

  conflicts: [
    {
      tenderSpec: "Weight limit: < 250 grams total weight (ultra-light)",
      standardSpec: "IS 2925 Clause 4.3 specifies nominal weight 340g - 420g to ensure structural shock absorption",
      severity: "Warning - Human review recommended",
      impact: "Ultra-lightweight shells below 250g may fail the 50 Joule impact penetration test unless carbon-fiber reinforced and specifically type-tested under BIS special certification."
    },
    {
      tenderSpec: "Operating temperature: 100°C continuous",
      standardSpec: "IS 2925 maximum rated: 80°C (Clause 7.3 specifies -10°C to +50°C standard, 80°C special grade)",
      severity: "Warning - Human review recommended",
      impact: "Polymer breakdown risk under sustained 100°C heat exposure without specialized aerospace composite formulation."
    }
  ],

  // Dashboard KPI Overview Data
  stats: {
    totalTendersAnalyzed: 47,
    avgConfidence: 84,
    standardsInKB: 62,
    pendingReviews: 5,
    accuracyRate: 94.2,
    avgProcessingTime: "1.4s"
  },

  // Chart: Confidence distribution across recent recommendations
  confidenceDistribution: [
    { range: "90-100% (High)", count: 24, fill: "#10B981" },
    { range: "80-89% (Optimal)", count: 14, fill: "#028090" },
    { range: "70-79% (Moderate)", count: 6, fill: "#F59E0B" },
    { range: "< 70% (Review Req.)", count: 3, fill: "#EF4444" }
  ],

  // Chart: Domain breakdown in Knowledge Base
  domainBreakdown: [
    { domain: "PPE & Occupational Safety", count: 18, share: "29%" },
    { domain: "Electrical & Electronics", count: 15, share: "24%" },
    { domain: "Civil & Construction Materials", count: 14, share: "23%" },
    { domain: "Mechanical & Tooling", count: 9, share: "15%" },
    { domain: "Chemical & Plastics", count: 6, share: "9%" }
  ],

  // Alternative tender presets for testing/demo
  tenderPresets: [
    {
      id: "helmet",
      title: "Construction Worker Industrial Helmet (<250g)",
      query: "We need industrial helmets for construction workers with impact resistance and electrical insulation ultra weight less than 250",
      department: "Public Works Department (PWD)",
      sampleFile: "Tender_Doc_PWD_Helmets_2024.pdf",
      fileType: "PDF"
    },
    {
      id: "cable",
      title: "Fire-Resistant Building Wiring",
      query: "Procurement of low-smoke zero-halogen (FRLS) copper wiring cables for commercial hospital buildings with 1100V rating",
      department: "Health Infrastructure Board",
      sampleFile: "Hospital_FRLS_Wiring_Specs.png",
      fileType: "PNG"
    },
    {
      id: "transformer",
      title: "33kV Power Distribution Transformer",
      query: "Supply and commissioning of 33/11kV oil-immersed power distribution transformers with energy efficiency Level-2 certification",
      department: "State Electricity Transmission Corp",
      sampleFile: "Substation_Transformer_Tender.pdf",
      fileType: "PDF"
    }
  ],

  // Sample OCR Scanned Documents for quick 1-click demonstration
  ocrSamples: [
    {
      id: "ocr-helmet-pdf",
      name: "Tender_Notice_PWD_Helmets_2024.pdf",
      type: "PDF",
      size: "248 KB",
      pages: "1 Page (Vector & Scanned Text)",
      department: "Public Works Dept, Govt of India",
      date: "10-Sept-2026",
      extractedText: "We need industrial helmets for construction workers with impact resistance and electrical insulation ultra weight less than 250",
      previewSnippet: "TENDER NOTICE NO: PWD/ELECT/2026/089\nItem 01: Industrial Safety Helmets for construction labor\nKey Specs: Impact resistance (50J drop test), Electrical insulation (proof voltage), Ultra-weight requirement: Less than 250 grams total weight for extended overhead shift wear."
    },
    {
      id: "ocr-helmet-png",
      name: "Scanned_BoQ_Helmets_Spec.png",
      type: "PNG",
      size: "612 KB",
      dimensions: "1920 x 1080 px",
      department: "Central Vigilance & Safety Division",
      date: "08-Sept-2026",
      extractedText: "We need industrial helmets for construction workers with impact resistance and electrical insulation ultra weight less than 250",
      previewSnippet: "[SCANNED DOCUMENT OCR RECOGNIZED]\nSection B.2: Personnel Protective Gear (Head Protection)\nSpecifications: Impact resistance shock absorption certified; High voltage electrical resistance; Ultra-lightweight shell under 250 grams."
    },
    {
      id: "ocr-pipe-pdf",
      name: "UPVC_Potable_Water_Pipes_Tender.pdf",
      type: "PDF",
      size: "380 KB",
      pages: "2 Pages",
      department: "State Jal Nigam Board",
      date: "04-Sept-2026",
      extractedText: "Procurement of high pressure unplasticized UPVC pipes class 3 for municipal potable drinking water distribution network with lead-free certification",
      previewSnippet: "JAL NIGAM MUNICIPAL WATER SUPPLY TENDER\nScope: Supply of UPVC pressure pipes for potable drinking water supply."
    }
  ]
};
