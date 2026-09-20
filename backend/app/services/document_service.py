"""
IS-SARATHI Tender Document Processing Service (SIH26108 workflow stage 4)
==========================================================================
Extracts machine-readable text from uploaded tender documents so the evidence
pipeline can analyze them:

  1. PDF text layer extraction (pypdf) - digital PDFs
  2. OCR fallback (pytesseract + pdf2image) - scanned/image-only PDFs
  3. Plain text / .txt uploads pass straight through

The service degrades gracefully: if OCR dependencies are missing, scanned
pages are flagged as needing OCR instead of silently returning garbage.
Extracted text is passed to the SAME analyze pipeline as pasted text -
no separate recommendation path, no new failure modes.
"""

import io
import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger("is_sarathi.document")

MAX_FILE_BYTES = 20 * 1024 * 1024  # 20 MB guard rail
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".png", ".jpg", ".jpeg"}

# Text-layer quality threshold: below this chars/page the PDF is likely scanned
MIN_CHARS_PER_PAGE = 60

# OCR output below this many chars for a full image/page is treated as
# unreliable — LOW_OCR_CONFIDENCE is flagged rather than guessing.
MIN_OCR_CHARS = 25


def _detect_ocr_language(text: str) -> str:
    """Script-based language hint for OCR / downstream multilingual handling."""
    if re.search(r"[\u0900-\u097F]", text or ""):
        return "hi"
    if re.search(r"[\u0C00-\u0C7F]", text or ""):
        return "te"
    return "en"


def _normalize_extracted_text(text: str) -> str:
    """Repair common PDF extraction artifacts without changing technical content."""
    if not text:
        return ""
    # Soft hyphens and zero-width chars
    text = text.replace("\u00ad", "").replace("\u200b", "").replace("\ufb01", "fi").replace("\ufb02", "fl")
    # Ligatures / fancy quotes that confuse regex extraction downstream
    text = text.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    # Collapse excessive whitespace but KEEP line structure (clause layout matters)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


class DocumentExtractionService:
    """Extracts text from tender documents (PDF/text) with OCR fallback."""

    def __init__(self) -> None:
        self._pdf_reader_available: Optional[bool] = None
        self._ocr_available: Optional[bool] = None

    # ------------------------------------------------------------------
    # Dependency probes (lazy, cached)
    # ------------------------------------------------------------------
    @property
    def pdf_available(self) -> bool:
        if self._pdf_reader_available is None:
            try:
                import pypdf  # noqa: F401
                self._pdf_reader_available = True
            except ImportError:
                self._pdf_reader_available = False
                logger.warning("pypdf not installed - PDF text extraction disabled.")
        return self._pdf_reader_available

    @property
    def ocr_available(self) -> bool:
        if self._ocr_available is None:
            try:
                import pytesseract  # noqa: F401
                import pdf2image  # noqa: F401
                # pytesseract needs the tesseract binary on PATH too
                import pytesseract
                pytesseract.get_tesseract_version()
                self._ocr_available = True
            except Exception:
                self._ocr_available = False
                logger.info("OCR dependencies (pytesseract/tesseract/pdf2image/poppler) not fully available - scanned PDFs will be flagged, not processed.")
        return self._ocr_available

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------
    def extract(
        self,
        filename: str,
        data: bytes,
        prefer_ocr: bool = False,
    ) -> Dict[str, Any]:
        """
        Returns:
            {
              "text": str,               # extracted machine-readable text ('' if none)
              "pages": int,              # page count (1 for txt)
              "method": str,             # pdf_text | ocr | text | none
              "needs_ocr": bool,         # scanned content detected but OCR unavailable
              "warnings": [str],
              "filename": str,
              "size_bytes": int,
            }
        """
        warnings: List[str] = []
        name = (filename or "upload").strip()
        lower = name.lower()

        if len(data) == 0:
            raise ValueError("Uploaded file is empty.")
        if len(data) > MAX_FILE_BYTES:
            raise ValueError(f"File exceeds the {MAX_FILE_BYTES // (1024*1024)} MB upload limit.")

        if lower.endswith(".txt"):
            text = _normalize_extracted_text(data.decode("utf-8", errors="replace"))
            return {
                "text": text, "pages": 1, "method": "text",
                "needs_ocr": False, "warnings": warnings,
                "filename": name, "size_bytes": len(data),
                "language": _detect_ocr_language(text),
                "low_ocr_confidence": False,
            }

        # ---- Image uploads (PNG/JPG) go straight to OCR ----------------
        if lower.endswith((".png", ".jpg", ".jpeg")):
            return self._extract_image(name, data, warnings)

        if not lower.endswith(".pdf"):
            raise ValueError("Unsupported file type. Upload a PDF, PNG, JPG or TXT tender document.")

        if not self.pdf_available:
            raise RuntimeError("PDF processing is unavailable: pypdf is not installed on the server.")

        return self._extract_pdf(name, data, prefer_ocr, warnings)

    # ------------------------------------------------------------------
    # Image pipeline: PNG/JPG -> OCR (never authoritative, never guessed)
    # ------------------------------------------------------------------
    def _extract_image(self, filename: str, data: bytes, warnings: List[str]) -> Dict[str, Any]:
        if not self.ocr_available:
            raise RuntimeError(
                "Image OCR is unavailable on this server (install pytesseract + "
                "tesseract binary + Pillow). Upload a text-based PDF or TXT instead."
            )
        text, ocr_warnings = self._ocr_images([data])
        warnings.extend(ocr_warnings)
        low_confidence = len(text.strip()) < MIN_OCR_CHARS
        if low_confidence:
            warnings.append(
                "LOW_OCR_CONFIDENCE: very little readable text was recovered from the "
                "image. Values shown must NOT be trusted — verify against the original document."
            )
            if not text.strip():
                text = ""
        return {
            "text": text,
            "pages": 1,
            "method": "ocr_image",
            "needs_ocr": False,
            "warnings": warnings,
            "filename": filename,
            "size_bytes": len(data),
            "language": _detect_ocr_language(text),
            "low_ocr_confidence": low_confidence,
        }

    # ------------------------------------------------------------------
    # PDF pipeline: text layer first, OCR fallback for scanned pages
    # ------------------------------------------------------------------
    def _extract_pdf(
        self,
        filename: str,
        data: bytes,
        prefer_ocr: bool,
        warnings: List[str],
    ) -> Dict[str, Any]:
        from pypdf import PdfReader

        try:
            reader = PdfReader(io.BytesIO(data))
        except Exception as exc:
            logger.warning("Unreadable PDF %s: %s", filename, exc)
            raise ValueError("The PDF could not be read. It may be corrupted or password-protected.")

        n_pages = len(reader.pages)
        if n_pages == 0:
            raise ValueError("The PDF contains no pages.")

        page_texts: List[str] = []
        pages_needing_ocr = 0

        for page in reader.pages:
            try:
                raw = page.extract_text() or ""
            except Exception:
                raw = ""
            cleaned = _normalize_extracted_text(raw)
            if len(cleaned) < MIN_CHARS_PER_PAGE:
                pages_needing_ocr += 1
            page_texts.append(cleaned)

        text_layer_chars = sum(len(t) for t in page_texts)
        text_layer_ratio = text_layer_chars / max(n_pages, 1)

        use_ocr = prefer_ocr or (text_layer_ratio < MIN_CHARS_PER_PAGE)
        method = "pdf_text"
        text = "\n\n".join(t for t in page_texts if t)

        if use_ocr:
            if self.ocr_available:
                ocr_text, ocr_warnings = self._ocr_pages(data, pages=range(n_pages))
                warnings.extend(ocr_warnings)
                if ocr_text.strip():
                    # OCR replaces a poor text layer; it is appended to a good one
                    if text_layer_ratio >= MIN_CHARS_PER_PAGE:
                        text = text + "\n\n" + ocr_text
                        method = "pdf_text+ocr"
                    else:
                        text = ocr_text
                        method = "ocr"
                else:
                    warnings.append("OCR produced no text; falling back to the PDF text layer.")
            else:
                warnings.append(
                    "Scanned/image-only pages detected but OCR is not configured on this server "
                    "(install pytesseract + tesseract binary + pdf2image/poppler)."
                )
                if not text:
                    method = "none"

        if pages_needing_ocr and method == "pdf_text":
            warnings.append(
                f"{pages_needing_ocr} of {n_pages} pages had little or no extractable text "
                "(possibly images/annexures)."
            )

        return {
            "text": text,
            "pages": n_pages,
            "method": method,
            "needs_ocr": bool(pages_needing_ocr and not text),
            "warnings": warnings,
            "filename": filename,
            "size_bytes": len(data),
            "language": _detect_ocr_language(text),
            "low_ocr_confidence": bool(use_ocr and self.ocr_available and len(text.strip()) < MIN_OCR_CHARS),
        }

    # ------------------------------------------------------------------
    # OCR path (only called when pytesseract + poppler are present)
    # ------------------------------------------------------------------
    def _ocr_pages(self, data: bytes, pages) -> tuple:
        warnings: List[str] = []
        texts: List[str] = []
        try:
            from pdf2image import convert_from_bytes
            from PIL import Image  # noqa: F401 - pdf2image returns PIL images

            images = convert_from_bytes(data, dpi=200)
            texts = self._ocr_images_data(images, warnings)
        except Exception as exc:
            warnings.append(f"OCR pipeline error: {exc}")
        return _normalize_extracted_text("\n\n".join(texts)), warnings

    def _ocr_images_data(self, images, warnings: List[str]) -> List[str]:
        import pytesseract
        texts: List[str] = []
        for img in images:
            try:
                texts.append(pytesseract.image_to_string(img))
            except Exception as exc:
                warnings.append(f"OCR failed on one page: {exc}")
        return texts

    def _ocr_images(self, image_bytes_list: List[bytes]) -> tuple:
        """OCR raw image bytes (PNG/JPG uploads)."""
        warnings: List[str] = []
        texts: List[str] = []
        try:
            import io as _io
            from PIL import Image
            images = [Image.open(_io.BytesIO(b)) for b in image_bytes_list]
            texts = self._ocr_images_data(images, warnings)
        except Exception as exc:
            warnings.append(f"Image OCR pipeline error: {exc}")
        return _normalize_extracted_text("\n\n".join(texts)), warnings


document_service = DocumentExtractionService()
