// Configuration
const API_BASE_URL = window.location.origin + '/api/v1';
const DEFAULT_QUERY = 'What is artificial intelligence?';

// DOM Elements
const queryInput = document.getElementById('queryInput');
const researchBtn = document.getElementById('researchBtn');
const clearBtn = document.getElementById('clearBtn');
const resultsSection = document.getElementById('resultsSection');
const progressSection = document.getElementById('progressSection');
const answerContent = document.getElementById('answerContent');
const sourcesContent = document.getElementById('sourcesContent');
const sourceCount = document.getElementById('sourceCount');
const apiStatus = document.getElementById('apiStatus');
const charCounter = document.getElementById('charCounter');
const progressTimer = document.getElementById('progressTimer');
const depthBtns = document.querySelectorAll('.depth-btn');
const sourceCheckboxes = document.querySelectorAll('input[name="source"]');
const themeToggle = document.getElementById('themeToggle');

// Progress step elements
const stepAnalyze = document.getElementById('stepAnalyze');
const stepWikipedia = document.getElementById('stepWikipedia');
const stepNews = document.getElementById('stepNews');
const stepAI = document.getElementById('stepAI');
const stepAnalyzeStatus = document.getElementById('stepAnalyzeStatus');
const stepWikipediaStatus = document.getElementById('stepWikipediaStatus');
const stepNewsStatus = document.getElementById('stepNewsStatus');
const stepAIStatus = document.getElementById('stepAIStatus');

// State
let currentDepth = 'balanced';
let startTime = null;
let timerInterval = null;

// ===== THEME MANAGEMENT =====
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    queryInput.value = DEFAULT_QUERY;
    updateCharCounter();
    checkAPIHealth();
    setupEventListeners();
    autoResizeTextarea();
});

function setupEventListeners() {
    // Theme toggle
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Research button
    researchBtn.addEventListener('click', performResearch);
    
    // Enter key in textarea (Ctrl+Enter or Cmd+Enter)
    queryInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
            e.preventDefault();
            performResearch();
        }
    });
    
    // Character counter
    queryInput.addEventListener('input', () => {
        autoResizeTextarea();
        updateCharCounter();
    });
    
    // Clear button
    clearBtn.addEventListener('click', clearAll);
    
    // Depth selector
    depthBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            depthBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentDepth = btn.dataset.depth;
        });
    });
    
    // Source checkboxes
    sourceCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateResearchButton);
    });
    
    updateResearchButton();
}

function autoResizeTextarea() {
    queryInput.style.height = 'auto';
    queryInput.style.height = Math.min(queryInput.scrollHeight, 200) + 'px';
}

function updateCharCounter() {
    const length = queryInput.value.length;
    charCounter.textContent = `${length}/500`;
}

function updateResearchButton() {
    const checkedSources = Array.from(sourceCheckboxes).filter(cb => cb.checked);
    researchBtn.disabled = checkedSources.length === 0;
}

async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        
        if (response.ok) {
            const statusDot = apiStatus.querySelector('.status-dot');
            const statusText = apiStatus.querySelector('.status-text');
            statusDot.style.background = '#10A37F';
            statusText.textContent = 'Connected';
        } else {
            throw new Error('Health check failed');
        }
    } catch (error) {
        const statusDot = apiStatus.querySelector('.status-dot');
        const statusText = apiStatus.querySelector('.status-text');
        statusDot.style.background = '#ef4444';
        statusText.textContent = 'Disconnected';
    }
}

async function performResearch() {
    const query = queryInput.value.trim();
    
    if (!query) {
        showError('Please enter a research question');
        return;
    }
    
    const selectedSources = Array.from(sourceCheckboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);
    
    if (selectedSources.length === 0) {
        showError('Please select at least one source');
        return;
    }
    
    // Hide results, show progress
    resultsSection.style.display = 'none';
    progressSection.style.display = 'block';
    resetProgress();
    
    // Start timer
    startTimer();
    
    // Prepare request data
    const requestData = {
        query: query,
        depth: currentDepth,
        include_sources: selectedSources,
        max_sources: currentDepth === 'deep' ? 8 : currentDepth === 'quick' ? 3 : 5
    };
    
    try {
        // Step 1: Analyzing
        updateStep('analyze', 'active', 'Processing...');
        
        // Step 2: Wikipedia
        if (selectedSources.includes('wikipedia')) {
            updateStep('wikipedia', 'active', 'Searching...');
            await new Promise(r => setTimeout(r, 800));
            updateStep('wikipedia', 'completed', 'Complete');
        }
        
        // Step 3: News
        if (selectedSources.includes('news')) {
            updateStep('news', 'active', 'Fetching...');
            await new Promise(r => setTimeout(r, 1200));
            updateStep('news', 'completed', 'Complete');
        }
        
        // Step 4: AI Synthesis
        updateStep('ai', 'active', 'Generating answer...');
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/research`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `API returned ${response.status}`);
        }
        
        const data = await response.json();
        
        // Complete AI step
        updateStep('ai', 'completed', 'Complete');
        
        // Stop timer
        stopTimer();
        
        // Hide progress, show results
        setTimeout(() => {
            progressSection.style.display = 'none';
            displayResults(data);
            resultsSection.style.display = 'block';
            scrollToResults();
        }, 500);
        
    } catch (error) {
        console.error('Research error:', error);
        stopTimer();
        progressSection.style.display = 'none';
        showError(error.message);
        resultsSection.style.display = 'block';
    }
}

function updateStep(step, status, message) {
    const elements = {
        analyze: { step: stepAnalyze, status: stepAnalyzeStatus },
        wikipedia: { step: stepWikipedia, status: stepWikipediaStatus },
        news: { step: stepNews, status: stepNewsStatus },
        ai: { step: stepAI, status: stepAIStatus }
    };
    
    const element = elements[step];
    if (!element) return;
    
    // Remove previous status classes
    element.step.classList.remove('active', 'completed');
    
    if (status === 'active') {
        element.step.classList.add('active');
    } else if (status === 'completed') {
        element.step.classList.add('completed');
    }
    
    if (element.status) {
        element.status.textContent = message;
    }
}

function resetProgress() {
    const steps = ['analyze', 'wikipedia', 'news', 'ai'];
    steps.forEach(step => {
        updateStep(step, '', 'Waiting...');
    });
}

function startTimer() {
    startTime = Date.now();
    timerInterval = setInterval(() => {
        if (startTime) {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            progressTimer.textContent = `${elapsed}s`;
        }
    }, 100);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
    startTime = null;
}

function displayResults(data) {
    // Display answer
    answerContent.innerHTML = formatAnswer(data.answer);
    
    // Display sources
    displaySources(data.sources);
    
    // Update source count
    sourceCount.textContent = data.sources.length;
    
    // Display metrics
    displayMetrics(data);
}

function formatAnswer(answer) {
    let formatted = answer
        .replace(/\[(\d+)\]/g, '<sup class="citation">[$1]</sup>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^### (.*$)/gm, '<h4>$1</h4>')
        .replace(/^## (.*$)/gm, '<h3>$1</h3>')
        .replace(/^# (.*$)/gm, '<h2>$1</h2>')
        .replace(/^\s*[-*]\s+(.*$)/gm, '<li>$1</li>')
        .replace(/\n\n/g, '</p><p>');
    
    return `<div class="answer-content">${formatted}</div>`;
}

function displaySources(sources) {
    if (!sources || sources.length === 0) {
        sourcesContent.innerHTML = '<div class="no-sources">No sources found</div>';
        return;
    }
    
    sourcesContent.innerHTML = `
        <div class="sources-list">
            ${sources.map((source, index) => `
                <div class="source-item">
                    <div class="source-header">
                        <div class="source-icon">
                            <i class="fas fa-${getSourceIcon(source.source_type)}"></i>
                        </div>
                        <div class="source-title">${escapeHtml(source.title)}</div>
                    </div>
                    <div class="source-meta">
                        <span><i class="fas fa-tag"></i> ${capitalizeFirst(source.source_type)}</span>
                        ${source.metadata?.published ? 
                            `<span><i class="far fa-calendar"></i> ${source.metadata.published}</span>` : ''}
                    </div>
                    <div class="source-content">${truncateText(escapeHtml(source.content), 200)}</div>
                    <a href="${source.url}" target="_blank" class="source-link">
                        <span>View Source</span>
                        <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            `).join('')}
        </div>
    `;
}

function displayMetrics(data) {
    const metricsContainer = document.getElementById('resultsMetrics');
    if (!metricsContainer) return;
    
    metricsContainer.innerHTML = `
        <div class="metric">
            <i class="fas fa-clock"></i>
            <span>${data.processing_time}s</span>
        </div>
        <div class="metric">
            <i class="fas fa-brain"></i>
            <span>${data.tokens_used} tokens</span>
        </div>
        <div class="metric">
            <i class="fas fa-database"></i>
            <span>${data.sources.length} sources</span>
        </div>
    `;
}

function showError(message) {
    answerContent.innerHTML = `
        <div class="error-message">
            <i class="fas fa-exclamation-triangle"></i>
            <h4>Research Failed</h4>
            <p>${message}</p>
            <button onclick="performResearch()" class="btn-primary" style="margin-top: 20px;">
                <i class="fas fa-redo"></i> Try Again
            </button>
        </div>
    `;
}

function clearAll() {
    queryInput.value = '';
    resultsSection.style.display = 'none';
    progressSection.style.display = 'none';
    answerContent.innerHTML = '';
    sourcesContent.innerHTML = '';
    sourceCount.textContent = '0';
    autoResizeTextarea();
    updateCharCounter();
    stopTimer();
}

function scrollToResults() {
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function getSourceIcon(type) {
    const icons = {
        'wikipedia': 'wikipedia-w',
        'news': 'newspaper'
    };
    return icons[type] || 'file-alt';
}

function capitalizeFirst(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength).trim() + '...';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}