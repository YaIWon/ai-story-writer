
async function connectToPage() {
    const result = await chrome.runtime.sendMessage({ action: 'CONNECT_TO_PAGE' });
    console.log('Connection result:', result);
}

async function syncWithBackend() {
    const result = await chrome.runtime.sendMessage({ action: 'SYNC_WITH_BACKEND' });
    console.log('Sync result:', result);
}
