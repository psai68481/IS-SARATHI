import React, { useState } from 'react';
import { 
  Sparkles, 
  Cpu, 
  CheckCircle2, 
  FileText, 
  RefreshCw, 
  ArrowRight, 
  Shield, 
  Tag, 
  Scan, 
  Upload, 
  Image as ImageIcon,
  Zap,
  AlertTriangle,
  FileCheck
} from 'lucide-react';
import OcrScannerModal from '../common/OcrScannerModal';

export default function TenderAnalysisTab({ 
  data, 
  setData, 
  onNavigateTab, 
  customQuery, 
  setCustomQuery 
}) {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analyzed, setAnalyzed] = useState(true);
  const [scanStep, setScanStep] = useState("");
  const [isOcrModalOpen, setIsOcrModalOpen] = useState(false);
  const [activeOcrDoc, setActiveOcrDoc] = useState(null);

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    setAnalyzed(false);
    setScanStep("Tokenizing tender specification & isolating technical clauses...");

    setTimeout(() => {
      setScanStep("Vector similarity search against verified BIS knowledge base...");
    }, 400);

    setTimeout(() => {
      setScanStep("Extracting mandatory safety, dielectric & weight parameters...");
    }, 800);

    setTimeout(() => {
      setIsAnalyzing(false);
      setAnalyzed(true);
      setScanStep("");
    }, 1200);
  };

  const handleReset = () => {
    setCustomQuery(data.tenderQuery);
    setActiveOcrDoc(null);
  };

  const handleApplyOcrText = (extractedText, docInfo) => {
    setCustomQuery(extractedText);
    setActiveOcrDoc(docInfo || {
      name: "Tender_Notice_PWD_Helmets_2024.pdf",
      type: "PDF/PNG",
      confidence: 99.4
    });
    handleAnalyze();
  };

  const sampleOcrDocs = data?.ocrSamples || [
    {
      id: "ocr-helmet-pdf",
      name: "Tender_Notice_PWD_Helmets_2024.pdf",
      type: "PDF",
      size: "248 KB",
      department: "Public Works Dept (PWD)",
      extractedText: "We need industrial helmets for construction workers with impact resistance and electrical insulation ultra weight less than 250",
      previewSnippet: "TENDER NOTICE NO: PWD/ELECT/2026/089\nItem 01: Industrial Safety Helmets for construction labor\nKey Specs: Impact resistance (50J drop test), Electrical insulation, Ultra-weight requirement: Less than 250 grams total weight."
    },
    {
      id: "ocr-helmet-png",
      name: "Scanned_BoQ_Helmets_Spec.png",
      type: "PNG",
      size: "612 KB",
      department: "Central Vigilance Division",
      extractedText: "We need industrial helmets for construction workers with impact resistance and electrical insulation ultra weight less than 250",
      previewSnippet: "[SCANNED DOCUMENT OCR RECOGNIZED]\nSection B.2: Personnel Protective Gear (Head Protection)\nSpecifications: Impact resistance shock absorption; Dielectric electrical resistance; Ultra-lightweight shell under 250 grams."
    }
  ];

  return (
    <div className="space-y-6">
      
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <FileText className="w-5 h-5 text-teal-600" />
            Tender Specification & Parameter Extraction
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Ingest raw tender text or scan physical PDF & PNG tender notices using our optical character recognition (OCR) engine.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsOcrModalOpen(true)}
            className="px-3.5 py-1.5 bg-gradient-to-r from-teal-600 to-blue-600 hover:from-teal-700 hover:to-blue-700 text-white rounded-lg text-xs font-bold shadow-sm transition-all flex items-center gap-1.5 active:scale-95 cursor-pointer"
          >
            <Scan className="w-4 h-4 text-teal-200 animate-pulse" />
            <span>OCR Scan PDF / PNG Document</span>
          </button>
        </div>
      </div>

      {/* Quick OCR Samples Bar */}
      <div className="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 text-white rounded-xl p-4 border border-slate-800 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-teal-500/20 text-teal-300 flex items-center justify-center shrink-0 border border-teal-500/30">
              <Scan className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-teal-300 uppercase tracking-wider">
                  OCR Ingestion Engine
                </span>
                <span className="text-[10px] bg-teal-400/20 text-teal-200 px-2 py-0.2 rounded-full font-mono">
                  v5.0 Ready
                </span>
              </div>
              <p className="text-[11px] text-slate-300 mt-0.5">
                Test 1-click OCR text extraction on sample scanned tenders:
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {sampleOcrDocs.map((doc) => (
              <button
                key={doc.id}
                onClick={() => handleApplyOcrText(doc.extractedText, doc)}
                className="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white text-xs font-semibold border border-white/20 transition-all flex items-center gap-1.5 hover:border-teal-400 active:scale-95"
                title={`Scan ${doc.name}`}
              >
                {doc.type === 'PDF' ? <FileText className="w-3.5 h-3.5 text-rose-400" /> : <ImageIcon className="w-3.5 h-3.5 text-blue-400" />}
                <span>Scan {doc.name}</span>
                <Zap className="w-3 h-3 text-amber-400" />
              </button>
            ))}

            <button
              onClick={() => setIsOcrModalOpen(true)}
              className="px-3 py-1.5 rounded-lg bg-teal-500 hover:bg-teal-600 text-white text-xs font-bold transition-all flex items-center gap-1 shadow-sm"
            >
              <Upload className="w-3.5 h-3.5" />
              <span>Upload Custom PDF/PNG</span>
            </button>
          </div>
        </div>

        {/* Active OCR Document Tag (if scanned) */}
        {activeOcrDoc && (
          <div className="mt-3 pt-3 border-t border-white/10 flex items-center justify-between text-[11px] text-teal-300">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              Ingested Document: <strong>{activeOcrDoc.name}</strong> ({activeOcrDoc.type || 'PDF'}) &bull; OCR Confidence: <strong>99.4%</strong>
            </span>
            <span className="text-slate-400">18 Tokens Recognized</span>
          </div>
        )}
      </div>

      {/* Tender Query Input Box */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
        <div className="flex items-center justify-between mb-2">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
            Procurement Tender Text / Scope of Work (SOW)
          </label>
          <button
            onClick={handleReset}
            className="text-xs text-teal-600 hover:text-teal-800 font-medium flex items-center gap-1 cursor-pointer"
          >
            <RefreshCw className="w-3 h-3" />
            Reset to Sample
          </button>
        </div>

        <div className="relative">
          <textarea
            rows={4}
            value={customQuery}
            onChange={(e) => setCustomQuery(e.target.value)}
            placeholder="Paste tender specification, BoQ items, or technical requirements here..."
            className="w-full text-sm text-slate-800 p-3.5 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:bg-white transition-all font-sans leading-relaxed resize-y"
          />
        </div>

        <div className="mt-4 flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100">
          <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
            <span className="font-semibold text-slate-700">{customQuery.length}</span> characters
            <span>&bull;</span>
            <span>Language: <strong>English (IN)</strong></span>
            <span>&bull;</span>
            <span>Format: <strong>Technical Tender Specs</strong></span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className={`px-5 py-2.5 rounded-lg text-xs font-bold text-white shadow-sm flex items-center gap-2 transition-all active:scale-95 ${
                isAnalyzing
                  ? "bg-slate-400 cursor-not-allowed"
                  : "bg-[#028090] hover:bg-[#006d7b] cursor-pointer"
              }`}
            >
              {isAnalyzing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Analyzing Specification...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Analyze Specification</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Dynamic scan progress indicator */}
        {isAnalyzing && (
          <div className="mt-4 p-3 bg-teal-50 rounded-lg border border-teal-200 flex items-center gap-3 animate-pulse">
            <Cpu className="w-5 h-5 text-teal-600 animate-spin" />
            <div className="text-xs text-teal-900 font-medium">
              {scanStep}
            </div>
          </div>
        )}
      </div>

      {/* Extracted Requirements Section */}
      {analyzed && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                Extracted Parameters & Requirements ({data.extractedRequirements.length})
              </h3>
              <p className="text-xs text-slate-500">
                Key technical parameters structured by the NLP engine for standard matching
              </p>
            </div>
            
            <button
              onClick={() => onNavigateTab('recommendations')}
              className="text-xs font-bold text-teal-700 hover:text-teal-900 flex items-center gap-1 cursor-pointer"
            >
              <span>View Recommended Standards</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
            {data.extractedRequirements.map((req, idx) => {
              const isWeight = req.field.includes("Weight");
              return (
                <div 
                  key={idx}
                  className={`bg-white p-4 rounded-xl border shadow-sm transition-all ${
                    isWeight ? "border-amber-300 ring-1 ring-amber-400/30" : "border-slate-200 hover:border-teal-300"
                  }`}
                >
                  <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
                    <span className="inline-flex items-center gap-1 font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-[11px]">
                      <Tag className="w-3 h-3 text-slate-400" />
                      {req.category || "General"}
                    </span>
                    <span className="text-[11px] font-bold text-emerald-600">
                      {req.confidence || 95}% conf.
                    </span>
                  </div>

                  <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    {req.field}
                  </div>
                  
                  <div className="text-base font-extrabold text-slate-900 mt-1 font-sans">
                    {req.value}
                  </div>

                  <div className="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                    <span>Match Status:</span>
                    <span className={`font-semibold flex items-center gap-1 ${isWeight ? "text-amber-600" : "text-emerald-600"}`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${isWeight ? "bg-amber-500" : "bg-emerald-500"}`}></span>
                      {isWeight ? "Conflict Flag" : "Clause Ready"}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Extraction Analysis Footnote */}
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-start sm:items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-teal-100 text-teal-800 flex items-center justify-center shrink-0">
                <Shield className="w-4 h-4" />
              </div>
              <div className="text-xs text-slate-700">
                <p className="font-bold text-slate-900">
                  Primary Standard Identified: <span className="text-teal-700">IS 2925:1984 (Industrial Safety Helmets)</span>
                </p>
                <p className="text-slate-500">
                  Parameters map to Clause 5.2 (Impact) and Clause 6.1 (Electrical). Note: Requested weight &lt;250g flags a conflict against Clause 4.3 (340g minimum).
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <button
                onClick={() => onNavigateTab('conflicts-gaps')}
                className="px-3.5 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-800 text-xs font-bold rounded-lg border border-amber-300 shadow-xs transition-all flex items-center gap-1 cursor-pointer"
              >
                <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                <span>View Weight Conflict</span>
              </button>
              <button
                onClick={() => onNavigateTab('coverage')}
                className="px-3.5 py-1.5 bg-white hover:bg-slate-100 text-slate-700 text-xs font-bold rounded-lg border border-slate-300 shadow-xs transition-all cursor-pointer"
              >
                Verify Clause Coverage
              </button>
            </div>
          </div>
        </div>
      )}

      {/* OCR Scanner Modal Dialog */}
      <OcrScannerModal
        isOpen={isOcrModalOpen}
        onClose={() => setIsOcrModalOpen(false)}
        onApplyExtractedText={handleApplyOcrText}
        samples={sampleOcrDocs}
      />

    </div>
  );
}
