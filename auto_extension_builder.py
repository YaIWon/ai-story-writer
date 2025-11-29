# auto_extension_builder.py

import os
import json
import shutil
import zipfile
from typing import Dict, List, Any
from datetime import datetime

class AutoExtensionBuilder:
    def __init__(self, output_dir: str = "browser_extension"):
        self.output_dir = output_dir
        self.extension_dir = os.path.join(output_dir, "rawai_extension")
        self.build_dir = os.path.join(output_dir, "build")
        
        os.makedirs(self.extension_dir, exist_ok=True)
        os.makedirs(self.build_dir, exist_ok=True)
    
    def build_complete_extension(self) -> Dict[str, Any]:
        """Build complete browser extension with all components"""
        print("🔨 Building browser extension...")
        
        build_result = {
            'status': 'building',
            'components_created': [],
            'files_generated': [],
            'errors': [],
            'build_path': '',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # 1. Create manifest
            self._create_manifest()
            build_result['components_created'].append('manifest')
            
            # 2. Create background script
            self._create_background_script()
            build_result['components_created'].append('background_script')
            
            # 3. Create content script
            self._create_content_script()
            build_result['components_created'].append('content_script')
            
            # 4. Create popup interface
            self._create_popup_interface()
            build_result['components_created'].append('popup_interface')
            
            # 5. Create options page
            self._create_options_page()
            build_result['components_created'].append('options_page')
            
            # 6. Copy icons
            self._copy_icons()
            build_result['components_created'].append('icons')
            
            # 7. Package extension
            package_path = self._package_extension()
            build_result['build_path'] = package_path
            build_result['files_generated'].append(package_path)
            
            build_result['status'] = 'success'
            print("✅ Browser extension built successfully!")
            
        except Exception as e:
            build_result['status'] = 'error'
            build_result['errors'].append(str(e))
            print(f"❌ Extension build error: {e}")
        
        return build_result
    
    def _create_manifest(self):
        """Create extension manifest.json"""
        manifest = {
            "manifest_version": 3,
            "name": "RawAI Creator Extension",
            "version": "1.0.0",
            "description": "AI content generation and automation extension",
            "permissions": [
                "activeTab",
                "storage",
                "scripting",
                "tabs",
                "webNavigation",
                "contextMenus"
            ],
            "host_permissions": [
                "https://*/*",
                "http://*/*"
            ],
            "background": {
                "service_worker": "background.js"
            },
            "content_scripts": [
                {
                    "matches": ["<all_urls>"],
                    "js": ["content.js"],
                    "css": ["content.css"]
                }
            ],
            "action": {
                "default_popup": "popup.html",
                "default_title": "RawAI Creator",
                "default_icon": {
                    "16": "icons/icon_16.png",
                    "32": "icons/icon_32.png",
                    "48": "icons/icon_48.png",
                    "128": "icons/icon_128.png"
                }
            },
            "options_page": "options.html",
            "icons": {
                "16": "icons/icon_16.png",
                "32": "icons/icon_32.png",
                "48": "icons/icon_48.png",
                "128": "icons/icon_128.png"
            },
            "web_accessible_resources": [{
                "resources": ["injected.js", "styles.css"],
                "matches": ["<all_urls>"]
            }]
        }
        
        manifest_path = os.path.join(self.extension_dir, "manifest.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
    
    def _create_background_script(self):
        """Create background service worker script"""
        background_script = '''
// RawAI Creator Background Service Worker
console.log('RawAI Creator extension background script loaded');

// Message handling between content scripts and popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('Background received message:', request);
    
    switch (request.action) {
        case 'SYNC_WITH_CODESPACES':
            syncWithCodespaces(request.data);
            break;
        case 'EXECUTE_ACTION':
            executeAction(request.data);
            break;
        case 'SCRAPE_CONTENT':
            scrapeContent(request.data);
            break;
        case 'AUTO_FILL':
            autoFillContent(request.data);
            break;
        default:
            console.log('Unknown action:', request.action);
    }
    
    return true;
});

// Sync with GitHub Codespaces
async function syncWithCodespaces(data) {
    try {
        const response = await fetch('http://localhost:5000/api/sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        console.log('Sync result:', result);
    } catch (error) {
        console.error('Sync error:', error);
    }
}

// Execute actions on web pages
function executeAction(data) {
    const { action, selector, value } = data;
    
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'EXECUTE_COMMAND',
                command: action,
                selector: selector,
                value: value
            });
        }
    });
}

// Scrape content from current page
function scrapeContent(data) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'SCRAPE_PAGE',
                patterns: data.patterns
            });
        }
    });
}

// Auto-fill forms and content
function autoFillContent(data) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'AUTO_FILL',
                fields: data.fields,
                content: data.content
            });
        }
    });
}

// Context menu integration
chrome.contextMenus.create({
    id: "rawai-scrape",
    title: "Scrape with RawAI",
    contexts: ["page", "selection"]
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "rawai-scrape") {
        chrome.tabs.sendMessage(tab.id, {
            action: 'CONTEXT_SCRAPE',
            selection: info.selectionText
        });
    }
});

// Tab monitoring for auto-sync
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.active) {
        // Auto-sync with new page load
        chrome.tabs.sendMessage(tabId, {
            action: 'PAGE_LOADED',
            url: tab.url
        });
    }
});
'''

        background_path = os.path.join(self.extension_dir, "background.js")
        with open(background_path, 'w', encoding='utf-8') as f:
            f.write(background_script)
    
    def _create_content_script(self):
        """Create content script for page interaction"""
        content_script = '''
// RawAI Creator Content Script
console.log('RawAI Creator content script loaded');

// Message handling from background and popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('Content script received:', request);
    
    switch (request.action) {
        case 'EXECUTE_COMMAND':
            executeCommand(request);
            break;
        case 'SCRAPE_PAGE':
            scrapePage(request.patterns);
            break;
        case 'AUTO_FILL':
            autoFill(request.fields, request.content);
            break;
        case 'CONTEXT_SCRAPE':
            handleContextScrape(request.selection);
            break;
        case 'PAGE_LOADED':
            handlePageLoaded(request.url);
            break;
    }
    
    return true;
});

// Execute commands on the page
function executeCommand(data) {
    const { command, selector, value } = data;
    
    try {
        switch (command) {
            case 'CLICK':
                document.querySelector(selector)?.click();
                break;
            case 'TYPE':
                const input = document.querySelector(selector);
                if (input) {
                    input.value = value;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                }
                break;
            case 'EXTRACT':
                const element = document.querySelector(selector);
                return element ? element.textContent : null;
            case 'NAVIGATE':
                window.location.href = value;
                break;
        }
    } catch (error) {
        console.error('Command execution error:', error);
    }
}

// Scrape page content based on patterns
function scrapePage(patterns) {
    const scrapedData = {};
    
    patterns.forEach(pattern => {
        const elements = document.querySelectorAll(pattern.selector);
        scrapedData[pattern.name] = Array.from(elements).map(el => ({
            text: el.textContent,
            html: el.innerHTML,
            attributes: Array.from(el.attributes).reduce((attrs, attr) => {
                attrs[attr.name] = attr.value;
                return attrs;
            }, {})
        }));
    });
    
    // Send scraped data back to background
    chrome.runtime.sendMessage({
        action: 'SCRAPED_DATA',
        data: scrapedData,
        url: window.location.href,
        timestamp: new Date().toISOString()
    });
    
    return scrapedData;
}

// Auto-fill forms and content areas
function autoFill(fields, content) {
    fields.forEach(field => {
        const element = document.querySelector(field.selector);
        if (element) {
            switch (field.type) {
                case 'input':
                case 'textarea':
                    element.value = content[field.name] || '';
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    break;
                case 'select':
                    element.value = content[field.name] || '';
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    break;
                case 'contenteditable':
                    element.innerHTML = content[field.name] || '';
                    break;
            }
        }
    });
}

// Handle context menu scraping
function handleContextScrape(selection) {
    const scrapedData = {
        selection: selection,
        pageTitle: document.title,
        pageUrl: window.location.href,
        timestamp: new Date().toISOString()
    };
    
    chrome.runtime.sendMessage({
        action: 'CONTEXT_SCRAPED_DATA',
        data: scrapedData
    });
}

// Handle page loaded event
function handlePageLoaded(url) {
    // Auto-scrape based on URL patterns
    const scrapePatterns = getScrapePatternsForUrl(url);
    if (scrapePatterns.length > 0) {
        setTimeout(() => {
            scrapePage(scrapePatterns);
        }, 2000); // Wait for page to fully load
    }
}

// Get scraping patterns based on URL
function getScrapePatternsForUrl(url) {
    const patterns = [];
    
    // Social media patterns
    if (url.includes('twitter.com') || url.includes('x.com')) {
        patterns.push(
            { name: 'tweets', selector: '[data-testid="tweet"]' },
            { name: 'usernames', selector: '[data-testid="User-Name"]' }
        );
    }
    
    if (url.includes('youtube.com')) {
        patterns.push(
            { name: 'videos', selector: '#video-title' },
            { name: 'channels', selector: '#channel-name' }
        );
    }
    
    if (url.includes('github.com')) {
        patterns.push(
            { name: 'repositories', selector: '.repo' },
            { name: 'code_files', selector: '.file' }
        );
    }
    
    // E-commerce patterns
    if (url.includes('amazon.com') || url.includes('ebay.com')) {
        patterns.push(
            { name: 'products', selector: '.s-result-item' },
            { name: 'prices', selector: '.a-price' }
        );
    }
    
    return patterns;
}

// Inject AI assistance into page
function injectAIAssistance() {
    const aiOverlay = document.createElement('div');
    aiOverlay.id = 'rawai-overlay';
    aiOverlay.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        background: #4F46E5;
        color: white;
        padding: 10px;
        border-radius: 5px;
        z-index: 10000;
        font-family: Arial, sans-serif;
        font-size: 12px;
    `;
    aiOverlay.innerHTML = 'RawAI Active';
    document.body.appendChild(aiOverlay);
}

// Initialize when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectAIAssistance);
} else {
    injectAIAssistance();
}
'''

        content_path = os.path.join(self.extension_dir, "content.js")
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write(content_script)
        
        # Create content CSS
        content_css = '''
/* RawAI Creator Content Styles */
#rawai-overlay {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}

.rawai-highlight {
    background-color: #4F46E5 !important;
    border: 2px solid #7E22CE !important;
    transition: all 0.3s ease;
}

.rawai-annotation {
    position: absolute;
    background: #4F46E5;
    color: white;
    padding: 5px 10px;
    border-radius: 3px;
    font-size: 12px;
    z-index: 9999;
    pointer-events: none;
}
'''

        css_path = os.path.join(self.extension_dir, "content.css")
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(content_css)
    
    def _create_popup_interface(self):
        """Create extension popup interface"""
        popup_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            width: 400px;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: #0a0a0a;
            color: white;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .tab {
            background: #1a1a1a;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            cursor: pointer;
        }
        .tab.active {
            background: #4F46E5;
        }
        .content {
            display: none;
        }
        .content.active {
            display: block;
        }
        button {
            background: #4F46E5;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            margin: 5px 0;
        }
        button:hover {
            background: #7E22CE;
        }
        textarea {
            width: 100%;
            height: 100px;
            background: #2a2a2a;
            color: white;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h3>🤖 RawAI Creator</h3>
        <p>AI-Powered Content & Automation</p>
    </div>
    
    <div class="tab active" onclick="switchTab('scrape')">🔍 Scrape Content</div>
    <div class="tab" onclick="switchTab('generate')">🎨 Generate Content</div>
    <div class="tab" onclick="switchTab('automate')">⚡ Automate</div>
    <div class="tab" onclick="switchTab('sync')">🔄 Sync</div>
    
    <div id="scrape" class="content active">
        <h4>Scrape Page Content</h4>
        <button onclick="scrapePage()">Scrape Current Page</button>
        <button onclick="scrapeSelection()">Scrape Selected Text</button>
        <textarea id="scrapeResult" placeholder="Scraped content will appear here..."></textarea>
        <button onclick="saveScraped()">Save to Training Data</button>
    </div>
    
    <div id="generate" class="content">
        <h4>Generate Content</h4>
        <textarea id="generatePrompt" placeholder="Enter your content prompt..."></textarea>
        <button onclick="generateContent()">Generate</button>
        <textarea id="generateResult" placeholder="Generated content will appear here..."></textarea>
        <button onclick="insertContent()">Insert on Page</button>
    </div>
    
    <div id="automate" class="content">
        <h4>Automation</h4>
        <button onclick="autoFillForms()">Auto-Fill Forms</button>
        <button onclick="autoClick()">Auto-Click Elements</button>
        <button onclick="autoNavigate()">Auto-Navigate</button>
        <button onclick="startMonitoring()">Start Monitoring</button>
    </div>
    
    <div id="sync" class="content">
        <h4>Sync with Codespaces</h4>
        <button onclick="syncData()">Sync Current Data</button>
        <button onclick="getTasks()">Get Tasks</button>
        <div id="syncStatus">Ready to sync...</div>
    </div>

    <script src="popup.js"></script>
</body>
</html>
'''

        popup_path = os.path.join(self.extension_dir, "popup.html")
        with open(popup_path, 'w', encoding='utf-8') as f:
            f.write(popup_html)
        
        # Create popup JavaScript
        popup_js = '''
// Popup JavaScript
function switchTab(tabName) {
    // Hide all tabs and contents
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.content').forEach(content => content.classList.remove('active'));
    
    // Show selected tab and content
    document.querySelector(`.tab[onclick="switchTab('${tabName}')"]`).classList.add('active');
    document.getElementById(tabName).classList.add('active');
}

// Scraping functions
async function scrapePage() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.tabs.sendMessage(tab.id, { action: 'SCRAPE_PAGE', patterns: [] }, (response) => {
        document.getElementById('scrapeResult').value = JSON.stringify(response, null, 2);
    });
}

async function scrapeSelection() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.tabs.sendMessage(tab.id, { action: 'CONTEXT_SCRAPE' }, (response) => {
        document.getElementById('scrapeResult').value = JSON.stringify(response, null, 2);
    });
}

async function saveScraped() {
    const data = document.getElementById('scrapeResult').value;
    
    chrome.runtime.sendMessage({
        action: 'SYNC_WITH_CODESPACES',
        data: {
            type: 'scraped_content',
            content: data,
            url: (await chrome.tabs.query({ active: true, currentWindow: true }))[0].url
        }
    });
    
    document.getElementById('syncStatus').textContent = 'Data synced!';
}

// Content generation
async function generateContent() {
    const prompt = document.getElementById('generatePrompt').value;
    
    chrome.runtime.sendMessage({
        action: 'SYNC_WITH_CODESPACES',
        data: {
            type: 'generation_request',
            prompt: prompt,
            context: 'browser_extension'
        }
    }, (response) => {
        document.getElementById('generateResult').value = response.generated_content;
    });
}

async function insertContent() {
    const content = document.getElementById('generateResult').value;
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.tabs.sendMessage(tab.id, {
        action: 'AUTO_FILL',
        fields: [{ selector: 'body', type: 'contenteditable' }],
        content: { content: content }
    });
}

// Automation functions
async function autoFillForms() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.tabs.sendMessage(tab.id, {
        action: 'AUTO_FILL',
        fields: [
            { selector: 'input[type="text"]', type: 'input' },
            { selector: 'textarea', type: 'textarea' },
            { selector: 'select', type: 'select' }
        ],
        content: { 
            text: 'Auto-filled by RawAI',
            textarea: 'This content was automatically filled by the RawAI Creator extension.'
        }
    });
}

async function autoClick() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.tabs.sendMessage(tab.id, {
        action: 'EXECUTE_COMMAND',
        command: 'CLICK',
        selector: 'button, a'
    });
}

async function autoNavigate() {
    chrome.runtime.sendMessage({
        action: 'EXECUTE_ACTION',
        data: {
            action: 'NAVIGATE',
            value: 'https://github.com'
        }
    });
}

async function startMonitoring() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.tabs.sendMessage(tab.id, {
        action: 'PAGE_LOADED',
        url: tab.url
    });
}

// Sync functions
async function syncData() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.runtime.sendMessage({
        action: 'SYNC_WITH_CODESPACES',
        data: {
            type: 'full_sync',
            url: tab.url,
            title: tab.title,
            timestamp: new Date().toISOString()
        }
    });
    
    document.getElementById('syncStatus').textContent = 'Syncing data...';
}

async function getTasks() {
    chrome.runtime.sendMessage({
        action: 'SYNC_WITH_CODESPACES',
        data: { type: 'get_tasks' }
    }, (response) => {
        document.getElementById('syncStatus').textContent = 
            `Tasks: ${response.tasks ? response.tasks.length : 0} pending`;
    });
}

// Initialize popup
document.addEventListener('DOMContentLoaded', () => {
    console.log('RawAI popup loaded');
});
'''

        popup_js_path = os.path.join(self.extension_dir, "popup.js")
        with open(popup_js_path, 'w', encoding='utf-8') as f:
            f.write(popup_js)
    
    def _create_options_page(self):
        """Create extension options page"""
        options_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { 
            width: 600px; 
            padding: 20px; 
            font-family: Arial, sans-serif;
            background: #0a0a0a;
            color: white;
        }
        .section { 
            background: #1a1a1a; 
            padding: 20px; 
            margin: 10px 0; 
            border-radius: 5px; 
        }
        button { 
            background: #4F46E5; 
            color: white; 
            border: none; 
            padding: 10px; 
            margin: 5px; 
            border-radius: 5px; 
            cursor: pointer; 
        }
        button:hover { background: #7E22CE; }
        input, textarea, select { 
            width: 100%; 
            padding: 8px; 
            margin: 5px 0; 
            background: #2a2a2a; 
            color: white; 
            border: 1px solid #444; 
            border-radius: 3px; 
        }
    </style>
</head>
<body>
    <h2>RawAI Creator Extension Settings</h2>
    
    <div class="section">
        <h3>🔗 Codespaces Connection</h3>
        <input type="url" id="codespacesUrl" placeholder="https://your-codespace.app.github.dev">
        <button onclick="testConnection()">Test Connection</button>
        <div id="connectionStatus"></div>
    </div>
    
    <div class="section">
        <h3>⚡ Automation Settings</h3>
        <label><input type="checkbox" id="autoScrape"> Auto-scrape on page load</label><br>
        <label><input type="checkbox" id="autoSync"> Auto-sync with Codespaces</label><br>
        <label><input type="checkbox" id="contextMenu"> Enable context menu</label>
    </div>
    
    <div class="section">
        <h3>🎨 Content Generation</h3>
        <select id="defaultModel">
            <option value="creative">Creative</option>
            <option value="technical">Technical</option>
            <option value="professional">Professional</option>
        </select>
        <textarea id="customInstructions" placeholder="Custom instructions for content generation..."></textarea>
    </div>
    
    <div class="section">
        <h3>📊 Data Management</h3>
        <button onclick="exportData()">Export All Data</button>
        <button onclick="clearData()">Clear Local Data</button>
        <button onclick="viewStats()">View Statistics</button>
    </div>
    
    <div class="section">
        <button onclick="saveSettings()" style="background: #10B981;">Save Settings</button>
        <button onclick="resetSettings()" style="background: #EF4444;">Reset to Defaults</button>
    </div>

    <script src="options.js"></script>
</body>
</html>
'''

        options_path = os.path.join(self.extension_dir, "options.html")
        with open(options_path, 'w', encoding='utf-8') as f:
            f.write(options_html)
        
        # Create options JavaScript
        options_js = '''
// Options page JavaScript
async function saveSettings() {
    const settings = {
        codespacesUrl: document.getElementById('codespacesUrl').value,
        autoScrape: document.getElementById('autoScrape').checked,
        autoSync: document.getElementById('autoSync').checked,
        contextMenu: document.getElementById('contextMenu').checked,
        defaultModel: document.getElementById('defaultModel').value,
        customInstructions: document.getElementById('customInstructions').value
    };
    
    await chrome.storage.sync.set(settings);
    alert('Settings saved!');
}

async function loadSettings() {
    const settings = await chrome.storage.sync.get([
        'codespacesUrl', 'autoScrape', 'autoSync', 'contextMenu', 
        'defaultModel', 'customInstructions'
    ]);
    
    document.getElementById('codespacesUrl').value = settings.codespacesUrl || '';
    document.getElementById('autoScrape').checked = settings.autoScrape || false;
    document.getElementById('autoSync').checked = settings.autoSync || false;
    document.getElementById('contextMenu').checked = settings.contextMenu || true;
    document.getElementById('defaultModel').value = settings.defaultModel || 'creative';
    document.getElementById('customInstructions').value = settings.customInstructions || '';
}

async function testConnection() {
    const url = document.getElementById('codespacesUrl').value;
    const status = document.getElementById('connectionStatus');
    
    try {
        const response = await fetch(url + '/api/status');
        if (response.ok) {
            status.textContent = '✅ Connection successful!';
            status.style.color = '#10B981';
        } else {
            throw new Error('Connection failed');
        }
    } catch (error) {
        status.textContent = '❌ Connection failed';
        status.style.color = '#EF4444';
    }
}

async function exportData() {
    const data = await chrome.storage.local.get(null);
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'rawai-extension-data.json';
    a.click();
    
    URL.revokeObjectURL(url);
}

async function clearData() {
    if (confirm('Are you sure you want to clear all local data?')) {
        await chrome.storage.local.clear();
        alert('Data cleared!');
    }
}

async function viewStats() {
    const data = await chrome.storage.local.get(null);
    const stats = {
        scrapedItems: Object.keys(data).filter(key => key.startsWith('scraped_')).length,
        generatedContent: Object.keys(data).filter(key => key.startsWith('generated_')).length,
        syncOperations: data.syncCount || 0
    };
    
    alert(`Extension Statistics:
📊 Scraped Items: ${stats.scrapedItems}
🎨 Generated Content: ${stats.generatedContent}
🔄 Sync Operations: ${stats.syncOperations}`);
}

function resetSettings() {
    if (confirm('Reset all settings to defaults?')) {
        chrome.storage.sync.clear();
        loadSettings();
        alert('Settings reset!');
    }
}

// Load settings when page opens
document.addEventListener('DOMContentLoaded', loadSettings);
'''

        options_js_path = os.path.join(self.extension_dir, "options.js")
        with open(options_js_path, 'w', encoding='utf-8') as f:
            f.write(options_js)
    
    def _copy_icons(self):
        """Copy or generate icons for extension"""
        icons_dir = os.path.join(self.extension_dir, "icons")
        os.makedirs(icons_dir, exist_ok=True)
        
        # Create placeholder icon files
        icon_sizes = ['16', '32', '48', '128']
        for size in icon_sizes:
            icon_path = os.path.join(icons_dir, f"icon_{size}.png")
            
            # Create placeholder metadata
            metadata = {
                'size': size,
                'description': f'RawAI Creator icon {size}x{size}',
                'generated_at': datetime.now().isoformat(),
                'note': 'Replace with actual PNG icons'
            }
            
            metadata_path = icon_path.replace('.png', '.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
    
    def _package_extension(self) -> str:
        """Package extension into ZIP file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"rawai_extension_{timestamp}.zip"
        zip_path = os.path.join(self.build_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.extension_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.extension_dir)
                    zipf.write(file_path, arcname)
        
        return zip_path
    
    def install_extension(self) -> Dict[str, Any]:
        """Install extension in browser (development mode)"""
        print("📥 Installing browser extension...")
        
        install_result = {
            'status': 'installing',
            'browser': 'chrome',
            'method': 'development_mode',
            'instructions': [],
            'errors': []
        }
        
        try:
            # For Chrome/Edge development mode installation
            instructions = [
                "1. Open Chrome/Edge and go to chrome://extensions/",
                "2. Enable 'Developer mode' in the top right",
                "3. Click 'Load unpacked' and select the extension folder:",
                f"   {os.path.abspath(self.extension_dir)}",
                "4. The RawAI Creator extension should now be installed!",
                "5. Pin the extension to your toolbar for easy access"
            ]
            
            install_result['instructions'] = instructions
            install_result['status'] = 'success'
            install_result['extension_path'] = os.path.abspath(self.extension_dir)
            
            print("✅ Extension ready for installation!")
            print("\\n".join(instructions))
            
        except Exception as e:
            install_result['status'] = 'error'
            install_result['errors'].append(str(e))
            print(f"❌ Installation setup error: {e}")
        
        return install_result
