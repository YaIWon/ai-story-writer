
// RawAI Creator Pro - Production Content Script
console.log('🔧 RawAI Pro Content Script Loaded');

class PageAutomation {
    constructor() {
        this.isConnected = false;
    }

    connect() {
        this.isConnected = true;
        this.injectUI();
        return { status: 'connected' };
    }

    injectUI() {
        if (document.getElementById('rawai-overlay')) return;
        
        const overlay = document.createElement('div');
        overlay.id = 'rawai-overlay';
        overlay.innerHTML = \`
            <div style="
                position: fixed;
                top: 10px;
                right: 10px;
                background: #4F46E5;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-family: Arial;
                font-size: 12px;
                z-index: 10000;
                box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            ">
                <strong>RawAI Pro</strong>
                <div style="font-size: 10px; margin-top: 5px;">
                    <span>🟢 Connected</span>
                </div>
            </div>
        \`;
        document.body.appendChild(overlay);
    }
}

const automation = new PageAutomation();

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'INITIALIZE_CONNECTION') {
        const result = automation.connect();
        sendResponse(result);
    }
});

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => automation.connect());
} else {
    automation.connect();
}
