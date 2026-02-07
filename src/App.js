import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ResearchPage from './components/ResearchPage';
import OutputPage from './components/OutputPage';
import './index.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<ResearchPage />} />
          <Route path="/output" element={<OutputPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
