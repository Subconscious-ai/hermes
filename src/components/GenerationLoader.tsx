import { useEffect, useState } from 'react';
import { Brain, Users, Zap, Mail, CheckCircle2, Loader2 } from 'lucide-react';

interface LoadingPhase {
  id: string;
  icon: React.ReactNode;
  title: string;
  description: string;
  duration: number;
  status: 'pending' | 'active' | 'complete';
}

export const GenerationLoader = () => {
  const [phases, setPhases] = useState<LoadingPhase[]>([
    {
      id: 'audience',
      icon: <Users className="w-6 h-6" />,
      title: 'Analyzing your audience',
      description: 'Loading LinkedIn profiles and mapping to behavioral profiles...',
      duration: 30,
      status: 'active'
    },
    {
      id: 'simulation',
      icon: <Brain className="w-6 h-6" />,
      title: 'Running behavioral simulations',
      description: 'Testing messaging combinations across 1,200+ behavioral profiles...',
      duration: 60,
      status: 'pending'
    },
    {
      id: 'insights',
      icon: <Zap className="w-6 h-6" />,
      title: 'Identifying winning insights',
      description: 'Calculating causal drivers and engagement predictions...',
      duration: 20,
      status: 'pending'
    },
    {
      id: 'writing',
      icon: <Mail className="w-6 h-6" />,
      title: 'Writing your campaign',
      description: 'Generating email sequence based on proven insights...',
      duration: 30,
      status: 'pending'
    }
  ]);

  const [currentPhaseIndex, setCurrentPhaseIndex] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const phaseTimer = setInterval(() => {
      setPhases(prev => {
        const updated = [...prev];
        
        if (currentPhaseIndex < updated.length) {
          updated[currentPhaseIndex].status = 'complete';
          
          if (currentPhaseIndex + 1 < updated.length) {
            updated[currentPhaseIndex + 1].status = 'active';
            setCurrentPhaseIndex(currentPhaseIndex + 1);
          }
        }
        
        return updated;
      });
    }, phases[currentPhaseIndex]?.duration * 1000 || 30000);

    const progressTimer = setInterval(() => {
      setProgress(prev => {
        const increment = 100 / (phases[currentPhaseIndex]?.duration || 30);
        return prev >= 100 ? 0 : prev + increment;
      });
    }, 1000);

    return () => {
      clearInterval(phaseTimer);
      clearInterval(progressTimer);
    };
  }, [currentPhaseIndex, phases]);

  return (
    <div className="min-h-screen gradient-subtle flex items-center justify-center p-6">
      <div className="max-w-2xl w-full">
        
        <div className="bg-card rounded-2xl shadow-2xl p-12 border border-border">
          
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-purple-100 to-blue-100 rounded-full mb-6">
              <Loader2 className="w-10 h-10 text-primary animate-spin" />
            </div>
            <h1 className="text-3xl font-bold text-navy-900 mb-3">
              Creating Your Campaign
            </h1>
            <p className="text-gray-600">
              Our AI is analyzing behavioral patterns and generating high-converting copy
            </p>
          </div>

          <div className="space-y-6 mb-8">
            {phases.map((phase) => (
              <div
                key={phase.id}
                className={`flex items-start gap-4 transition-all duration-500 ${
                  phase.status === 'pending' ? 'opacity-40' : 'opacity-100'
                }`}
              >
                <div className={`
                  flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300
                  ${phase.status === 'complete' 
                    ? 'bg-green-100 text-green-600' 
                    : phase.status === 'active'
                    ? 'bg-purple-100 text-purple-600 animate-pulse'
                    : 'bg-gray-100 text-gray-400'
                  }
                `}>
                  {phase.status === 'complete' ? (
                    <CheckCircle2 className="w-6 h-6" />
                  ) : (
                    phase.icon
                  )}
                </div>

                <div className="flex-1 pt-1">
                  <h3 className={`font-semibold mb-1 transition-colors ${
                    phase.status === 'active' ? 'text-purple-600' : 'text-gray-900'
                  }`}>
                    {phase.title}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {phase.description}
                  </p>
                  
                  {phase.status === 'active' && (
                    <div className="mt-3">
                      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className="h-full gradient-primary transition-all duration-1000 ease-linear"
                          style={{ width: `${progress}%` }}
                        />
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex-shrink-0 pt-2">
                  {phase.status === 'complete' && (
                    <span className="text-xs font-medium text-success">
                      ✓ Done
                    </span>
                  )}
                  {phase.status === 'active' && (
                    <span className="text-xs font-medium text-purple-600 animate-pulse">
                      In progress...
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="pt-6 border-t border-border">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="text-gray-600">Overall Progress</span>
              <span className="font-semibold text-navy-900">
                {Math.round((currentPhaseIndex / phases.length) * 100)}%
              </span>
            </div>
            <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className="h-full gradient-success transition-all duration-500"
                style={{ width: `${(currentPhaseIndex / phases.length) * 100}%` }}
              />
            </div>
          </div>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-500">
              Estimated time remaining: <span className="font-medium text-gray-700">
                {Math.max(0, phases.slice(currentPhaseIndex).reduce((sum, p) => sum + p.duration, 0))} seconds
              </span>
            </p>
          </div>
        </div>

        <div className="mt-8 text-center">
          <div className="inline-block bg-card/80 backdrop-blur px-6 py-3 rounded-lg shadow-sm border border-border">
            <p className="text-sm text-gray-700">
              <span className="font-semibold text-primary">💡 Did you know?</span> Our simulations analyze{' '}
              <span className="font-semibold">3.5 million real behavioral patterns</span> to predict campaign performance with 93% accuracy
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
