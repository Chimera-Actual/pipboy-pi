// Pip-Boy Framework - Settings Manager

class PipBoySettings {
    constructor() {
        this.settings = {
            crt: {
                scanlines: 'HIGH',
                curve: 'HIGH',
                glow: 'HIGH',
                flicker: 'MED',
                chromatic: 'OFF'
            },
            theme: 'GREEN'
        };
        
        this.themes = {
            GREEN: { color: '#00ff00', rgb: '0, 255, 0', bg: '#001100' },
            BLUE: { color: '#00ffff', rgb: '0, 255, 255', bg: '#001111' },
            AMBER: { color: '#ffb000', rgb: '255, 176, 0', bg: '#110800' },
            RED: { color: '#ff0040', rgb: '255, 0, 64', bg: '#110004' },
            WHITE: { color: '#ffffff', rgb: '255, 255, 255', bg: '#111111' }
        };
        
        this.crtLevels = {
            scanlines: { OFF: 0, LOW: 0.3, MED: 0.6, HIGH: 1 },
            curve: { OFF: 0, LOW: 0.3, MED: 0.6, HIGH: 1 },
            glow: { OFF: 0, LOW: 0.3, MED: 0.6, HIGH: 1 },
            flicker: { OFF: 0, LOW: 0.3, MED: 0.6, HIGH: 1 }
        };
        
        this.currentFocusIndex = 0;
        this.settingElements = [];
        
        this.init();
    }
    
    init() {
        this.loadSettings();
        this.applySettings();
        this.setupSettingsUI();
        setTimeout(() => {
            this.attachEventListeners();
        }, 100);
    }
    
    loadSettings() {
        const saved = localStorage.getItem('pipboy-settings');
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                this.settings = { ...this.settings, ...parsed };
            } catch (e) {
                console.log('Failed to load settings, using defaults');
            }
        }
    }
    
    saveSettings() {
        localStorage.setItem('pipboy-settings', JSON.stringify(this.settings));
    }
    
    applySettings() {
        // Apply theme
        const theme = this.themes[this.settings.theme];
        document.documentElement.style.setProperty('--pip-color', theme.color);
        document.documentElement.style.setProperty('--pip-color-rgb', theme.rgb);
        document.documentElement.style.setProperty('--pip-bg-color', theme.bg);
        
        // Update PWA theme color meta tag
        const themeColorMeta = document.querySelector('meta[name="theme-color"]');
        if (themeColorMeta) {
            themeColorMeta.content = theme.color;
        }
        
        // Apply CRT effects
        const crt = this.settings.crt;
        document.documentElement.style.setProperty('--scanline-intensity', this.crtLevels.scanlines[crt.scanlines]);
        document.documentElement.style.setProperty('--curve-intensity', this.crtLevels.curve[crt.curve]);
        document.documentElement.style.setProperty('--glow-intensity', this.crtLevels.glow[crt.glow]);
        document.documentElement.style.setProperty('--flicker-intensity', this.crtLevels.flicker[crt.flicker]);
        document.documentElement.style.setProperty('--chromatic-intensity', crt.chromatic === 'ON' ? 1 : 0);
        
        // Apply vignette (tied to curve setting)
        document.documentElement.style.setProperty('--vignette-intensity', this.crtLevels.curve[crt.curve]);
        
        this.updateChromaticLayer();
    }
    
    updateChromaticLayer() {
        let chromatic = document.querySelector('.chromatic-aberration');
        if (this.settings.crt.chromatic === 'ON') {
            if (!chromatic) {
                chromatic = document.createElement('div');
                chromatic.className = 'chromatic-aberration';
                document.querySelector('.pipboy-container').appendChild(chromatic);
            }
        } else if (chromatic) {
            chromatic.remove();
        }
    }
    
    setupSettingsUI() {
        // Wait for content to be created
        setTimeout(() => {
            const settingsPanel = document.querySelector('.content-panel[data-tab="data"][data-subtab="3"]');
            if (settingsPanel) {
                settingsPanel.innerHTML = this.generateSettingsHTML();
            }
        }, 50);
    }
    
    generateSettingsHTML() {
        return `
            <div class="settings-container">
                <div class="settings-section">
                    <h3>CRT EFFECTS</h3>
                    ${this.createToggleControl('Scanlines', 'scanlines', ['OFF', 'LOW', 'MED', 'HIGH'])}
                    ${this.createToggleControl('Screen Curve', 'curve', ['OFF', 'LOW', 'MED', 'HIGH'])}
                    ${this.createToggleControl('Glow Effect', 'glow', ['OFF', 'LOW', 'MED', 'HIGH'])}
                    ${this.createToggleControl('Flicker', 'flicker', ['OFF', 'LOW', 'MED', 'HIGH'])}
                    ${this.createToggleControl('Chromatic Aberration', 'chromatic', ['OFF', 'ON'])}
                </div>
                
                <div class="settings-section">
                    <h3>COLOR THEME</h3>
                    <div class="theme-selector">
                        ${Object.keys(this.themes).map(themeName => this.createThemeOption(themeName)).join('')}
                    </div>
                </div>
            </div>
        `;
    }
    
    createToggleControl(label, settingKey, options) {
        const currentValue = this.settings.crt[settingKey];
        return `
            <div class="setting-item" data-setting="${settingKey}">
                <span class="setting-label">${label}</span>
                <div class="toggle-control">
                    ${options.map(opt => `
                        <button class="toggle-option ${opt === currentValue ? 'active' : ''}" 
                                data-value="${opt}">${opt}</button>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    createThemeOption(themeName) {
        const theme = this.themes[themeName];
        const isActive = this.settings.theme === themeName;
        return `
            <div class="theme-option ${isActive ? 'active' : ''}" data-theme="${themeName}">
                <div class="theme-radio"></div>
                <span class="theme-name">${themeName}</span>
                <div class="theme-preview" style="background: ${theme.color}"></div>
            </div>
        `;
    }
    
    attachEventListeners() {
        // CRT effect toggles
        document.querySelectorAll('.toggle-control').forEach(control => {
            const setting = control.closest('.setting-item').dataset.setting;
            control.querySelectorAll('.toggle-option').forEach(btn => {
                btn.addEventListener('click', () => {
                    this.updateCRTSetting(setting, btn.dataset.value);
                });
            });
        });
        
        // Theme selector
        document.querySelectorAll('.theme-option').forEach(option => {
            option.addEventListener('click', () => {
                this.updateTheme(option.dataset.theme);
            });
        });
        
        // Keyboard navigation for settings
        this.setupSettingsKeyboardNav();
    }
    
    updateCRTSetting(setting, value) {
        this.settings.crt[setting] = value;
        this.applySettings();
        this.saveSettings();
        
        // Update UI
        const control = document.querySelector(`.setting-item[data-setting="${setting}"]`);
        if (control) {
            control.querySelectorAll('.toggle-option').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.value === value);
            });
        }
        
        // Trigger mini glitch for feedback
        if (window.pipboy) {
            window.pipboy.triggerMiniGlitch();
        }
    }
    
    updateTheme(themeName) {
        this.settings.theme = themeName;
        this.applySettings();
        this.saveSettings();
        
        // Update UI
        document.querySelectorAll('.theme-option').forEach(option => {
            option.classList.toggle('active', option.dataset.theme === themeName);
        });
        
        // Trigger glitch for feedback
        if (window.pipboy) {
            window.pipboy.triggerGlitch();
        }
    }
    
    setupSettingsKeyboardNav() {
        // Check if we're on the settings tab
        document.addEventListener('keydown', (e) => {
            const settingsPanel = document.querySelector('.content-panel[data-tab="data"][data-subtab="3"].active');
            if (!settingsPanel) return;
            
            const allItems = [
                ...document.querySelectorAll('.setting-item'),
                ...document.querySelectorAll('.theme-option')
            ];
            
            if (allItems.length === 0) return;
            
            switch(e.key) {
                case 'Tab':
                    e.preventDefault();
                    this.navigateFocus(allItems, 1);
                    break;
                case 'ArrowUp':
                    if (e.target.matches('.toggle-option, .theme-option')) {
                        e.preventDefault();
                        this.navigateFocus(allItems, -1);
                    }
                    break;
                case 'ArrowDown':
                    if (e.target.matches('.toggle-option, .theme-option')) {
                        e.preventDefault();
                        this.navigateFocus(allItems, 1);
                    }
                    break;
                case 'ArrowLeft':
                    if (e.target.matches('.toggle-option')) {
                        e.preventDefault();
                        this.navigateOptions(e.target, -1);
                    }
                    break;
                case 'ArrowRight':
                    if (e.target.matches('.toggle-option')) {
                        e.preventDefault();
                        this.navigateOptions(e.target, 1);
                    }
                    break;
                case 'Enter':
                case ' ':
                    if (e.target.matches('.toggle-option, .theme-option')) {
                        e.preventDefault();
                        e.target.click();
                    }
                    break;
            }
        });
    }
    
    navigateFocus(items, direction) {
        items.forEach(item => item.classList.remove('focused'));
        
        this.currentFocusIndex += direction;
        if (this.currentFocusIndex < 0) this.currentFocusIndex = items.length - 1;
        if (this.currentFocusIndex >= items.length) this.currentFocusIndex = 0;
        
        const currentItem = items[this.currentFocusIndex];
        currentItem.classList.add('focused');
        
        // Focus appropriate control
        if (currentItem.classList.contains('setting-item')) {
            const activeOption = currentItem.querySelector('.toggle-option.active');
            if (activeOption) activeOption.focus();
        } else if (currentItem.classList.contains('theme-option')) {
            currentItem.focus();
        }
    }
    
    navigateOptions(currentOption, direction) {
        const options = Array.from(currentOption.parentElement.querySelectorAll('.toggle-option'));
        const currentIndex = options.indexOf(currentOption);
        let newIndex = currentIndex + direction;
        
        if (newIndex < 0) newIndex = options.length - 1;
        if (newIndex >= options.length) newIndex = 0;
        
        options[newIndex].click();
        options[newIndex].focus();
    }
}