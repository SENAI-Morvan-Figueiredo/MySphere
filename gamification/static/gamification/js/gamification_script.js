document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');
    const actionItems = document.querySelectorAll('.action-item[data-tab-link]');

    function switchTab(tabId) {
        tabs.forEach(t => t.classList.remove('active'));
        contents.forEach(c => c.classList.remove('active'));
        actionItems.forEach(a => a.classList.remove('active'));

        const activeTab = document.querySelector(`.tab[data-tab="${tabId}"]`);
        const activeContent = document.getElementById(tabId);
        const activeAction = document.querySelector(`.action-item[data-tab-link="${tabId}"]`);

        if (activeTab) activeTab.classList.add('active');
        if (activeContent) activeContent.classList.add('active');
        if (activeAction) activeAction.classList.add('active');
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            switchTab(tab.dataset.tab);
        });
    });

    actionItems.forEach(action => {
        action.addEventListener('click', () => {
            switchTab(action.dataset.tabLink);
        });
    });
});
