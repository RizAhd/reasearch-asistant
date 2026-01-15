// Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';
const DEFAULT_QUERY = 'What is artificial intelligence?';

// DOM Elements
const queryInput = document.getElementById('queryInput');
const depthSelect = document.getElementById('depthSelect');
const researchBtn = document.getElementById('researchBtn');
const clearBtn = document.getElementById('clearBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingSection = document.getElementById('loadingSection');
const answerContent = document.getElementById('answerContent');
const sourcesContent = document.getElementById('sourcesContent');
const sourceCount = document.getElementById('sourceCount');
const jsonOutput = document.getElementById('jsonOutput');
const jsonContent = document.getElementById('jsonContent');
const toggleJsonBtn = document.getElementById('toggleJson');
const statsElement = document.getElementById('stats');
const apiStatusIndicator = document.getElementById('apiStatusIndicator');
const loaderText = document.getElementById('loaderText');
const wikiStatus = document.getElementById('wikiStatus');
const arxivStatus = document.getElementById('arxivStatus');
const newsStatus = document.getElementById('newsStatus');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Set default query
    queryInput.value = DEFAULT_QUERY;
    
    // Check API health
    checkAPIHealth();
    
    // Set up event listeners
    setupEventListeners();
    
    // Auto-resize textarea
    queryInput.addEventListener('input', autoResizeTextarea);
    autoResizeTextarea();
});

function setupEventListeners() {
    // Research button
    researchBtn.addEventListener('click', performResearch);
    
    // Enter key in textarea
    queryInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            performResearch();
        }
    });
    
    // Clear button
    clearBtn.addEventListener('click', clearResults);
    
    // Toggle JSON view
    toggleJsonBtn.addEventListener('click', toggleJsonView);
    
    // Source checkboxes
    document.querySelectorAll('input[name="source"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateResearchButton);
    });
}

function autoResizeTextarea() {
    queryInput.style.height = 'auto';
    queryInput.style.height = Math.min(queryInput.scrollHeight, 200) + 'px';
}

async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        apiStatusIndicator.textContent = 'Connected';
        apiStatusIndicator.className = 'status-indicator connected';
        
        console.log('API Health:', data);
    } catch (error) {
        apiStatusIndicator.textContent = 'Disconnected';
        apiStatusIndicator.className = 'status-indicator disconnected';
        
        console.error('API Health check failed:', error);
        
        // Show error in results if available
        if (resultsSection.style.display !== 'none') {
            answerContent.innerHTML = `
                <div class="error-message">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h4>API Connection Error</h4>
                    <p>Could not connect to the Research Assistant API. Make sure:</p>
                    <ul>
                        <li>The backend server is running</li>
                        <li>You're using the correct API URL</li>
                        <li>There are no network restrictions</li>
                    </ul>
                    <p>Error: ${error.message}</p>
                </div>
            `;
        }
    }
}

function updateResearchButton() {
    const checkedSources = Array.from(document.querySelectorAll('input[name="source"]:checked'));
    researchBtn.disabled = checkedSources.length === 0;
    researchBtn.innerHTML = researchBtn.disabled 
        ? '<i class="fas fa-ban"></i> Select at least one source'
        : '<i class="fas fa-search"></i> Start Research';
}

async function performResearch() {
    const query = queryInput.value.trim();
    
    if (!query) {
        alert('Please enter a research question');
        return;
    }
    
    // Get selected sources
    const selectedSources = Array.from(document.querySelectorAll('input[name="source"]:checked'))
        .map(cb => cb.value);
    
    if (selectedSources.length === 0) {
        alert('Please select at least one source');
        return;
    }
    
    // Show loading, hide results
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';
    
    // Reset status indicators
    resetStatusIndicators();
    
    // Prepare request data
    const requestData = {
        query: query,
        depth: depthSelect.value,
        include_sources: selectedSources,
        max_sources: 5
    };
    
    console.log('Sending request:', requestData);
    
    try {
        // Simulate source fetching progress
        simulateSourceFetching(selectedSources);
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/research`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`API returned ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Update all status indicators to complete
        updateAllStatusIndicators('complete');
        
        // Hide loading, show results
        setTimeout(() => {
            loadingSection.style.display = 'none';
            displayResults(data);
            resultsSection.style.display = 'block';
            scrollToResults();
        }, 500);
        
    } catch (error) {
        console.error('Research error:', error);
        
        loadingSection.style.display = 'none';
        
        answerContent.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <h4>Research Failed</h4>
                <p>${error.message}</p>
                <p>Please check:</p>
                <ul>
                    <li>Your internet connection</li>
                    <li>API keys configuration</li>
                    <li>Rate limits (free APIs have limits)</li>
                </ul>
                <button onclick="performResearch()" class="btn-primary">
                    <i class="fas fa-redo"></i> Try Again
                </button>
            </div>
        `;
        
        resultsSection.style.display = 'block';
    }
}

function resetStatusIndicators() {
    [wikiStatus, arxivStatus, newsStatus].forEach(el => {
        el.className = 'status-item pending';
        el.innerHTML = el.innerHTML.replace('✓', '<i class="fas fa-spinner fa-spin"></i>');
    });
}

function simulateSourceFetching(sources) {
    let progress = 0;
    const steps = ['Analyzing query...', 'Searching Wikipedia...', 'Fetching academic papers...', 
                   'Getting latest news...', 'Synthesizing information...'];
    
    const interval = setInterval(() => {
        if (progress < steps.length) {
            loaderText.textContent = steps[progress];
            progress++;
        } else {
            clearInterval(interval);
        }
    }, 800);
    
    // Update source status indicators
    sources.forEach(source => {
        setTimeout(() => {
            const element = document.getElementById(`${source}Status`);
            if (element) {
                element.className = 'status-item active';
                element.innerHTML = element.innerHTML.replace('fa-spinner fa-spin', 'fa-check');
            }
        }, Math.random() * 1500 + 1000);
    });
}

function updateAllStatusIndicators(status) {
    [wikiStatus, arxivStatus, newsStatus].forEach(el => {
        if (status === 'complete') {
            el.className = 'status-item active';
            el.innerHTML = el.innerHTML.replace('fa-spinner fa-spin', 'fa-check');
        }
    });
}

function displayResults(data) {
    // Display answer with formatted citations
    answerContent.innerHTML = formatAnswer(data.answer);
    
    // Display sources
    displaySources(data.sources);
    
    // Update source count
    sourceCount.textContent = data.sources.length;
    
    // Display stats
    displayStats(data);
    
    // Display raw JSON
    jsonOutput.textContent = JSON.stringify(data, null, 2);
    
    // Highlight JSON syntax
    highlightJSON();
}

function formatAnswer(answer) {
    // Convert markdown-like formatting to HTML
    let formatted = answer
        // Citations [1], [2]
        .replace(/\[(\d+)\]/g, '<sup class="citation">[$1]</sup>')
        // Bold text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Italic text
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        // Headers
        .replace(/^### (.*$)/gm, '<h4>$1</h4>')
        .replace(/^## (.*$)/gm, '<h3>$1</h3>')
        .replace(/^# (.*$)/gm, '<h2>$1</h2>')
        // Lists
        .replace(/^\s*[-*]\s+(.*$)/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
        // Paragraphs
        .replace(/\n\n/g, '</p><p>');
    
    // Wrap in paragraph if not already
    if (!formatted.startsWith('<')) {
        formatted = '<p>' + formatted + '</p>';
    }
    
    return formatted;
}

function displaySources(sources) {
    if (!sources || sources.length === 0) {
        sourcesContent.innerHTML = '<p class="no-sources">No sources found for this query.</p>';
        return;
    }
    
    sourcesContent.innerHTML = sources.map((source, index) => `
        <div class="source-item">
            <div class="source-title">${index + 1}. ${escapeHtml(source.title)}</div>
            <div class="source-meta">
                <span class="source-type">
                    <i class="fas fa-${getSourceIcon(source.source_type)}"></i>
                    ${capitalizeFirst(source.source_type)}
                </span>
                ${source.metadata && source.metadata.published 
                    ? `<span class="source-date">
                         <i class="far fa-calendar"></i>
                         ${source.metadata.published}
                       </span>`
                    : ''
                }
            </div>
            <div class="source-content">${truncateText(escapeHtml(source.content), 150)}</div>
            <a href="${source.url}" target="_blank" class="source-link">
                <i class="fas fa-external-link-alt"></i> View Source
            </a>
        </div>
    `).join('');
}

function displayStats(data) {
    statsElement.innerHTML = `
        <div class="stat-item">
            <i class="fas fa-clock"></i> ${data.processing_time}s
        </div>
        <div class="stat-item">
            <i class="fas fa-brain"></i> ${data.tokens_used} tokens
        </div>
        <div class="stat-item">
            <i class="fas fa-database"></i> ${data.sources.length} sources
        </div>
    `;
}

function getSourceIcon(sourceType) {
    const icons = {
        'wikipedia': 'wikipedia-w',
        'arxiv': 'graduation-cap',
        'news': 'newspaper'
    };
    return icons[sourceType] || 'file-alt';
}

function capitalizeFirst(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength).trim() + '...';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function highlightJSON() {
    const jsonString = jsonOutput.textContent;
    let highlighted = jsonString
        .replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|\b-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?\b)/g, 
            function(match) {
                let cls = 'json-number';
                if (/^"/.test(match)) {
                    if (/:$/.test(match)) {
                        cls = 'json-key';
                    } else {
                        cls = 'json-string';
                    }
                } else if (/true|false/.test(match)) {
                    cls = 'json-boolean';
                } else if (/null/.test(match)) {
                    cls = 'json-null';
                }
                return `<span class="${cls}">${match}</span>`;
            });
    
    jsonOutput.innerHTML = highlighted;
}

function toggleJsonView() {
    const isVisible = jsonContent.style.display !== 'none';
    jsonContent.style.display = isVisible ? 'none' : 'block';
    toggleJsonBtn.innerHTML = isVisible 
        ? '<i class="fas fa-eye"></i> Show' 
        : '<i class="fas fa-eye-slash"></i> Hide';
}

function clearResults() {
    queryInput.value = '';
    resultsSection.style.display = 'none';
    answerContent.innerHTML = '';
    sourcesContent.innerHTML = '';
    jsonOutput.textContent = '';
    statsElement.innerHTML = '';
    sourceCount.textContent = '0';
    autoResizeTextarea();
}

function scrollToResults() {
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Add some CSS for JSON highlighting
const style = document.createElement('style');
style.textContent = `
    .json-key { color: #f92672; }
    .json-string { color: #a6e22e; }
    .json-number { color: #ae81ff; }
    .json-boolean { color: #fd971f; }
    .json-null { color: #f92672; }
    .citation { 
        color: #4361ee;
        font-weight: bold;
        cursor: pointer;
    }
    .citation:hover {
        text-decoration: underline;
    }
    .error-message {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 10px;
        padding: 20px;
        color: #721c24;
    }
    .error-message i {
        font-size: 2rem;
        color: #dc3545;
        margin-bottom: 15px;
    }
    .error-message h4 {
        margin: 10px 0;
        color: #721c24;
    }
    .error-message ul {
        margin: 10px 0 10px 20px;
    }
    .no-sources {
        text-align: center;
        color: #6c757d;
        font-style: italic;
        padding: 40px 20px;
    }
`;
document.head.appendChild(style);