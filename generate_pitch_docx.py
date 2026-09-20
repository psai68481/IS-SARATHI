import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()

# Page setup
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Color constants
COLOR_NAVY = RGBColor(0x1E, 0x27, 0x61)
COLOR_TEAL = RGBColor(0x02, 0x80, 0x90)
COLOR_GRAY = RGBColor(0x55, 0x5F, 0x6B)
COLOR_BLACK = RGBColor(0x1A, 0x1A, 0x1A)

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

# Title & Header
p_title = doc.add_paragraph()
r_title = p_title.add_run("IS-SARATHI : SIH 2026 Pitch & Live Demo Guide")
r_title.font.name = "Calibri"
r_title.font.size = Pt(24)
r_title.font.bold = True
r_title.font.color.rgb = COLOR_NAVY
p_title.paragraph_format.space_after = Pt(2)

p_sub = doc.add_paragraph()
r_sub = p_sub.add_run("AI-Powered Indian Standards Recommendation Dashboard for Public Procurement")
r_sub.font.name = "Calibri"
r_sub.font.size = Pt(13)
r_sub.font.bold = True
r_sub.font.color.rgb = COLOR_TEAL
p_sub.paragraph_format.space_after = Pt(8)

p_meta = doc.add_paragraph()
r_meta = p_meta.add_run("Live Prototype: https://is-sarathi.vercel.app  |  Team: Team Sarathi  |  Smart India Hackathon 2026")
r_meta.font.name = "Calibri"
r_meta.font.size = Pt(10)
r_meta.font.italic = True
r_meta.font.color.rgb = COLOR_GRAY
p_meta.paragraph_format.space_after = Pt(14)

# Section Divider Line
p_hr = doc.add_paragraph()
p_hr_run = p_hr.add_run("―" * 58)
p_hr_run.font.color.rgb = COLOR_TEAL
p_hr.paragraph_format.space_after = Pt(12)

# 1. Executive Summary
h1 = doc.add_heading("1. Executive Summary & Problem Context", level=1)
h1.style.font.color.rgb = COLOR_NAVY

p1 = doc.add_paragraph(
    "Public procurement in India exceeds ₹10 Lakh Crore annually across GeM and CPPP portals. "
    "A major bottleneck is the manual alignment of tender requirements with over 22,000 Bureau of Indian Standards (BIS) documents. "
    "Mismatched standards lead to audit objections, procurement delays, and safety violations. "
    "IS-SARATHI is an intelligent recommendation engine that ingests tender specifications, extracts critical parameters, "
    "identifies primary and harmonized Indian Standards, cross-verifies clauses, detects non-compliance conflicts, "
    "and explains disqualifications with 100% audit transparency."
)
p1.paragraph_format.space_after = Pt(12)

# 2. Live Website Demonstration Script (Screen-by-Screen)
h2 = doc.add_heading("2. Live Website Demonstration Script (Step-by-Step)", level=1)
h2.style.font.color.rgb = COLOR_NAVY

p_info = doc.add_paragraph("Open https://is-sarathi.vercel.app on the projector and press F11 for clean Fullscreen Mode. Follow these 9 steps:")
p_info.paragraph_format.space_after = Pt(10)

screens = [
    (
        "Screen 1: Top Bar & Dashboard Tab",
        "Keep the browser on the Dashboard overview.",
        "Respected Judges, welcome to IS-SARATHI — our AI-powered Indian Standards recommendation dashboard built for GeM and procurement committees. Right at the top is our KPI overview showing 47 tenders analyzed with an 84% average confidence match and a live confidence distribution chart powered by our clause scoring model."
    ),
    (
        "Screen 2: Tender Analysis Tab",
        "Click on 'Tender Analysis' in the left sidebar and click 'Analyze Specification'.",
        "Here, an officer inputs tender text: 'Industrial helmets for construction workers with impact resistance and electrical insulation'. When we click 'Analyze Specification', our NLP engine tokenizes the document and extracts 4 core parameters: Product Type, Impact Resistance, Electrical Insulation, and Operating Temperature with high confidence."
    ),
    (
        "Screen 3: AI Recommendations Tab",
        "Click on 'AI Recommendations' in the left sidebar.",
        "The system recommends IS 2925:1984 as the Primary Standard with a 91% AI confidence match on our radial meter. Crucially, it highlights that BIS ISI Mark is MANDATORY under latest Quality Control Orders (QCO) to prevent illegal non-compliant procurement, while also displaying reaffirmation years and secondary harmonized standards like IS 15298."
    ),
    (
        "Screen 4: Related Standards Tab",
        "Click on 'Related Standards' in the left sidebar and click on any leaf node.",
        "Procurement never relies on a single standard in isolation. IS-SARATHI generates an interactive Dependency Graph linking the helmet specification to IS 2925 Part 2 (Test Methods), IS 15298 (Safety), and IS 7016 (Plastics Material Testing), providing clear audit notes for vendor test certificates."
    ),
    (
        "Screen 5: Requirement Coverage Tab",
        "Click on 'Requirement Coverage' in the left sidebar.",
        "Instead of vague keyword matches, we provide clause-by-clause legal evidence: Impact Resistance is proven under Clause 5.2 (50J drop test), Electrical Insulation under Clause 6.1 (10kV proof voltage), and Operating Temp under Clause 7.3, providing an airtight compliance score of 75%."
    ),
    (
        "Screen 6: Conflicts & Gaps Tab",
        "Click on 'Conflicts & Gaps' in the left sidebar.",
        "Here is our automated safety guardrail: Look at Conflict #1 — the tender requested 100°C continuous temperature, but IS 2925 maximum rated envelope is 80°C. The system flags a Red Warning for Human Review, preventing procurement of substandard gear before tender publication!"
    ),
    (
        "Screen 7: 'Why Not?' Disqualification Tab",
        "Click on 'Why Not?' in the left sidebar.",
        "To ensure zero black-box AI, our 'Why Not?' tab explains why other candidates were rejected: IS 4770 was rejected because it covers rubber electrical gloves, not headgear, while IS 4151 is for motorcyclists. Every disqualified alternative has a clear, explainable rationale."
    ),
    (
        "Screen 8: Historical Decisions & AI Override Learning",
        "Click on 'Historical Decisions', then 'AI Override & Learning'.",
        "We maintain an immutable historical audit log. When a human officer overrides an AI recommendation (e.g. choosing IS 15298 for high-voltage sites), the system captures this as a Learning Signal Rule (#RL-2024-HV-01), fine-tuning future vector retrieval without hallucination."
    ),
    (
        "Screen 9: Export Report Modal & Closing",
        "Click the teal 'Export Report' button in the top bar.",
        "Finally, clicking 'Export Report' instantly generates an official Government of India Procurement Standards Compliance Certificate ready to attach to the GeM tender file. IS-SARATHI cuts tender prep from days to seconds and guarantees 100% BIS compliance. Thank you!"
    )
]

for title, action, script in screens:
    # Table card
    tbl = doc.add_table(rows=2, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.8)

    # Row 1: Header
    c1 = tbl.cell(0, 0)
    set_cell_background(c1, "1E2761")
    set_cell_margins(c1, top=80, bottom=80, left=120, right=120)
    p_c1 = c1.paragraphs[0]
    r_c1 = p_c1.add_run(f"▶  {title}")
    r_c1.font.bold = True
    r_c1.font.size = Pt(11)
    r_c1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Row 2: Content
    c2 = tbl.cell(1, 0)
    set_cell_background(c2, "F8FAFC")
    set_cell_margins(c2, top=100, bottom=100, left=120, right=120)
    p_c2_act = c2.paragraphs[0]
    r_act_lbl = p_c2_act.add_run("ACTION / CLICK: ")
    r_act_lbl.font.bold = True
    r_act_lbl.font.size = Pt(9.5)
    r_act_lbl.font.color.rgb = COLOR_TEAL
    r_act_val = p_c2_act.add_run(action)
    r_act_val.font.italic = True
    r_act_val.font.size = Pt(9.5)
    p_c2_act.paragraph_format.space_after = Pt(6)

    p_c2_spk = c2.add_paragraph()
    r_spk_lbl = p_c2_spk.add_run("SPOKEN SCRIPT: \n")
    r_spk_lbl.font.bold = True
    r_spk_lbl.font.size = Pt(10)
    r_spk_lbl.font.color.rgb = COLOR_NAVY
    r_spk_val = p_c2_spk.add_run(f'"{script}"')
    r_spk_val.font.size = Pt(10)
    r_spk_val.font.color.rgb = COLOR_BLACK

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# 3. Anticipated Judge Q&A
doc.add_page_break()
h3 = doc.add_heading("3. Anticipated Judge Q&A and Winning Answers", level=1)
h3.style.font.color.rgb = COLOR_NAVY

qas = [
    (
        "Q1: How do you handle standards that get updated, amended, or superseded?",
        "IS-SARATHI tracks the BIS Gazette Reaffirmation lifecycle. In our Recommendations tab, each standard displays its reaffirmation status and latest amendment (e.g. Amendment 2, 2019). If a standard is superseded, it is tagged in red and points to the active replacement."
    ),
    (
        "Q2: What happens if an AI recommendation is inaccurate or disputed?",
        "We maintain a strict Human-in-the-Loop architecture. The procurement officer always retains override authority. When an override occurs, the system logs the justification and converts it into a policy rule (e.g. Rule #RL-2024-HV-01) to refine future retriever weighting."
    ),
    (
        "Q3: How easily can this integrate into the actual GeM / CPPP portal?",
        "Our frontend and data schemas are modular and API-first. It can be embedded directly as a micro-frontend iframe widget or connected via RESTful API into the GeM tender creation wizard during the technical parameter definition stage."
    ),
    (
        "Q4: How does this prevent vendor bid rigging or bias?",
        "By enforcing objective clause verification and 'Why Not?' explainability, the platform ensures tenders do not insert restrictive specifications tailored to a single vendor, ensuring open competition under Public Procurement (Preference to Make in India) Orders."
    )
]

for q, a in qas:
    p_q = doc.add_paragraph()
    r_q = p_q.add_run(q)
    r_q.font.bold = True
    r_q.font.size = Pt(11)
    r_q.font.color.rgb = COLOR_NAVY
    p_q.paragraph_format.space_after = Pt(2)

    p_a = doc.add_paragraph()
    r_a = p_a.add_run(f"Winning Response: {a}")
    r_a.font.size = Pt(10)
    r_a.font.color.rgb = COLOR_BLACK
    p_a.paragraph_format.space_after = Pt(8)

# 4. Presentation Day Checklist
h4 = doc.add_heading("4. Presentation Day Checklist", level=1)
h4.style.font.color.rgb = COLOR_NAVY

tips = [
    "Open https://is-sarathi.vercel.app beforehand on Chrome/Edge and press F11 for clean Fullscreen view.",
    "Practice the tab transitions in sequence: Dashboard → Tender Analysis → Recommendations → Related Standards → Coverage → Conflicts → Why Not → Override → Export.",
    "Click the 'Analyze Specification' button live to demonstrate real-time parameter parsing.",
    "End the pitch by opening the 'Export Report' modal to show the official Government Certificate."
]

for tip in tips:
    p_tip = doc.add_paragraph(style='List Bullet')
    r_tip = p_tip.add_run(tip)
    r_tip.font.size = Pt(10)

doc.save("IS_SARATHI_SIH2026_Pitch_and_Demo_Guide.docx")
print("Word document generated successfully!")
