import { useState } from 'react';
import { CampaignInputForm } from '@/components/CampaignInputForm';
import { GenerationLoader } from '@/components/GenerationLoader';

interface FormData {
  productDescription: string;
  targetAudience: string;
}

const Index = () => {
  const [currentView, setCurrentView] = useState<'input' | 'loading'>('input');
  const [campaignData, setCampaignData] = useState<FormData | null>(null);

  const handleFormSubmit = (data: FormData) => {
    setCampaignData(data);
    setCurrentView('loading');
  };

  return (
    <>
      {currentView === 'input' && (
        <CampaignInputForm onSubmit={handleFormSubmit} />
      )}
      {currentView === 'loading' && (
        <GenerationLoader />
      )}
    </>
  );
};

export default Index;
