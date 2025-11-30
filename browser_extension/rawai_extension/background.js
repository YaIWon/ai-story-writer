
// RawAI Creator Pro - Production Background Script
console.log('🚀 RawAI Pro Background Script Loaded');

class ConnectionManager {
    constructor() {
        this.isConnected = false;
    }

    async connectToPage(tabId) {
        try {
            await chrome.scripting.executeScript({
                target: { tabId: tabId },
                files: ['content.js']
            });
            
            await chrome.scripting.insertCSS({
                target: { tabId: tabId },
                files: ['content.css']
            });

            this.isConnected = true;
            return { status: 'connected', tabId: tabId };
        } catch (error) {
            return { status: 'error', error: error.message };
        }
    }

    async syncWithBackend(data) {
        const endpoints = [
            'http://localhost:5000/api/sync',
            'http://localhost:3000/api/sync'
        ];

        for (const endpoint of endpoints) {
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    await chrome.storage.local.set({
                        lastSync: new Date().toISOString(),
                        syncData: result
                    });
                    return { status: 'success', data: result };
                }
            } catch (error) {
                console.log(`Sync failed with ${endpoint}:`, error);
            }
        }
        return { status: 'error', error: 'All sync endpoints failed' };
    }
}

const connectionManager = new ConnectionManager();

// Message handling
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    const handlers = {
        'CONNECT_TO_PAGE': async () => {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            return await connectionManager.connectToPage(tab.id);
        },
        'SYNC_WITH_BACKEND': async () => {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            const syncData = {
                url: tab.url,
                title: tab.title,
                timestamp: new Date().toISOString()
            };
            return await connectionManager.syncWithBackend(syncData);
        }
    };

    if (handlers[request.action]) {
        handlers[request.action]().then(sendResponse);
        return true;
    }
});

// Auto-connect to active tab
chrome.tabs.onActivated.addListener((activeInfo) => {
    connectionManager.connectToPage(activeInfo.tabId);
});

console.log('✅ RawAI Pro Background Script Ready');
