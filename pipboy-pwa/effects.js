// Pip-Boy Framework - Visual Effects

class PipBoyEffects {
    constructor() {
        this.glitchActive = false;
        this.scanlineSpeed = 8;
        this.init();
    }
    
    init() {
        this.setupRandomGlitches();
        this.setupScreenFlicker();
        this.setupMouseGlow();
        this.addBootAnimation();
    }
    
    setupRandomGlitches() {
        // Random glitch effect
        setInterval(() => {
            if (Math.random() < 0.005) { // 0.5% chance every 100ms
                this.triggerRandomGlitch();
            }
        }, 100);
    }
    
    triggerRandomGlitch() {
        if (this.glitchActive) return;
        this.glitchActive = true;
        
        const glitchTypes = ['horizontal', 'vertical', 'color', 'static'];
        const type = glitchTypes[Math.floor(Math.random() * glitchTypes.length)];
        
        switch(type) {
            case 'horizontal':
                this.horizontalGlitch();
                break;
            case 'vertical':
                this.verticalGlitch();
                break;
            case 'color':
                this.colorGlitch();
                break;
            case 'static':
                this.staticGlitch();
                break;
        }
        
        setTimeout(() => {
            this.glitchActive = false;
        }, 200);
    }
    
    horizontalGlitch() {
        const screen = document.querySelector('.pipboy-screen');
        const lines = Math.floor(Math.random() * 5) + 2;
        
        for (let i = 0; i < lines; i++) {
            const line = document.createElement('div');
            line.style.position = 'absolute';
            line.style.left = '0';
            line.style.width = '100%';
            line.style.height = '2px';
            line.style.top = `${Math.random() * 100}%`;
            line.style.background = 'rgba(0, 255, 0, 0.5)';
            line.style.zIndex = '105';
            line.style.animation = 'horizontalShift 0.2s';
            
            screen.appendChild(line);
            
            setTimeout(() => line.remove(), 200);
        }
    }
    
    verticalGlitch() {
        const screen = document.querySelector('.pipboy-screen');
        screen.style.transform = `translateX(${Math.random() * 4 - 2}px)`;
        setTimeout(() => {
            screen.style.transform = 'translateX(0)';
        }, 100);
    }
    
    colorGlitch() {
        const elements = document.querySelectorAll('.pipboy-content *');
        elements.forEach(el => {
            if (Math.random() < 0.1) {
                el.style.textShadow = '2px 2px 0 rgba(255, 0, 0, 0.3), -2px -2px 0 rgba(0, 255, 255, 0.3)';
                setTimeout(() => {
                    el.style.textShadow = '';
                }, 150);
            }
        });
    }
    
    staticGlitch() {
        const overlay = document.createElement('div');
        overlay.style.position = 'absolute';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.background = `url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><filter id="static"><feTurbulence baseFrequency="0.9"/><feColorMatrix values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0"/></filter><rect width="100" height="100" filter="url(%23static)" opacity="0.1"/></svg>')`;
        overlay.style.opacity = '0.2';
        overlay.style.zIndex = '104';
        overlay.style.pointerEvents = 'none';
        overlay.style.mixBlendMode = 'screen';
        
        document.querySelector('.pipboy-container').appendChild(overlay);
        setTimeout(() => overlay.remove(), 100);
    }
    
    setupScreenFlicker() {
        // Subtle brightness flicker
        setInterval(() => {
            if (Math.random() < 0.01) {
                const screen = document.querySelector('.pipboy-screen');
                screen.style.opacity = '0.95';
                setTimeout(() => {
                    screen.style.opacity = '1';
                }, 50);
            }
        }, 1000);
    }
    
    setupMouseGlow() {
        const container = document.querySelector('.pipboy-container');
        let glowElement = document.createElement('div');
        glowElement.className = 'mouse-glow';
        glowElement.style.cssText = `
            position: absolute;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(0, 255, 0, 0.1) 0%, transparent 70%);
            pointer-events: none;
            z-index: 90;
            display: none;
        `;
        container.appendChild(glowElement);
        
        container.addEventListener('mousemove', (e) => {
            const rect = container.getBoundingClientRect();
            glowElement.style.display = 'block';
            glowElement.style.left = `${e.clientX - rect.left - 50}px`;
            glowElement.style.top = `${e.clientY - rect.top - 50}px`;
        });
        
        container.addEventListener('mouseleave', () => {
            glowElement.style.display = 'none';
        });
    }
    
    addBootAnimation() {
        // Initial boot sequence animation
        const screen = document.querySelector('.pipboy-screen');
        screen.style.opacity = '0';
        screen.style.transform = 'scale(0.9)';
        
        setTimeout(() => {
            screen.style.transition = 'opacity 1s, transform 0.5s';
            screen.style.opacity = '1';
            screen.style.transform = 'scale(1)';
            
            // Boot text sequence
            this.showBootSequence();
        }, 100);
    }
    
    showBootSequence() {
        const bootTexts = [
            'ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM',
            'COPYRIGHT 2075-2077 ROBCO INDUSTRIES',
            'LOADING PIPBOY FRAMEWORK...',
            'INITIALIZING...',
            'SYSTEM READY'
        ];
        
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: black;
            color: #00ff00;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 200;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.5;
        `;
        
        const textContainer = document.createElement('div');
        textContainer.style.textAlign = 'left';
        overlay.appendChild(textContainer);
        
        document.querySelector('.pipboy-container').appendChild(overlay);
        
        let index = 0;
        const typeText = () => {
            if (index < bootTexts.length) {
                const line = document.createElement('div');
                line.style.opacity = '0';
                line.textContent = bootTexts[index];
                textContainer.appendChild(line);
                
                setTimeout(() => {
                    line.style.transition = 'opacity 0.2s';
                    line.style.opacity = '1';
                }, 50);
                
                index++;
                setTimeout(typeText, 300);
            } else {
                setTimeout(() => {
                    overlay.style.transition = 'opacity 0.5s';
                    overlay.style.opacity = '0';
                    setTimeout(() => overlay.remove(), 500);
                }, 1000);
            }
        };
        
        setTimeout(typeText, 500);
    }
    
    // Additional effect: Phosphor trail
    addPhosphorTrail(element) {
        const trail = element.cloneNode(true);
        trail.style.position = 'absolute';
        trail.style.opacity = '0.3';
        trail.style.filter = 'blur(1px)';
        trail.style.zIndex = parseInt(element.style.zIndex || 0) - 1;
        trail.style.pointerEvents = 'none';
        
        element.parentElement.insertBefore(trail, element);
        
        setTimeout(() => {
            trail.style.transition = 'opacity 0.5s';
            trail.style.opacity = '0';
            setTimeout(() => trail.remove(), 500);
        }, 50);
    }
}

// CSS for horizontal shift animation
const style = document.createElement('style');
style.textContent = `
    @keyframes horizontalShift {
        0% { transform: translateX(0); }
        25% { transform: translateX(5px); }
        50% { transform: translateX(-3px); }
        75% { transform: translateX(2px); }
        100% { transform: translateX(0); }
    }
`;
document.head.appendChild(style);

// Initialize effects when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.pipboyEffects = new PipBoyEffects();
});