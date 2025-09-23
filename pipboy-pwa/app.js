// Pip-Boy Framework - Main Application Logic

class PipBoyFramework {
    constructor() {
        this.currentTab = 'stat';
        this.currentSubTabs = {
            stat: 0,
            inv: 0,
            data: 0,
            map: 0,
            radio: 0
        };
        
        this.tabs = {
            stat: ['STATUS', 'SPECIAL', 'PERKS'],
            inv: ['WEAPONS', 'APPAREL', 'AID', 'MISC', 'JUNK'],
            data: ['QUESTS', 'WORKSHOPS', 'STATS', 'SETTINGS'],
            map: ['LOCAL MAP', 'WORLD MAP'],
            radio: ['DIAMOND CITY', 'CLASSICAL', 'FREEDOM']
        };
        
        this.settingsManager = null;
        this.init();
    }
    
    init() {
        this.setupTabListeners();
        this.setupSubTabListeners();
        this.registerServiceWorker();
        this.createContentPanels();
        this.initializeKeyboardNavigation();
        // Initialize settings manager after DOM is ready
        if (typeof PipBoySettings !== 'undefined') {
            this.settingsManager = new PipBoySettings();
        }
    }
    
    setupTabListeners() {
        const tabButtons = document.querySelectorAll('.tab-button');
        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const tabName = e.target.dataset.tab;
                this.switchTab(tabName);
            });
        });
    }
    
    setupSubTabListeners() {
        const subTabButtons = document.querySelectorAll('.sub-tab-button');
        subTabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const parentTab = e.target.closest('.sub-tabs').dataset.parent;
                const subTabIndex = Array.from(e.target.parentElement.children).indexOf(e.target);
                this.switchSubTab(parentTab, subTabIndex);
            });
        });
    }
    
    switchTab(tabName) {
        if (tabName === this.currentTab) return;
        
        // Trigger glitch effect
        this.triggerGlitch();
        
        // Update tab buttons
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.tab === tabName) {
                btn.classList.add('active');
            }
        });
        
        // Update sub-tabs visibility
        document.querySelectorAll('.sub-tabs').forEach(subTab => {
            subTab.classList.add('hidden');
        });
        const targetSubTab = document.querySelector(`#sub-tabs-${tabName}`);
        if (targetSubTab) {
            targetSubTab.classList.remove('hidden');
            
            // CRITICAL FIX: Force grid layout for DATA and INV tabs
            if (tabName === 'data' || tabName === 'inv') {
                targetSubTab.style.display = 'grid';
                if (tabName === 'data') {
                    targetSubTab.style.gridTemplateColumns = 'repeat(4, 1fr)';
                } else if (tabName === 'inv') {
                    targetSubTab.style.gridTemplateColumns = 'repeat(5, 1fr)';
                }
                
                // Verify all buttons are visible
                const buttons = targetSubTab.querySelectorAll('.sub-tab-button');
                console.log(`${tabName.toUpperCase()} tab has ${buttons.length} sub-tabs:`);
                buttons.forEach((btn, idx) => {
                    console.log(`  ${idx + 1}. ${btn.textContent}`);
                });
            }
        }
        
        // Update content
        this.updateContent(tabName, this.currentSubTabs[tabName]);
        
        // Play sound effect (if implemented)
        this.playTabSwitchSound();
        
        this.currentTab = tabName;
    }
    
    switchSubTab(parentTab, subTabIndex) {
        if (parentTab !== this.currentTab) return;
        
        // Update sub-tab buttons
        const subTabContainer = document.querySelector(`#sub-tabs-${parentTab}`);
        const subTabButtons = subTabContainer.querySelectorAll('.sub-tab-button');
        subTabButtons.forEach((btn, idx) => {
            btn.classList.remove('active');
            if (idx === subTabIndex) {
                btn.classList.add('active');
            }
        });
        
        // Update current sub-tab index
        this.currentSubTabs[parentTab] = subTabIndex;
        
        // Update content
        this.updateContent(parentTab, subTabIndex);
        
        // Slight glitch effect
        this.triggerMiniGlitch();
    }
    
    updateContent(tabName, subTabIndex) {
        // Hide all content panels
        document.querySelectorAll('.content-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        
        // Show the selected content panel
        const targetPanel = document.querySelector(`.content-panel[data-tab="${tabName}"][data-subtab="${subTabIndex}"]`);
        if (targetPanel) {
            targetPanel.classList.add('active');
        }
    }
    
    createContentPanels() {
        const contentContainer = document.getElementById('pipboy-content');
        
        // Generate demo content for each tab/subtab combination
        Object.keys(this.tabs).forEach(tabName => {
            this.tabs[tabName].forEach((subTabName, subTabIndex) => {
                // Skip if panel already exists (stat/status is pre-created)
                if (tabName === 'stat' && subTabIndex === 0) return;
                
                const panel = document.createElement('div');
                panel.className = 'content-panel';
                panel.dataset.tab = tabName;
                panel.dataset.subtab = subTabIndex;
                
                panel.innerHTML = `
                    <div class="demo-content">
                        <h2>${subTabName}</h2>
                        <div class="grid-pattern">
                            ${this.generateDemoContent(tabName, subTabName)}
                        </div>
                    </div>
                `;
                
                contentContainer.appendChild(panel);
            });
        });
    }
    
    generateDemoContent(tabName, subTabName) {
        const demoData = {
            'SPECIAL': '<p>Strength: 5</p><p>Perception: 7</p><p>Endurance: 4</p><p>Charisma: 3</p><p>Intelligence: 8</p><p>Agility: 6</p><p>Luck: 7</p>',
            'PERKS': '<p>Lockpicking - Rank 3</p><p>Science - Rank 2</p><p>Gunslinger - Rank 1</p>',
            'WEAPONS': '<p>10mm Pistol</p><p>Laser Rifle</p><p>Combat Shotgun</p>',
            'APPAREL': '<p>Vault Suit</p><p>Combat Armor</p><p>Power Armor MK-II</p>',
            'AID': '<p>Stimpak x10</p><p>RadAway x5</p><p>Purified Water x20</p>',
            'MISC': '<p>Bobby Pins x50</p><p>Holotapes x3</p><p>Pre-War Money x100</p>',
            'JUNK': '<p>Steel x150</p><p>Wood x75</p><p>Adhesive x25</p>',
            'QUESTS': '<p>Main Quest: Find the Institute</p><p>Side Quest: Help the Settlers</p>',
            'WORKSHOPS': '<p>Sanctuary Hills - Population: 15</p><p>Red Rocket - Population: 3</p>',
            'STATS': '<p>Locations Discovered: 127</p><p>Enemies Killed: 892</p><p>Caps Collected: 15,420</p>',
            'SETTINGS': '<p>Display Settings: Active</p><p>Audio Settings: Enabled</p><p>Theme: Green</p><p>Effects: All On</p>',
            'LOCAL MAP': '<p>[Map Grid Display]</p><p>Current Location: Commonwealth</p>',
            'WORLD MAP': '<p>[World Overview]</p><p>Fast Travel Points: 45</p>',
            'DIAMOND CITY': '<p>♪ Playing: Diamond City Radio</p><p>Travis Miles - "The Nervous DJ"</p>',
            'CLASSICAL': '<p>♪ Playing: Classical Radio</p><p>Current Track: Beethoven Symphony No. 5</p>',
            'FREEDOM': '<p>♪ Playing: Radio Freedom</p><p>Minutemen Emergency Broadcast</p>'
        };
        
        return demoData[subTabName] || '<p>Framework content placeholder</p><p>Ready for implementation</p>';
    }
    
    initializeKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            const tabs = ['stat', 'inv', 'data', 'map', 'radio'];
            const currentIndex = tabs.indexOf(this.currentTab);
            
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    if (currentIndex > 0) {
                        this.switchTab(tabs[currentIndex - 1]);
                    }
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    if (currentIndex < tabs.length - 1) {
                        this.switchTab(tabs[currentIndex + 1]);
                    }
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    this.navigateSubTab(-1);
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    this.navigateSubTab(1);
                    break;
            }
        });
    }
    
    navigateSubTab(direction) {
        const currentSubIndex = this.currentSubTabs[this.currentTab];
        const maxSubIndex = this.tabs[this.currentTab].length - 1;
        let newIndex = currentSubIndex + direction;
        
        if (newIndex < 0) newIndex = maxSubIndex;
        if (newIndex > maxSubIndex) newIndex = 0;
        
        this.switchSubTab(this.currentTab, newIndex);
    }
    
    triggerGlitch() {
        const glitchElement = document.getElementById('screen-glitch');
        glitchElement.classList.add('active');
        setTimeout(() => {
            glitchElement.classList.remove('active');
        }, 300);
    }
    
    triggerMiniGlitch() {
        const glitchElement = document.getElementById('screen-glitch');
        glitchElement.style.opacity = '0.3';
        glitchElement.classList.add('active');
        setTimeout(() => {
            glitchElement.classList.remove('active');
            glitchElement.style.opacity = '';
        }, 150);
    }
    
    playTabSwitchSound() {
        // Audio implementation would go here
        // For now, we'll just console log
        console.log('Tab switch sound effect');
    }
    
    registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('./service-worker.js')
                .then(registration => console.log('Service Worker registered'))
                .catch(error => console.log('Service Worker registration failed:', error));
        }
    }
    
    // API Methods for extending the framework
    registerTab(tabName, subTabs) {
        this.tabs[tabName] = subTabs;
        this.currentSubTabs[tabName] = 0;
        // Would need to dynamically create tab button and sub-tabs
        console.log(`Tab '${tabName}' registered with sub-tabs:`, subTabs);
    }
    
    setContent(tabName, subTabIndex, content) {
        const panel = document.querySelector(`.content-panel[data-tab="${tabName}"][data-subtab="${subTabIndex}"]`);
        if (panel) {
            const contentDiv = panel.querySelector('.grid-pattern');
            if (contentDiv) {
                contentDiv.innerHTML = content;
            }
        }
    }
}

// Initialize the framework when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.pipboy = new PipBoyFramework();
    
    // Expose API globally
    window.PipBoyAPI = {
        registerTab: (name, subTabs) => window.pipboy.registerTab(name, subTabs),
        setContent: (tab, subTab, content) => window.pipboy.setContent(tab, subTab, content),
        switchTab: (tab) => window.pipboy.switchTab(tab),
        switchSubTab: (tab, subTab) => window.pipboy.switchSubTab(tab, subTab)
    };
    
    console.log('Pip-Boy Framework initialized');
    console.log('Use window.PipBoyAPI to interact with the framework');
});