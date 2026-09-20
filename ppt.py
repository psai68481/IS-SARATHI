from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION

BLUE=RGBColor(0x0B,0x5C,0xAB); DARKBLUE=RGBColor(0x08,0x3A,0x6E)
LIGHTBLUE=RGBColor(0xE3,0xEF,0xFA); GREEN=RGBColor(0x1E,0x7D,0x32)
LIGHTGREEN=RGBColor(0xE4,0xF3,0xE7); RED=RGBColor(0xC0,0x2B,0x2B)
ORANGE=RGBColor(0xD9,0x7A,0x21); GRAY=RGBColor(0x55,0x5F,0x6B)
LIGHTGRAY=RGBColor(0xF2,0xF4,0xF7); WHITE=RGBColor(0xFF,0xFF,0xFF)
BLACK=RGBColor(0x1A,0x1A,0x1A); YELLOW=RGBColor(0xF4,0xB4,0x00)
PALEBLUE=RGBColor(0xBF,0xD9,0xF2); LINE=RGBColor(0xD5,0xDD,0xE5)
CREAM=RGBColor(0xFB,0xEE,0xDC)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
BLANK=prs.slide_layouts[6]; SW,SH=prs.slide_width,prs.slide_height

def rect(s,x,y,w,h,fill=WHITE,line=None,round_=False,radius=0.08):
    shp=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,x,y,w,h)
    if round_:
        try: shp.adjustments[0]=radius
        except Exception: pass
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb=fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb=line; shp.line.width=Pt(1)
    shp.shadow.inherit=False; return shp

def text(s,x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space_after=4,line_spacing=1.0,wrap=True):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame
    tf.word_wrap=wrap; tf.vertical_anchor=anchor
    tf.margin_left=tf.margin_right=Emu(0); tf.margin_top=tf.margin_bottom=Emu(0)
    for i,para in enumerate(runs):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.space_after=Pt(space_after); p.line_spacing=line_spacing
        for (t,size,color,bold,italic) in para:
            r=p.add_run(); r.text=t; r.font.size=Pt(size); r.font.color.rgb=color
            r.font.bold=bold; r.font.italic=italic; r.font.name="Calibri"
    return tb

def header(s,title,page=None):
    rect(s,0,0,SW,Inches(0.92),fill=BLUE)
    rect(s,0,Inches(0.92),SW,Inches(0.06),fill=YELLOW)
    text(s,Inches(0.5),Inches(0.13),Inches(10.5),Inches(0.7),
         [[(title,30,WHITE,True,False)]],anchor=MSO_ANCHOR.MIDDLE)
    rect(s,Inches(11.35),Inches(0.14),Inches(1.6),Inches(0.64),fill=WHITE,round_=True,radius=0.25)
    text(s,Inches(11.35),Inches(0.16),Inches(1.6),Inches(0.6),
         [[("SIH 2026",12,BLUE,True,False)],[("Team Sarathi",10,GRAY,False,False)]],
         align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space_after=0)
    if page:
        text(s,Inches(12.75),Inches(7.08),Inches(0.5),Inches(0.35),
             [[(str(page),11,GRAY,False,False)]],align=PP_ALIGN.RIGHT)

def footer(s):
    text(s,Inches(0.5),Inches(7.08),Inches(6),Inches(0.35),
         [[("IS-SARATHI  |  SIH 2026 Idea Submission",10,GRAY,False,False)]])

def card_title(s,x,y,w,label,color=BLUE):
    text(s,x,y,w,Inches(0.32),[[(label,14,color,True,False)]])

# ===== SLIDE 1 : TITLE =====
s=prs.slides.add_slide(BLANK)
rect(s,0,0,SW,SH,fill=DARKBLUE)
rect(s,0,Inches(4.9),SW,Inches(0.07),fill=YELLOW)
for cx,cy,r in [(11.9,1.1,1.5),(12.6,5.9,1.1),(0.9,6.2,0.9)]:
    o=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(cx),Inches(cy),Inches(r),Inches(r))
    o.fill.solid(); o.fill.fore_color.rgb=BLUE; o.line.fill.background(); o.shadow.inherit=False
text(s,Inches(1),Inches(1.5),Inches(11.3),Inches(1.6),[[("IS-SARATHI",64,WHITE,True,False)]],align=PP_ALIGN.CENTER)
text(s,Inches(1),Inches(3.0),Inches(11.3),Inches(0.6),
     [[("AI-Powered Semantic Search for Indian Standards in Public Procurement",23,PALEBLUE,False,False)]],align=PP_ALIGN.CENTER)
text(s,Inches(1),Inches(3.8),Inches(11.3),Inches(0.5),
     [[("Team Sarathi   |   Smart India Hackathon 2026",18,WHITE,False,False)]],align=PP_ALIGN.CENTER)
text(s,Inches(1),Inches(5.25),Inches(11.3),Inches(1.4),
     [[("Problem: ",14,YELLOW,True,False),
       ("procurement officers struggle to map plain-language tender requirements to the correct Indian Standard (IS) codes — slowing tenders, causing disputes, and blocking MSME participation.",14,WHITE,False,False)],
      [("Pitch: ",14,YELLOW,True,False),
       ("ask in plain language (even Hindi, Tamil, Bengali…), get the right IS code with an auditable citation — in under 2 seconds.",14,WHITE,False,False)]],
     align=PP_ALIGN.CENTER,space_after=8)

# ===== SLIDE 2 : PROPOSED SOLUTION =====
s=prs.slides.add_slide(BLANK)
rect(s,0,0,SW,SH,fill=LIGHTGRAY)
header(s,"PROPOSED SOLUTION",page=2); footer(s)
L=Inches(0.45); T=Inches(1.25); W=Inches(6.05); H=Inches(5.6)
rect(s,L,T,W,H,fill=WHITE,line=LINE,round_=True)
card_title(s,L+Inches(0.3),T+Inches(0.2),W-Inches(0.6),"How IS-SARATHI works")
bullets=[("AI-powered RAG engine"," converts plain-language requirements into ranked Indian Standards — no IS-code memorisation needed."),
 ("Semantic + metadata search"," combines meaning-based retrieval with ICS code, status and certification filtering for precise matches."),
 ("Grounded citations"," — every recommendation quotes the exact retrieved scope text, so answers are auditable and traceable to BIS sources."),
 ("Version & certification flagging"," — surfaces outdated editions and marks mandatory schemes (ISI / CRS / Hallmarking)."),
 ("Related-standards discovery"," for testing, safety and installation requirements linked to each standard."),
 ("Confidence-based fallback"," — low-confidence queries are routed to the official BIS portal instead of guessing.")]
paras=[[("▸  ",13,BLUE,True,False),(b[0],13,BLACK,True,False),(b[1],13,BLACK,False,False)] for b in bullets]
text(s,L+Inches(0.3),T+Inches(0.62),W-Inches(0.6),H-Inches(0.85),paras,space_after=9,line_spacing=1.05)
R=Inches(6.85); RW=Inches(6.05)
rect(s,R,T,RW,H,fill=WHITE,line=LINE,round_=True)
card_title(s,R+Inches(0.3),T+Inches(0.2),RW-Inches(0.6),"It Addresses the Problem:")
probs=[("Prevents procurement errors"," — answers are always traceable to current, official Indian Standards."),
 ("Scalable & reliable"," — instant knowledge-base updates via re-indexing; no model retraining needed."),
 ("Empowers MSMEs & engineers"," — fast, accessible standards discovery without deep domain expertise."),
 ("Builds trust"," — grounded citations plus confidence scoring and honest fallbacks, never silent guesses."),
 ("Works in Indian languages"," — multilingual query pipeline with English fallback for regional officers and vendors.")]
paras=[[("✔  ",13,GREEN,True,False),(p[0],13,BLACK,True,False),(p[1],13,BLACK,False,False)] for p in probs]
text(s,R+Inches(0.3),T+Inches(0.62),RW-Inches(0.6),H-Inches(0.85),paras,space_after=12,line_spacing=1.05)
rect(s,Inches(5.72),Inches(3.85),Inches(1.9),Inches(0.7),fill=BLUE,round_=True,radius=0.5)
text(s,Inches(5.72),Inches(3.9),Inches(1.9),Inches(0.6),
     [[("IS-SARATHI",15,WHITE,True,False)],[("RAG + Search",10,PALEBLUE,False,False)]],
     align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space_after=0)

# ===== SLIDE 3 : TECHNICAL APPROACH =====
s=prs.slides.add_slide(BLANK)
rect(s,0,0,SW,SH,fill=LIGHTGRAY)
header(s,"TECHNICAL APPROACH",page=3); footer(s)
T3=Inches(1.2); H3=Inches(2.55); GAP=Inches(0.25)
CW=(SW-Inches(0.9)-GAP*2)/3
x=Inches(0.45)
rect(s,x,T3,CW,H3,fill=WHITE,line=LINE,round_=True)
card_title(s,x+Inches(0.25),T3+Inches(0.15),CW-Inches(0.5),"Tech Stack")
stack=[("Frontend","Next.js · React · TypeScript · Tailwind CSS"),
 ("Backend","Python · FastAPI · Uvicorn"),
 ("Vector Store","FAISS + Sentence-Transformers (multilingual)"),
 ("AI / LLM","OpenAI API / Groq SDK · LangChain"),
 ("Database","PostgreSQL (metadata, logs, user data)"),
 ("Deploy & Dev","Vercel · Render · Docker  |  Git / GitHub (version control)")]
paras=[[(k+":  ",11.5,BLUE,True,False),(v,11.5,BLACK,False,False)] for k,v in stack]
text(s,x+Inches(0.25),T3+Inches(0.55),CW-Inches(0.5),H3-Inches(0.7),paras,space_after=8)
text(s,x+Inches(0.25),T3+H3-Inches(0.42),CW-Inches(0.5),Inches(0.35),
     [[("Modular, retrieval-based — scales without retraining",10.5,RED,False,True)]])
x=Inches(0.45)+CW+GAP
rect(s,x,T3,CW,H3,fill=WHITE,line=LINE,round_=True)
card_title(s,x+Inches(0.25),T3+Inches(0.15),CW-Inches(0.5),"Working Prototype")
rect(s,x+Inches(0.25),T3+Inches(0.55),CW-Inches(0.5),Inches(0.32),fill=LIGHTGRAY,round_=True,radius=0.5)
rect(s,x+Inches(0.25),T3+Inches(0.55),(CW-Inches(0.5))*0.55,Inches(0.32),fill=GREEN,round_=True,radius=0.5)
text(s,x+Inches(0.25),T3+Inches(0.56),CW-Inches(0.5),Inches(0.3),
     [[("Progress: 55%",11,WHITE,True,False)]],align=PP_ALIGN.CENTER)
feats=["Natural-language & multilingual queries","ICS + status metadata filtering",
 "Related-standards discovery","Grounded citations with scope-text quotes",
 "Confidence-based fallback to BIS portal"]
paras=[[("✔  ",11.5,GREEN,True,False),(f,11.5,BLACK,False,False)] for f in feats]
text(s,x+Inches(0.25),T3+Inches(1.05),CW-Inches(0.5),Inches(1.5),paras,space_after=6)
rect(s,x+Inches(0.25),T3+H3-Inches(0.5),CW-Inches(0.5),Inches(0.36),fill=BLUE,round_=True,radius=0.5)
text(s,x+Inches(0.25),T3+H3-Inches(0.49),CW-Inches(0.5),Inches(0.34),
     [[("Demo video: [insert clickable link]",12,WHITE,True,False)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
x=Inches(0.45)+(CW+GAP)*2
rect(s,x,T3,CW,H3,fill=WHITE,line=LINE,round_=True)
card_title(s,x+Inches(0.25),T3+Inches(0.15),CW-Inches(0.5),"Pilot Scope & Performance")
chips=[("40–80","curated IS standards in pilot KB"),("5–10","ranked candidates per query"),
 ("<2s","end-to-end response time"),("RAG + FAISS","retrieval engine, no model training"),
 ("Multilingual","Hindi, Tamil, Bengali + English fallback")]
paras=[[(a+"  ",15,BLUE,True,False),("— "+b,11,BLACK,False,False)] for a,b in chips]
text(s,x+Inches(0.25),T3+Inches(0.6),CW-Inches(0.5),H3-Inches(0.75),paras,space_after=9)
text(s,x+Inches(0.25),T3+H3-Inches(0.62),CW-Inches(0.5),Inches(0.55),
     [[("Roadmap: pilot corpus → full BIS catalogue (20,000+ IS codes) via automated digitisation.",10.5,GRAY,False,True)]],line_spacing=1.0)
TB=Inches(4.0); HB=Inches(2.85)
rect(s,Inches(0.45),TB,SW-Inches(0.9),HB,fill=WHITE,line=LINE,round_=True)
card_title(s,Inches(0.75),TB+Inches(0.12),Inches(6),"System Flow")
steps=[("1. Query","Officer types plain-language / multilingual requirement"),
 ("2. Retrieve","FAISS semantic search over curated IS knowledge base"),
 ("3. Filter & Re-rank","ICS, status & certification filters + LLM re-ranking"),
 ("4. Grounded Answer","Ranked IS codes + quoted scope text + confidence score"),
 ("5. Fallback","Low confidence → direct link to official BIS portal")]
bw=Inches(2.28); bh=Inches(1.55); by=TB+Inches(0.55); x0=Inches(0.75)
for i,(t1,t2) in enumerate(steps):
    bx=x0+i*(bw+Inches(0.29))
    col=[BLUE,DARKBLUE,BLUE,GREEN,ORANGE][i]
    fillc=LIGHTBLUE if i<3 else (LIGHTGREEN if i==3 else CREAM)
    rect(s,bx,by,bw,bh,fill=fillc,line=col,round_=True)
    text(s,bx+Inches(0.08),by+Inches(0.12),bw-Inches(0.16),Inches(0.4),
         [[(t1,13,col,True,False)]],align=PP_ALIGN.CENTER)
    text(s,bx+Inches(0.12),by+Inches(0.5),bw-Inches(0.24),bh-Inches(0.6),
         [[(t2,10.5,BLACK,False,False)]],align=PP_ALIGN.CENTER,line_spacing=1.02)
    if i<4:
        ar=s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,bx+bw+Inches(0.015),by+Inches(0.6),Inches(0.27),Inches(0.32))
        ar.fill.solid(); ar.fill.fore_color.rgb=GRAY; ar.line.fill.background(); ar.shadow.inherit=False
rect(s,Inches(0.75),by+bh+Inches(0.12),SW-Inches(1.5),Inches(0.42),fill=LIGHTGRAY,round_=True,radius=0.3)
text(s,Inches(0.95),by+bh+Inches(0.16),SW-Inches(1.7),Inches(0.35),
     [[("Admin dashboard: ",11,DARKBLUE,True,False),
       ("knowledge-base curation · accuracy monitoring · standards update log · ICS taxonomy verification",11,GRAY,False,False)]])

# ===== SLIDE 4 : FEASIBILITY AND VIABILITY =====
s=prs.slides.add_slide(BLANK)
rect(s,0,0,SW,SH,fill=LIGHTGRAY)
header(s,"FEASIBILITY AND VIABILITY",page=4); footer(s)
T4=Inches(1.2); H4=Inches(4.35); GAP=Inches(0.25)
CW=(SW-Inches(0.9)-GAP*2)/3
x=Inches(0.45)
rect(s,x,T4,CW,H4,fill=WHITE,line=LINE,round_=True)
card_title(s,x+Inches(0.25),T4+Inches(0.15),CW-Inches(0.5),"Financials (pilot-year cost)")
rows=[("Knowledge Base (curation & verification)","₹1.1L – ₹1.3L",40),
      ("Cloud (compute, storage, security)","₹70K – ₹80K",25),
      ("Backend & AI (LLM APIs, vector DB)","₹68K – ₹75K",24),
      ("Others (audits, compliance updates)","₹28K – ₹35K",11)]
ry=T4+Inches(0.55)
for name,val,pct in rows:
    rect(s,x+Inches(0.25),ry,Inches(0.14),Inches(0.14),fill=BLUE,round_=True)
    text(s,x+Inches(0.48),ry-Inches(0.04),CW-Inches(0.72),Inches(0.5),
         [[(name,10,BLACK,False,False)],[(val+"  ("+str(pct)+"%)",10,BLUE,True,False)]],space_after=1,line_spacing=0.98)
    ry+=Inches(0.55)
cd=CategoryChartData()
cd.categories=["Knowledge Base","Cloud","Backend & AI","Others"]
cd.add_series("Cost share",(40,25,24,11))
gf=s.shapes.add_chart(XL_CHART_TYPE.PIE,x+Inches(0.7),ry+Inches(0.02),Inches(2.5),Inches(1.25),cd)
ch=gf.chart; ch.has_legend=False; plot=ch.plots[0]
plot.has_data_labels=True; dl=plot.data_labels
dl.show_percentage=True; dl.show_value=False; dl.show_category_name=False
dl.position=XL_LABEL_POSITION.BEST_FIT
dl.font.size=Pt(9); dl.font.color.rgb=WHITE; dl.font.bold=True
for i,pt in enumerate(plot.series[0].points):
    pt.format.fill.solid(); pt.format.fill.fore_color.rgb=[BLUE,GREEN,ORANGE,GRAY][i]
text(s,x+Inches(0.25),T4+H4-Inches(0.28),CW-Inches(0.5),Inches(0.25),
     [[("Cost split totals 100% of the ~₹3.0L pilot budget",9.5,GRAY,False,True)]])
x=Inches(0.45)+CW+GAP
rect(s,x,T4,CW,H4,fill=WHITE,line=LINE,round_=True)
card_title(s,x+Inches(0.25),T4+Inches(0.15),CW-Inches(0.5),"Feasibility")
feas=[("Proven RAG architecture"," — FAISS + sentence-transformers for reliable multilingual retrieval."),
 ("Pilot-scale corpus"," — 40–80 priority standards digitised in Phase 1; automated pipeline scales to BIS's full 20,000+ code catalogue [Ref 2]."),
 ("Multilingual pipeline"," — tested across major Indian languages with English fallback."),
 ("Low infrastructure cost"," — lightweight vector search + pay-per-use LLM APIs; response under 2s."),
 ("Open-source stack"," — FastAPI, FAISS, LangChain; no proprietary licensing.")]
paras=[[("▸  ",11.5,BLUE,True,False),(a,11.5,BLACK,True,False),(b,11.5,BLACK,False,False)] for a,b in feas]
text(s,x+Inches(0.25),T4+Inches(0.55),CW-Inches(0.5),H4-Inches(0.7),paras,space_after=9,line_spacing=1.03)
x=Inches(0.45)+(CW+GAP)*2
rect(s,x,T4,CW,H4,fill=WHITE,line=LINE,round_=True)
card_title(s,x+Inches(0.25),T4+Inches(0.15),CW-Inches(0.5),"Viability")
viab=[("Massive market"," — India's public procurement is ~$500B annually (20–22% of GDP) [Ref 1]; standards compliance is mandatory across sectors."),
 ("Policy alignment"," — supports BIS and Dept. of Consumer Affairs digital-governance and e-procurement modernisation goals."),
 ("Cuts training burden"," — new officers find the right standard without domain expertise."),
 ("Extensible"," — private procurement and export-compliance use cases beyond government."),
 ("Revenue model"," — SaaS licensing for procurement portals, PSU partnerships, per-query API access, training & consulting.")]
paras=[[("▸  ",11.5,GREEN,True,False),(a,11.5,BLACK,True,False),(b,11.5,BLACK,False,False)] for a,b in viab]
text(s,x+Inches(0.25),T4+Inches(0.55),CW-Inches(0.5),H4-Inches(0.7),paras,space_after=9,line_spacing=1.03)
T5=Inches(5.7); H5=Inches(1.3)
rect(s,Inches(0.45),T5,SW-Inches(0.9),H5,fill=WHITE,line=LINE,round_=True)
text(s,Inches(0.75),T5+Inches(0.08),Inches(8),Inches(0.32),
     [[("Challenges and Mitigation",14,RED,True,False)]])
ch=[("Incomplete / outdated standards data","Hand-curated dataset + scheduled version & amendment audits keep records current"),
    ("LLM may hallucinate wrong IS codes","Retrieval-grounded answers quote source scope text only — fabrication risk minimised, not zero; every answer carries a verifiable citation"),
    ("Regional-language accuracy varies","Translation layer tested across major Indian languages, with fallback to English originals"),
    ("Slow government adoption cycles","Pilot partnership with a BIS regional office to validate before wider rollout")]
colw=(SW-Inches(1.5))/2
for i,(c,m) in enumerate(ch):
    cxx=Inches(0.75)+(i%2)*colw; cyy=T5+Inches(0.45)+(i//2)*Inches(0.42)
    text(s,cxx,cyy,colw-Inches(0.35),Inches(0.4),
         [[("⚠ ",10.5,ORANGE,True,False),(c+"  ",10.5,BLACK,True,False),
           ("→ ",10.5,GREEN,True,False),(m,10.5,GRAY,False,False)]],line_spacing=0.95,space_after=0)

# ===== SLIDE 5 : IMPACT AND BENEFITS =====
s=prs.slides.add_slide(BLANK)
rect(s,0,0,SW,SH,fill=LIGHTGRAY)
header(s,"IMPACT AND BENEFITS",page=5); footer(s)
T5=Inches(1.2); H5=Inches(5.6)
HALF=(SW-Inches(0.9)-Inches(0.3))/2
x=Inches(0.45)
rect(s,x,T5,HALF,H5,fill=WHITE,line=LINE,round_=True)
text(s,x+Inches(0.3),T5+Inches(0.15),HALF-Inches(0.6),Inches(0.4),
     [[("IMPACT — the problem today",16,RED,True,False)]])
impacts=[("Slow manual lookup","Manual standard lookup slows procurement speed by an estimated 30–40% across government tenders*."),
 ("Wrong or outdated citations","Outdated editions cited in tenders cause disputes and rework during evaluation*."),
 ("Digital divide","Manual search fails in low-digital-literacy settings common among MSMEs and smaller vendors."),
 ("Real money at stake","India's public procurement market is ~$500B annually [Ref 1] — errors carry real fiscal cost."),
 ("Compliance loss","Ambiguous specifications are estimated to cut vendor compliance accuracy by 15–20%*."),
 ("Tender delays","Standards disputes contribute to delays in an estimated 25% of tenders*."),
 ("Knowledge gap","The gap spans 20,000+ published IS codes [Ref 2] across dozens of sectors.")]
iy=T5+Inches(0.65)
for t1,t2 in impacts:
    rect(s,x+Inches(0.3),iy+Inches(0.03),Inches(0.14),Inches(0.14),fill=RED,round_=True)
    text(s,x+Inches(0.55),iy,HALF-Inches(0.9),Inches(0.62),
         [[(t1+": ",11.5,BLACK,True,False),(t2,11.5,BLACK,False,False)]],line_spacing=1.0,space_after=0)
    iy+=Inches(0.63)
text(s,x+Inches(0.3),T5+H5-Inches(0.42),HALF-Inches(0.6),Inches(0.35),
     [[("*Team estimates from pilot user interviews (n=25) — to be validated in Phase 1.",9.5,GRAY,False,True)]])
x=Inches(0.45)+HALF+Inches(0.3)
rect(s,x,T5,HALF,H5,fill=WHITE,line=LINE,round_=True)
text(s,x+Inches(0.3),T5+Inches(0.15),HALF-Inches(0.6),Inches(0.4),
     [[("BENEFITS — who gains what",16,GREEN,True,False)]])
bens=[("Procurement officers","Faster, confident standard selection with grounded citations."),
 ("Engineers & MSMEs","Plain-language search removes the need for BIS expertise."),
 ("Tender committees","Reduced disputes and rework; fewer compliance errors."),
 ("BIS & Ministry","Digital governance aligned with e-procurement modernisation goals."),
 ("Government & PSUs","Standardised, auditable procurement decisions; review time down ~40%*."),
 ("Small vendors","Easier compliance access, levelling the playing field for MSMEs."),
 ("Training institutes","Faster onboarding of new procurement staff via self-serve search."),
 ("Cross-department reach","Amplifies standardisation across ministries.")]
by_=T5+Inches(0.65)
for t1,t2 in bens:
    rect(s,x+Inches(0.3),by_+Inches(0.03),Inches(0.14),Inches(0.14),fill=GREEN,round_=True)
    text(s,x+Inches(0.55),by_,HALF-Inches(0.9),Inches(0.62),
         [[(t1+": ",11.5,BLACK,True,False),(t2,11.5,BLACK,False,False)]],line_spacing=1.0,space_after=0)
    by_+=Inches(0.58)
rect(s,Inches(6.16),Inches(3.9),Inches(1.0),Inches(1.0),fill=BLUE,round_=True,radius=0.5)
text(s,Inches(6.16),Inches(4.02),Inches(1.0),Inches(0.8),[[("🔍",22,WHITE,False,False)]],
     align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)

# ===== SLIDE 6 : RESEARCH AND REFERENCES =====
s=prs.slides.add_slide(BLANK)
rect(s,0,0,SW,SH,fill=LIGHTGRAY)
header(s,"RESEARCH AND REFERENCES",page=6); footer(s)

T6=Inches(1.2); H6_TOP=Inches(3.85); GAP6=Inches(0.3)
HALF6=(SW-Inches(0.9)-GAP6)/2
x1=Inches(0.45)

# Left Column: Existing Solutions & Gap Analysis
rect(s,x1,T6,HALF6,H6_TOP,fill=WHITE,line=LINE,round_=True)
card_title(s,x1+Inches(0.3),T6+Inches(0.18),HALF6-Inches(0.6),"Existing Systems & Gap Analysis")

gaps=[
    ("BIS Manakonline Portal", "Requires exact IS number or navigating deep ICS hierarchies; no plain-language or intent search for non-experts."),
    ("GeM Keyword Search", "Limited to exact string matches; fails on descriptive technical specifications or regional language queries."),
    ("General-Purpose LLMs", "Prone to hallucinating obsolete or non-existent IS codes; lack real-time ground truth and verifiable clause citations."),
    ("IS-SARATHI Differentiator", "Combines multilingual semantic embeddings with grounded RAG to guarantee auditable, clause-level BIS citations under 2s.")
]

gy=T6+Inches(0.58)
for title, desc in gaps:
    col = GREEN if "Differentiator" in title else BLUE
    bullet = "★ " if "Differentiator" in title else "▸ "
    text(s,x1+Inches(0.3),gy,HALF6-Inches(0.6),Inches(0.72),
         [[(bullet,11.5,col,True,False),(title+": ",11.5,DARKBLUE,True,False),(desc,11,BLACK,False,False)]],
         line_spacing=1.02,space_after=0)
    gy+=Inches(0.78)

# Right Column: Research & Citations
x2=Inches(0.45)+HALF6+GAP6
rect(s,x2,T6,HALF6,H6_TOP,fill=WHITE,line=LINE,round_=True)
card_title(s,x2+Inches(0.3),T6+Inches(0.18),HALF6-Inches(0.6),"Research Literature & Data Sources")

refs=[
    ("[Ref 1] Ministry of Finance / World Bank Report", "Public Procurement in India: Assessment of Market Size (~20–22% of GDP, ~$500B annually) and standardization bottlenecks."),
    ("[Ref 2] Bureau of Indian Standards (BIS)", "Official Standards Catalogue & Manakonline Database (20,000+ published standards across 14 division councils and ICS taxonomy)."),
    ("[Ref 3] Lewis et al. (NeurIPS)", "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks — foundational architecture for eliminating LLM hallucinations."),
    ("[Ref 4] Reimers & Gurevych (EMNLP)", "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks — basis for high-speed multilingual vector similarity search.")
]

ry=T6+Inches(0.58)
for title, desc in refs:
    text(s,x2+Inches(0.3),ry,HALF6-Inches(0.6),Inches(0.72),
         [[("▸ ",11.5,BLUE,True,False),(title+": ",11.5,DARKBLUE,True,False),(desc,11,BLACK,False,False)]],
         line_spacing=1.02,space_after=0)
    ry+=Inches(0.78)

# Bottom Container: Policy Alignment & Open-Source Stack
T6_BOT=Inches(5.2)
H6_BOT=Inches(1.75)
rect(s,Inches(0.45),T6_BOT,SW-Inches(0.9),H6_BOT,fill=WHITE,line=LINE,round_=True)
card_title(s,Inches(0.75),T6_BOT+Inches(0.14),SW-Inches(1.5),"Policy Alignment & Technical Foundation")

policies=[
    ("Digital India & e-Governance", "Directly supports the modernization of public e-procurement (GeM / CPPP) and transparent standard enforcement."),
    ("Make in India & MSME Growth", "Lowers compliance barriers for small enterprises by democratizing access to complex technical standards."),
    ("Open Standards & Toolchain", "Built on open-source FAISS, FastAPI, LangChain, and PostgreSQL — modular, auditable, and self-hostable on sovereign cloud infra."),
    ("Sovereign Data Governance", "All standards indexes and query telemetry reside within domestic infrastructure compliant with DPDP Act 2023.")
]

colw=(SW-Inches(1.5))/2
for i,(p_title, p_desc) in enumerate(policies):
    px = Inches(0.75) + (i % 2) * colw
    py = T6_BOT + Inches(0.48) + (i // 2) * Inches(0.56)
    text(s, px, py, colw - Inches(0.3), Inches(0.5),
         [[("✔ ",10.5,GREEN,True,False),(p_title+":  ",10.5,DARKBLUE,True,False),(p_desc,10,GRAY,False,False)]],
         line_spacing=0.98, space_after=0)

# Save presentation
prs.save("IS_SARATHI_SIH2026.pptx")
print("Successfully generated IS_SARATHI_SIH2026.pptx")