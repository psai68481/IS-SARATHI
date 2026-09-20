import { DashboardData, ExtractedRequirement, StandardRecommendation } from '@/types';

// Same-origin API path — Next.js rewrites proxy /api/v1/* to the FastAPI backend
// (next.config.js). Works on localhost AND behind any public tunnel/domain with
// zero client-side URL configuration.
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '/api/v1';

export async function analyzeTenderApi(
  query: string,
  department: string = 'Public Works Department (PWD)',
  includeStability: boolean = false
) {
  try {
    const res = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, department, include_stability: includeStability }),
    });

    if (!res.ok) {
      throw new Error(`API error: ${res.status}`);
    }

    return await res.json();
  } catch (error) {
    console.warn('Backend API unavailable, using client-side fallback:', error);
    return null;
  }
}

export async function analyzeTenderDocumentApi(
  file: File,
  department: string = 'Public Works Department (PWD)',
  includeStability: boolean = false,
  preferOcr: boolean = false
) {
  try {
    const form = new FormData();
    form.append('file', file);
    form.append('department', department);
    form.append('include_stability', includeStability ? 'true' : 'false');
    form.append('prefer_ocr', preferOcr ? 'true' : 'false');
    const res = await fetch(`${API_BASE_URL}/analyze-document`, {
      method: 'POST',
      body: form,
    });
    if (!res.ok) {
      const detail = await res.json().catch(() => null);
      throw new Error(detail?.detail || `API error: ${res.status}`);
    }
    return await res.json();
  } catch (error) {
    console.warn('Document upload API error:', error);
    throw error;
  }
}

export async function getDashboardStatsApi() {
  try {
    const res = await fetch(`${API_BASE_URL}/feedback/dashboard-stats`);
    if (res.ok) {
      return await res.json();
    }
  } catch (e) {
    console.warn('Dashboard stats API unavailable:', e);
  }
  return null;
}

export async function reportIncorrectRecommendationApi(payload: {
  case_id?: string;
  title?: string;
  tender_query: string;
  selected_standard: string;
  semantic_score?: number;
  comment: string;
}) {
  try {
    const res = await fetch(`${API_BASE_URL}/feedback/report-incorrect`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return await res.json();
  } catch (e) {
    console.warn('Report-incorrect API error:', e);
    return { status: 'error' };
  }
}

export async function getHistoricalDecisionsApi() {
  try {
    const res = await fetch(`${API_BASE_URL}/feedback/decisions`);
    if (res.ok) {
      return await res.json();
    }
  } catch (e) {
    console.warn('Feedback API unavailable:', e);
  }
  return null;
}

export async function submitDecisionFeedbackApi(feedback: any) {
  try {
    const res = await fetch(`${API_BASE_URL}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feedback),
    });
    return await res.json();
  } catch (e) {
    console.warn('Feedback submission error:', e);
    return { status: 'mock_success' };
  }
}
