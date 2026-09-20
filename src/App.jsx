import React, { useState } from 'react';
import Topbar from './components/layout/Topbar';
import Sidebar from './components/layout/Sidebar';
import ExportReportModal from './components/common/ExportReportModal';
import { GLOBAL_MOCK_DATA } from './data/mockData';

// Tab components
import DashboardTab from './components/tabs/DashboardTab';
import TenderAnalysisTab from './components/tabs/TenderAnalysisTab';
import RecommendationsTab from './components/tabs/RecommendationsTab';
import RelatedStandardsTab from './components/tabs/RelatedStandardsTab';
import RequirementCoverageTab from './components/tabs/RequirementCoverageTab';
import ConflictsGapsTab from './components/tabs/ConflictsGapsTab';
import WhyNotTab from './components/tabs/WhyNotTab';
import HistoricalDecisionsTab from './components/tabs/HistoricalDecisionsTab';
import AIOverrideLearningTab from './components/tabs/AIOverrideLearningTab';

export default function App() {
  const [appData, setAppData] = useState(GLOBAL_MOCK_DATA);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [activePreset, setActivePreset] = useState('helmet');
  const [customQuery, setCustomQuery] = useState(GLOBAL_MOCK_DATA.tenderQuery);
  const [isExportModalOpen, setIsExportModalOpen] = useState(false);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  const handleSelectPreset = (presetId) => {
    setActivePreset(presetId);
    const found = appData.tenderPresets.find(p => p.id === presetId);
    if (found) {
      setCustomQuery(found.query);
      setAppData(prev => ({ ...prev, tenderQuery: found.query }));
    }
  };

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardTab data={appData} onNavigateTab={setActiveTab} />;
      case 'tender-analysis':
        return (
          <TenderAnalysisTab
            data={appData}
            setData={setAppData}
            onNavigateTab={setActiveTab}
            customQuery={customQuery}
            setCustomQuery={setCustomQuery}
          />
        );
      case 'recommendations':
        return <RecommendationsTab data={appData} onNavigateTab={setActiveTab} />;
      case 'related-standards':
        return <RelatedStandardsTab data={appData} />;
      case 'coverage':
        return <RequirementCoverageTab data={appData} onNavigateTab={setActiveTab} />;
      case 'conflicts-gaps':
        return <ConflictsGapsTab data={appData} onNavigateTab={setActiveTab} />;
      case 'why-not':
        return <WhyNotTab data={appData} onNavigateTab={setActiveTab} />;
      case 'history':
        return <HistoricalDecisionsTab data={appData} onNavigateTab={setActiveTab} />;
      case 'learning':
        return <AIOverrideLearningTab data={appData} />;
      default:
        return <DashboardTab data={appData} onNavigateTab={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans text-slate-900">
      
      {/* Persistent Top Navigation Bar */}
      <Topbar
        activePreset={activePreset}
        onSelectPreset={handleSelectPreset}
        presets={appData.tenderPresets}
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
        data={appData}
      />

    </div>
  );
}
