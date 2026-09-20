'use client';

import React, { useState } from 'react';
import Topbar from '@/components/layout/Topbar';
import Sidebar from '@/components/layout/Sidebar';
import ExportReportModal from '@/components/common/ExportReportModal';
import { GLOBAL_MOCK_DATA } from '@/data/mockData';
import { DashboardData } from '@/types';

// Tab components
import DashboardTab from '@/components/tabs/DashboardTab';
import TenderAnalysisTab from '@/components/tabs/TenderAnalysisTab';
import RecommendationsTab from '@/components/tabs/RecommendationsTab';
import RelatedStandardsTab from '@/components/tabs/RelatedStandardsTab';
import RequirementCoverageTab from '@/components/tabs/RequirementCoverageTab';
import ConflictsGapsTab from '@/components/tabs/ConflictsGapsTab';
import WhyNotTab from '@/components/tabs/WhyNotTab';
import HistoricalDecisionsTab from '@/components/tabs/HistoricalDecisionsTab';
import AIOverrideLearningTab from '@/components/tabs/AIOverrideLearningTab';

export default function Home() {
  const [data, setData] = useState<DashboardData>(GLOBAL_MOCK_DATA);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [activePreset, setActivePreset] = useState('helmet');
  const [customQuery, setCustomQuery] = useState(GLOBAL_MOCK_DATA.tenderQuery);
  const [isExportModalOpen, setIsExportModalOpen] = useState(false);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  const handleSelectPreset = (presetId: string) => {
    setActivePreset(presetId);
    const found = data.tenderPresets.find(p => p.id === presetId);
    if (found) {
      setCustomQuery(found.query);
      setData(prev => ({
        ...prev,
        tenderQuery: found.query
      }));
    }
  };

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardTab data={data} onNavigateTab={setActiveTab} />;
      case 'tender-analysis':
        return (
          <TenderAnalysisTab
            data={data}
            setData={setData}
            onNavigateTab={setActiveTab}
            customQuery={customQuery}
            setCustomQuery={setCustomQuery}
          />
        );
      case 'recommendations':
        return <RecommendationsTab data={data} onNavigateTab={setActiveTab} />;
      case 'related-standards':
        return <RelatedStandardsTab data={data} />;
      case 'coverage':
        return <RequirementCoverageTab data={data} onNavigateTab={setActiveTab} />;
      case 'conflicts-gaps':
        return <ConflictsGapsTab data={data} onNavigateTab={setActiveTab} />;
      case 'why-not':
        return <WhyNotTab data={data} onNavigateTab={setActiveTab} />;
      case 'history':
        return <HistoricalDecisionsTab data={data} onNavigateTab={setActiveTab} />;
      case 'learning':
        return <AIOverrideLearningTab data={data} />;
      default:
        return <DashboardTab data={data} onNavigateTab={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans text-slate-900">
      
      {/* Persistent Top Navigation Bar */}
      <Topbar
        activePreset={activePreset}
        onSelectPreset={handleSelectPreset}
        presets={data.tenderPresets}
        onExportReport={() => setIsExportModalOpen(true)}
        isMobileSidebarOpen={isMobileSidebarOpen}
        setIsMobileSidebarOpen={setIsMobileSidebarOpen}
      />

      {/* Main Body with Sidebar + Content Panel */}
      <div className="flex flex-1 relative overflow-hidden">
        
        {/* Left Sidebar Navigation */}
        <Sidebar
          activeTab={activeTab}
          onSelectTab={setActiveTab}
          isOpen={isMobileSidebarOpen}
          onClose={() => setIsMobileSidebarOpen(false)}
        />

        {/* Right Main Content Area */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto w-full">
          <div className="animate-in fade-in duration-150">
            {renderActiveTab()}
          </div>
        </main>

      </div>

      {/* Export Report / Certificate Modal */}
      <ExportReportModal
        isOpen={isExportModalOpen}
        onClose={() => setIsExportModalOpen(false)}
        data={data}
      />

    </div>
  );
}
