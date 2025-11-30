
async function saveSettings() {
    const settings = {
        autoConnect: document.getElementById('autoConnect').checked
    };
    await chrome.storage.sync.set(settings);
    alert('Settings saved!');
}

document.addEventListener('DOMContentLoaded', async () => {
    const settings = await chrome.storage.sync.get(['autoConnect']);
    document.getElementById('autoConnect').checked = settings.autoConnect ?? true;
});
