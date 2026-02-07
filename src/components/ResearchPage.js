import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const ResearchPage = () => {
  const navigate = useNavigate();
  const [darkMode, setDarkMode] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [timeRange, setTimeRange] = useState('7');
  const [reportLength, setReportLength] = useState('medium');
  const [keywords, setKeywords] = useState('');
  const [numberOfSources, setNumberOfSources] = useState('10');
  const [outputFormat, setOutputFormat] = useState('markdown');
  const [searchHistory, setSearchHistory] = useState([
    { time: '14:32:15', query: 'AI market trends', status: 'completed', sources: 15 },
    { time: '14:28:42', query: 'blockchain technology 2024', status: 'completed', sources: 22 },
    { time: '14:15:18', query: 'renewable energy investments', status: 'completed', sources: 18 },
    { time: '13:52:33', query: 'quantum computing applications', status: 'in-progress', sources: 0 }
  ]);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    // This effect can be used for future search history updates
  }, []);

  const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchQuery(value);
    setIsSearching(value.length > 0);
  };

  const handleStartResearch = () => {
    const researchData = {
      query: searchQuery,
      timeRange,
      reportLength,
      keywords: keywords.split(',').map(k => k.trim()).filter(k => k),
      numberOfSources,
      outputFormat,
      timestamp: new Date().toISOString()
    };
    
    // Add to search history
    const newSearchEntry = {
      time: new Date().toLocaleTimeString(),
      query: searchQuery,
      status: 'in-progress',
      sources: 0
    };
    setSearchHistory(prev => [newSearchEntry, ...prev.slice(0, 9)]);
    
    localStorage.setItem('researchData', JSON.stringify(researchData));
    navigate('/output');
  };

  const handleKeywordChange = (e) => {
    const value = e.target.value;
    const keywordArray = value.split(',').map(k => k.trim()).filter(k => k);
    if (keywordArray.length <= 10) {
      setKeywords(value);
    }
  };

  return (
    <div className="dark-container">
      {/* Header */}
      <div style={{ position: 'relative', zIndex: 10, padding: '20px 40px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 className="glow-text" style={{ fontSize: '48px', fontWeight: 'bold', margin: 0 }}>
            NOVA
          </h1>
          <div className="toggle-switch active" onClick={() => setDarkMode(!darkMode)} />
        </div>
        <p style={{ marginTop: '10px', color: 'rgba(255, 255, 255, 0.7)', fontSize: '16px' }}>
          Advanced Research Intelligence Platform - Transform data into actionable insights
        </p>
      </div>

      {/* Main Content */}
      <div style={{ position: 'relative', zIndex: 10, display: 'flex', padding: '0 40px', gap: '30px' }}>
        
        {/* Left Panel - Intelligence Stream */}
        <div style={{ flex: '0 0 300px' }}>
          <div className="card">
            <h3 style={{ color: '#9333ea', marginBottom: '15px', fontSize: '18px' }}>
              Intelligence Stream
            </h3>
            <div style={{ marginBottom: '20px' }}>
              <h4 style={{ color: 'rgba(255, 255, 255, 0.8)', marginBottom: '10px', fontSize: '14px' }}>
                Search History
              </h4>
              <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
                {searchHistory.map((search, index) => (
                  <div key={index} className="log-entry">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <span style={{ color: '#9333ea' }}>{search.time}</span> - {search.query}
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span 
                          style={{ 
                            fontSize: '10px', 
                            padding: '2px 6px', 
                            borderRadius: '3px',
                            background: search.status === 'completed' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(245, 158, 11, 0.2)',
                            color: search.status === 'completed' ? '#10b981' : '#f59e0b'
                          }}
                        >
                          {search.status}
                        </span>
                        {search.sources > 0 && (
                          <span style={{ fontSize: '11px', color: 'rgba(255, 255, 255, 0.6)' }}>
                            {search.sources} sources
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h4 style={{ color: 'rgba(255, 255, 255, 0.8)', marginBottom: '10px', fontSize: '14px' }}>
                Knowledge Bin
              </h4>
              <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.6)' }}>
                <p>Stored insights: 1,247</p>
                <p>Recent topics: AI trends, market analysis</p>
                <p>Last sync: 2 minutes ago</p>
              </div>
            </div>
          </div>
        </div>

        {/* Center - Purple Sphere and Search */}
        <div style={{ flex: 1, textAlign: 'center', position: 'relative' }}>
          <div className="purple-sphere" style={{ animation: isSearching ? 'morph 1s ease-in-out infinite, pulse 0.5s ease-in-out infinite' : 'bounce 2s ease-in-out infinite, pulse 2s ease-in-out infinite, morph 4s ease-in-out infinite' }} />
          
          {/* Search Input */}
          <div style={{ position: 'relative', zIndex: 20, marginTop: '350px' }}>
            <h2 style={{ color: 'rgba(255, 255, 255, 0.9)', marginBottom: '20px' }}>
              What would you like NOVA to research today?
            </h2>
            <input
              type="text"
              className="form-input"
              placeholder="Enter your research query..."
              value={searchQuery}
              onChange={handleSearchChange}
              style={{ maxWidth: '600px', fontSize: '16px' }}
            />
          </div>

          {/* Action Buttons */}
          <div style={{ position: 'relative', zIndex: 20, marginTop: '30px' }}>
            <button className="btn-primary" onClick={handleStartResearch}>
              Initialize Research
            </button>
            <div style={{ marginTop: '15px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
              <button className="btn-secondary">Market Intel</button>
              <button className="btn-secondary">Tech Deep-Dive</button>
              <button className="btn-secondary">Competitive Analysis</button>
            </div>
          </div>
        </div>

        {/* Right Panel - Report Canvas */}
        <div style={{ flex: '0 0 300px' }}>
          <div className="card">
            <h3 style={{ color: '#9333ea', marginBottom: '15px', fontSize: '18px' }}>
              Report Canvas
            </h3>
            <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.6)' }}>
              <p>Reports generated: 89</p>
              <p>Active research: 3</p>
              <p>Queue position: None</p>
            </div>
          </div>
        </div>
      </div>

      {/* Research Configuration */}
      <div style={{ position: 'relative', zIndex: 10, padding: '40px', marginTop: '20px' }}>
        <div className="card">
          <h3 style={{ color: '#9333ea', marginBottom: '20px' }}>Research Configuration</h3>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
            
            {/* Time Range */}
            <div>
              <label style={{ display: 'block', marginBottom: '8px', color: 'rgba(255, 255, 255, 0.8)' }}>
                Time Range (days)
              </label>
              <select 
                className="form-input" 
                value={timeRange} 
                onChange={(e) => setTimeRange(e.target.value)}
              >
                <option value="1">Last 24 hours</option>
                <option value="7">Last 7 days</option>
                <option value="30">Last 30 days</option>
                <option value="90">Last 90 days</option>
                <option value="365">Last year</option>
              </select>
            </div>

            {/* Report Length */}
            <div>
              <label style={{ display: 'block', marginBottom: '8px', color: 'rgba(255, 255, 255, 0.8)' }}>
                Report Length
              </label>
              <select 
                className="form-input" 
                value={reportLength} 
                onChange={(e) => setReportLength(e.target.value)}
              >
                <option value="brief">Brief (1-2 pages)</option>
                <option value="medium">Medium (3-5 pages)</option>
                <option value="detailed">Detailed (6-10 pages)</option>
                <option value="comprehensive">Comprehensive (10+ pages)</option>
              </select>
            </div>

            {/* Number of Sources */}
            <div>
              <label style={{ display: 'block', marginBottom: '8px', color: 'rgba(255, 255, 255, 0.8)' }}>
                Number of Sources
              </label>
              <select 
                className="form-input" 
                value={numberOfSources} 
                onChange={(e) => setNumberOfSources(e.target.value)}
              >
                <option value="5">5 sources</option>
                <option value="10">10 sources</option>
                <option value="20">20 sources</option>
                <option value="50">50 sources</option>
                <option value="100">100 sources</option>
              </select>
            </div>

            {/* Output Format */}
            <div>
              <label style={{ display: 'block', marginBottom: '8px', color: 'rgba(255, 255, 255, 0.8)' }}>
                Output Format
              </label>
              <select 
                className="form-input" 
                value={outputFormat} 
                onChange={(e) => setOutputFormat(e.target.value)}
              >
                <option value="pdf">PDF</option>
                <option value="markdown">Markdown</option>
                <option value="essay">Essay</option>
                <option value="json">JSON</option>
                <option value="csv">CSV</option>
              </select>
            </div>
          </div>

          {/* Keywords */}
          <div style={{ marginTop: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: 'rgba(255, 255, 255, 0.8)' }}>
              Preferred Keywords (limit 10)
            </label>
            <textarea
              className="form-input"
              placeholder="Enter keywords separated by commas..."
              value={keywords}
              onChange={handleKeywordChange}
              rows={3}
            />
            <div style={{ marginTop: '10px' }}>
              {keywords.split(',').map((keyword, index) => 
                keyword.trim() && (
                  <span key={index} className="keyword-tag">
                    {keyword.trim()}
                  </span>
                )
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResearchPage;
