# Pip-Boy Progressive Web App (PWA)

## Overview
A browser-based Progressive Web App implementation of the Pip-Boy interface from the Fallout series. This PWA provides an authentic retro interface with tab navigation, visual effects, and offline capability - all running in modern web browsers.

## Recent Changes (September 23, 2025)
- ✅ **PWA Conversion**: Successfully converted from Pygame desktop app to Progressive Web App
- ✅ **Web Server**: Running on port 5000 with proper MIME types and headers
- ✅ **Service Worker**: Implemented for offline functionality with cache-first strategy
- ✅ **PWA Manifest**: Configured for installability as standalone app
- ✅ **Tab System**: Ported tab/sub-tab navigation to JavaScript
- ✅ **Visual Effects**: Recreated CRT effects, scanlines, and glitches in CSS/JS
- ✅ **Framework API**: Clean, content-agnostic interface exposed via window.PipBoyAPI
- ✅ **Enhanced CRT Effects**: More pronounced with adjustable intensity controls
- ✅ **Settings Tab**: Added under DATA tab with retro-style controls
- ✅ **Color Themes**: Blue, amber, red, white themes in addition to classic green
- ✅ **Persistent Settings**: All visual preferences saved in localStorage

## Project Architecture

### Core Structure
- **pipboy-pwa/index.html**: Main HTML structure with semantic layout
- **pipboy-pwa/styles.css**: Complete Pip-Boy styling with animations and effects
- **pipboy-pwa/app.js**: Tab navigation system and framework API
- **pipboy-pwa/effects.js**: Visual effects (CRT, glitch, scanlines, boot sequence)
- **pipboy-pwa/service-worker.js**: Offline caching and PWA functionality
- **pipboy-pwa/manifest.json**: PWA manifest for installation
- **pipboy-pwa/server.py**: Python web server serving on port 5000

### Key Features
- **Tab System**: 5 main tabs (STAT, INV, DATA, MAP, RADIO) with sub-tabs
- **Navigation**: Keyboard (arrow keys) and mouse/touch support
- **Visual Effects**: CRT monitor simulation, scanlines, phosphor glow, glitches
- **PWA Capabilities**: Offline functionality, installable as standalone app
- **Framework API**: window.PipBoyAPI for dynamic content registration

## User Preferences
- **Technology**: Progressive Web App for browser deployment
- **Port**: 5000 for web server
- **Styling**: Authentic green (#00ff00) on black retro terminal aesthetic
- **Effects**: CRT monitor effects, scanlines, glitches for authenticity
- **Framework**: Content-agnostic design for flexibility

## Technical Notes

### PWA Implementation
- Service Worker with cache-first strategy for offline functionality
- Relative paths for proper scope and installation
- Manifest configured for standalone app installation
- Responsive design that fills the viewport

### Browser Compatibility
- Works in all modern browsers (Chrome, Firefox, Safari, Edge)
- Progressive enhancement for older browsers
- Touch and keyboard navigation support
- Mobile and desktop compatible

## Running the Application
The PWA runs via the configured workflow:
```bash
cd pipboy-pwa && python3 server.py
```
Access at: http://localhost:5000

## Development Notes
- Use window.PipBoyAPI to register custom tabs and content
- Visual effects can be toggled via effects.js settings
- Service Worker caches all assets for offline use
- Install as PWA via browser's "Install App" option
- Framework is content-agnostic - ready for any data integration