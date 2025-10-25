import { useState } from 'react';
import { Sparkles, Users, Package, MessageSquare, ArrowRight } from 'lucide-react';

interface FormData {
  productDescription: string;
  targetAudience: string;
}

interface CampaignInputFormProps {
  onSubmit: (data: FormData) => void;
}

export const CampaignInputForm = ({ onSubmit }: CampaignInputFormProps) => {
  const [formData, setFormData] = useState<FormData>({
    productDescription: '',
    targetAudience: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isGenerating, setIsGenerating] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const newErrors: Record<string, string> = {};
    
    if (formData.productDescription.length < 100) {
      newErrors.productDescription = 'Please provide at least 100 characters';
    }
    
    const urlCount = formData.targetAudience.split('\n').filter(line => 
      line.trim().startsWith('https://linkedin.com')
    ).length;
    
    if (urlCount < 5) {
      newErrors.targetAudience = 'Please provide at least 5 LinkedIn URLs';
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    setIsGenerating(true);
    onSubmit(formData);
  };

  return (
    <div className="min-h-screen gradient-subtle">
      <header className="bg-card border-b border-border">
        <div className="max-w-4xl mx-auto px-6 py-6">
          <div className="flex items-center gap-3">
            <Sparkles className="w-8 h-8 text-primary" />
            <h1 className="text-2xl font-bold text-navy-900">
              Campaign Generator
            </h1>
          </div>
          <p className="mt-2 text-gray-600">
            Create data-backed email campaigns in minutes
          </p>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-12">
        <form onSubmit={handleSubmit} className="space-y-8">
          
          <section className="group bg-card rounded-xl shadow-lg border border-border p-8 transition-all duration-300 hover:shadow-2xl hover:border-primary/20 hover:-translate-y-1 animate-fade-in">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-gradient-to-br from-purple-100 to-purple-50 rounded-lg group-hover:scale-110 transition-transform duration-300">
                <Package className="w-6 h-6 text-purple-600" />
              </div>
              <div className="flex-1">
                <h2 className="text-xl font-semibold text-navy-900 mb-2">
                  Product Description
                </h2>
                <p className="text-gray-600 text-sm mb-4">
                  Describe your product, its main benefits, and what makes it unique
                </p>
                
                <textarea
                  value={formData.productDescription}
                  onChange={(e) => setFormData({...formData, productDescription: e.target.value})}
                  placeholder="e.g., TaskFlow AI is an intelligent project management tool that automatically prioritizes tasks based on deadlines, dependencies, and team capacity. Unlike traditional tools, our AI engine learns from your team's patterns to surface the most critical work first, saving managers 10+ hours per week on manual task sorting..."
                  className="w-full h-40 px-4 py-3 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent resize-none text-foreground placeholder:text-gray-400 bg-background transition-all"
                />
                
                <div className="flex items-center justify-between mt-2">
                  <span className={`text-sm transition-colors ${formData.productDescription.length >= 100 ? 'text-success' : 'text-gray-500'}`}>
                    {formData.productDescription.length} / 100 characters minimum
                  </span>
                  {errors.productDescription && (
                    <span className="text-sm text-destructive">
                      {errors.productDescription}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </section>

          <section className="group bg-card rounded-xl shadow-lg border border-border p-8 transition-all duration-300 hover:shadow-2xl hover:border-secondary/20 hover:-translate-y-1 animate-fade-in [animation-delay:100ms]">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-gradient-to-br from-blue-100 to-blue-50 rounded-lg group-hover:scale-110 transition-transform duration-300">
                <Users className="w-6 h-6 text-blue-600" />
              </div>
              <div className="flex-1">
                <h2 className="text-xl font-semibold text-navy-900 mb-2">
                  Target Audience
                </h2>
                <p className="text-gray-600 text-sm mb-4">
                  Paste LinkedIn profile URLs of your ideal customers (one per line, minimum 5)
                </p>
                
                <textarea
                  value={formData.targetAudience}
                  onChange={(e) => setFormData({...formData, targetAudience: e.target.value})}
                  placeholder="https://linkedin.com/in/startup-founder-example&#10;https://linkedin.com/in/marketing-director-saas&#10;https://linkedin.com/in/vp-growth-series-a&#10;https://linkedin.com/in/head-of-marketing-tech&#10;https://linkedin.com/in/cmo-b2b-software"
                  className="w-full h-32 px-4 py-3 border border-input rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent resize-none text-foreground font-mono text-sm placeholder:text-gray-400 placeholder:font-sans bg-background transition-all"
                />
                
                <div className="flex items-center justify-between mt-2">
                  <span className="text-sm text-gray-500">
                    {formData.targetAudience.split('\n').filter(line => 
                      line.trim().startsWith('https://linkedin.com')
                    ).length} LinkedIn URLs detected
                  </span>
                  {errors.targetAudience && (
                    <span className="text-sm text-destructive">
                      {errors.targetAudience}
                    </span>
                  )}
                </div>
                
                <div className="mt-4 p-4 bg-gradient-to-br from-blue-50 to-cyan-50 border border-blue-200 rounded-lg hover:shadow-md transition-all duration-300">
                  <p className="text-sm text-blue-900">
                    <strong>💡 Why LinkedIn profiles?</strong> Our behavioral simulation analyzes real profile data to understand your audience's decision-making patterns, roles, and preferences—making predictions far more accurate than demographic guesses.
                  </p>
                </div>
              </div>
            </div>
          </section>

          <div className="flex justify-center pt-8">
            <button
              type="submit"
              disabled={isGenerating}
              className="group relative flex items-center gap-3 px-10 py-5 gradient-primary text-white font-semibold rounded-2xl shadow-2xl hover:shadow-[0_20px_60px_-15px_rgba(147,51,234,0.5)] hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 overflow-hidden animate-fade-in [animation-delay:200ms]"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
              <Sparkles className="w-6 h-6 group-hover:rotate-12 transition-transform duration-300" />
              <span className="text-lg relative">Generate My Campaign</span>
              <ArrowRight className="w-6 h-6 group-hover:translate-x-2 transition-transform duration-300" />
            </button>
          </div>
          
          <div className="text-center pt-6 animate-fade-in [animation-delay:300ms]">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-muted/50 rounded-full border border-border/50">
              <div className="w-2 h-2 bg-success rounded-full animate-pulse" />
              <p className="text-sm text-muted-foreground">
                Generation typically takes 2-3 minutes • Uses behavioral simulation from 3.5M+ real users
              </p>
            </div>
          </div>
        </form>
      </main>
    </div>
  );
};
