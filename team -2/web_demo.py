import asyncio
from flask import Flask, render_template_string, request, jsonify
from web_search import search_multiple_queries
import json

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔍 Web Search Module - Team Member 3</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .search-section {
            padding: 40px;
            background: #f8fafc;
        }
        
        .search-form {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .query-input {
            flex: 1;
            min-width: 250px;
            padding: 15px 20px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .query-input:focus {
            outline: none;
            border-color: #4f46e5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
        
        .search-btn {
            padding: 15px 30px;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .search-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(79, 70, 229, 0.3);
        }
        
        .search-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .add-query-btn {
            padding: 15px 20px;
            background: #10b981;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .add-query-btn:hover {
            background: #059669;
        }
        
        .results-section {
            padding: 0 40px 40px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            font-size: 18px;
            color: #64748b;
        }
        
        .result-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .result-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-color: #4f46e5;
        }
        
        .result-title {
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 8px;
            line-height: 1.4;
        }
        
        .result-url {
            font-size: 14px;
            color: #64748b;
            word-break: break-all;
        }
        
        .stats {
            background: #f1f5f9;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 24px;
            font-weight: 700;
            color: #4f46e5;
        }
        
        .stat-label {
            font-size: 14px;
            color: #64748b;
            margin-top: 5px;
        }
        
        .json-output {
            background: #1e293b;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin-top: 20px;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .team-info {
            background: #fef3c7;
            border: 1px solid #f59e0b;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        .team-info h3 {
            color: #92400e;
            margin-bottom: 10px;
        }
        
        .team-info p {
            color: #78350f;
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Web Search Module</h1>
            <p>Team Member 3 - Async Multi-Query Search Engine</p>
        </div>
        
        <div class="search-section">
            <div class="team-info">
                <h3>📋 Module Info</h3>
                <p><strong>Main Function:</strong> <code>async def search_multiple_queries(queries: list[str]) -> list[dict]</code></p>
                <p><strong>Output Format:</strong> List of dictionaries with 'url' and 'title' keys for Team 4</p>
                <p><strong>Search Engines:</strong> SerpAPI → Bing API → DuckDuckGo → Brave → Google</p>
            </div>
            
            <form class="search-form" id="searchForm">
                <div id="queryInputs">
                    <input type="text" class="query-input" placeholder="Enter search query..." value="AI in healthcare">
                    <input type="text" class="query-input" placeholder="Enter another query..." value="machine learning in hospitals">
                </div>
                <button type="button" class="add-query-btn" onclick="addQueryInput()">+ Add Query</button>
                <button type="submit" class="search-btn" id="searchBtn">🔍 Search</button>
            </form>
        </div>
        
        <div class="results-section">
            <div id="results"></div>
        </div>
    </div>
    
    <script>
        function addQueryInput() {
            const queryInputs = document.getElementById('queryInputs');
            const newInput = document.createElement('input');
            newInput.type = 'text';
            newInput.className = 'query-input';
            newInput.placeholder = 'Enter search query...';
            queryInputs.appendChild(newInput);
        }
        
        document.getElementById('searchForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const searchBtn = document.getElementById('searchBtn');
            const resultsDiv = document.getElementById('results');
            
            // Get all query values
            const queryInputs = document.querySelectorAll('.query-input');
            const queries = Array.from(queryInputs)
                .map(input => input.value.trim())
                .filter(query => query.length > 0);
            
            if (queries.length === 0) {
                alert('Please enter at least one search query');
                return;
            }
            
            // Show loading
            searchBtn.disabled = true;
            searchBtn.textContent = '🔄 Searching...';
            resultsDiv.innerHTML = '<div class="loading">🔍 Searching multiple engines... This may take a few seconds...</div>';
            
            try {
                const response = await fetch('/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ queries: queries })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    resultsDiv.innerHTML = `<div style="color: red; padding: 20px;">❌ Error: ${data.error}</div>`;
                } else {
                    displayResults(data);
                }
                
            } catch (error) {
                resultsDiv.innerHTML = `<div style="color: red; padding: 20px;">❌ Network error: ${error.message}</div>`;
            } finally {
                searchBtn.disabled = false;
                searchBtn.textContent = '🔍 Search';
            }
        });
        
        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            
            let html = `
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-number">${data.queries_searched}</div>
                        <div class="stat-label">Queries Searched</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${data.total_results}</div>
                        <div class="stat-label">Results Found</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${data.search_time.toFixed(2)}s</div>
                        <div class="stat-label">Search Time</div>
                    </div>
                </div>
            `;
            
            if (data.results.length === 0) {
                html += '<div style="text-align: center; padding: 40px; color: #64748b;">No results found. Try different queries.</div>';
            } else {
                data.results.forEach((result, index) => {
                    html += `
                        <div class="result-card" onclick="window.open('${result.url}', '_blank')">
                            <div class="result-title">${index + 1}. ${result.title}</div>
                            <div class="result-url">🔗 ${result.url}</div>
                        </div>
                    `;
                });
                
                // Add JSON output for Team 4
                html += `
                    <h3 style="margin-top: 30px; margin-bottom: 10px; color: #1e293b;">📤 Output for Team 4 (JSON Format):</h3>
                    <div class="json-output">${JSON.stringify(data.results, null, 2)}</div>
                `;
            }
            
            resultsDiv.innerHTML = html;
        }
        
        // Auto-search on page load
        window.addEventListener('load', () => {
            setTimeout(() => {
                document.getElementById('searchForm').dispatchEvent(new Event('submit'));
            }, 500);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        queries = data.get('queries', [])
        
        if not queries:
            return jsonify({'error': 'No queries provided'}), 400
        
        # Run async search
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        import time
        start_time = time.time()
        results = loop.run_until_complete(search_multiple_queries(queries))
        search_time = time.time() - start_time
        
        loop.close()
        
        return jsonify({
            'queries_searched': len(queries),
            'total_results': len(results),
            'search_time': search_time,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Web Search Module Demo Server")
    print("🌐 Open http://localhost:8000 in your browser")
    print("🔍 This will visually demonstrate the search functionality")
    app.run(debug=True, host='0.0.0.0', port=8000)
