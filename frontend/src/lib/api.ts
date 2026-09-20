import { DashboardData, ExtractedRequirement, StandardRecommendation } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export async function analyzeTenderApi(query: string, department: string = 'Public Works Department (PWD)') {
  try {
    const res = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, department }),
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
