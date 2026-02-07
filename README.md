# NOVA Research Intelligence Platform

A React frontend for an advanced research intelligence platform with a beautiful dark theme and animated purple sphere.

## Features

### Research Input Page
- **NOVA Heading** with glowing text effect
- **Animated Purple Sphere** with floating and pulsing animations
- **Search Input** for research queries
- **Intelligence Stream** panel with live logs and knowledge bin
- **Report Canvas** panel showing research statistics
- **Research Configuration** with:
  - Time range selection (1 day to 1 year)
  - Report length options (brief to comprehensive)
  - Number of sources (5 to 100)
  - Output format (PDF, Markdown, Essay, JSON, CSV)
  - Keywords input with 10-keyword limit
- **Action Buttons** for quick research topics

### Output Page
- **Research Report** display with generation progress
- **Executive Summary** with key findings
- **Sources Analysis** showing relevance scores
- **Key Insights** with categorized information
- **Download functionality** (ready for FastAPI integration)
- **Timestamp and metadata** display

## Technical Stack

- **React 18** with modern hooks
- **React Router** for navigation
- **CSS animations** for the purple sphere
- **Dark theme** with purple accent colors
- **Responsive design** with grid layouts
- **Local storage** for data persistence

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view the application.

## FastAPI Integration

The frontend is designed to integrate seamlessly with a FastAPI backend. Here are the integration points:

### Research Submission
When the "Initialize Research" button is clicked, the research data is stored in localStorage and the user is redirected to the output page. For FastAPI integration, modify the `handleStartResearch` function in `ResearchPage.js`:

```javascript
const handleStartResearch = async () => {
  const researchData = {
    query: searchQuery,
    timeRange,
    reportLength,
    keywords: keywords.split(',').map(k => k.trim()).filter(k => k),
    numberOfSources,
    outputFormat
  };
  
  try {
    const response = await fetch('http://your-fastapi-endpoint/research', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(researchData)
    });
    
    const result = await response.json();
    localStorage.setItem('researchData', JSON.stringify(result));
    navigate('/output');
  } catch (error) {
    console.error('Error submitting research:', error);
  }
};
```

### Download Integration
The download function in `OutputPage.js` can be connected to your FastAPI endpoint:

```javascript
const handleDownload = async () => {
  try {
    const response = await fetch(`http://your-fastapi-endpoint/download/${researchData.id}`, {
      method: 'GET',
    });
    
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `research-report.${researchData.outputFormat}`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } catch (error) {
    console.error('Error downloading report:', error);
  }
};
```

## Customization

### Colors and Theme
The dark theme and purple colors can be customized in `src/index.css`. The main color variables are:
- `#9333ea` - Primary purple
- `#6b21a8` - Darker purple
- `#4c1d95` - Darkest purple
- `#a855f7` - Lighter purple

### Animations
The purple sphere animations are defined in the `.purple-sphere` class and can be adjusted for speed and intensity.

## File Structure

```
src/
├── components/
│   ├── ResearchPage.js    # Main research input page
│   └── OutputPage.js      # Research results page
├── App.js                 # Main app component with routing
├── index.css              # Global styles and animations
└── index.js               # App entry point
```

## Performance

The application uses React's built-in optimization features:
- Functional components with hooks
- Efficient state management
- CSS animations for smooth performance
- Minimal re-renders with proper state handling

## Browser Support

The application supports all modern browsers including:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
