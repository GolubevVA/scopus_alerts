class ScopusAlertsPresentation {
    constructor() {
        this.currentSlide = 1;
        this.totalSlides = 9;
        this.isAnimating = false;
        
        this.init();
    }
    
    init() {
        this.cacheElements();
        this.bindEvents();
        this.updateUI();
    }
    
    cacheElements() {
        this.slidesContainer = document.getElementById('slidesContainer');
        this.slides = document.querySelectorAll('.slide');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.currentSlideSpan = document.getElementById('currentSlide');
        this.totalSlidesSpan = document.getElementById('totalSlides');
        this.progressFill = document.getElementById('progressFill');
        this.fullscreenBtn = document.getElementById('fullscreenBtn');
    }
    
    bindEvents() {
        // Navigation buttons
        this.prevBtn.addEventListener('click', () => this.previousSlide());
        this.nextBtn.addEventListener('click', () => this.nextSlide());
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                e.preventDefault();
                this.previousSlide();
            } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
                e.preventDefault();
                this.nextSlide();
            } else if (e.key === 'Home') {
                e.preventDefault();
                this.goToSlide(1);
            } else if (e.key === 'End') {
                e.preventDefault();
                this.goToSlide(this.totalSlides);
            } else if (e.key === 'F11' || (e.key === 'f' && e.ctrlKey)) {
                e.preventDefault();
                this.toggleFullscreen();
            }
        });
        
        // Fullscreen button
        this.fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        
        // Handle fullscreen change events
        document.addEventListener('fullscreenchange', () => this.handleFullscreenChange());
        document.addEventListener('webkitfullscreenchange', () => this.handleFullscreenChange());
        document.addEventListener('mozfullscreenchange', () => this.handleFullscreenChange());
        document.addEventListener('MSFullscreenChange', () => this.handleFullscreenChange());
        
        // Touch/swipe support
        this.addTouchSupport();
        
        // Prevent context menu on presentation
        document.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
    }
    
    addTouchSupport() {
        let startX = 0;
        let startY = 0;
        let endX = 0;
        let endY = 0;
        
        this.slidesContainer.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        
        this.slidesContainer.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            
            const deltaX = endX - startX;
            const deltaY = endY - startY;
            const minSwipeDistance = 50;
            
            // Horizontal swipe is more significant than vertical
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > minSwipeDistance) {
                if (deltaX > 0) {
                    // Swipe right - go to previous slide
                    this.previousSlide();
                } else {
                    // Swipe left - go to next slide
                    this.nextSlide();
                }
            }
        });
    }
    
    nextSlide() {
        if (this.isAnimating) return;
        
        if (this.currentSlide < this.totalSlides) {
            this.goToSlide(this.currentSlide + 1);
        }
    }
    
    previousSlide() {
        if (this.isAnimating) return;
        
        if (this.currentSlide > 1) {
            this.goToSlide(this.currentSlide - 1);
        }
    }
    
    goToSlide(slideNumber) {
        if (this.isAnimating || slideNumber === this.currentSlide) return;
        if (slideNumber < 1 || slideNumber > this.totalSlides) return;
        
        this.isAnimating = true;
        
        const previousSlide = this.currentSlide;
        this.currentSlide = slideNumber;
        
        // Remove active class from all slides
        this.slides.forEach(slide => {
            slide.classList.remove('active', 'prev');
        });
        
        // Add prev class to previous slide for exit animation
        if (previousSlide !== slideNumber) {
            this.slides[previousSlide - 1].classList.add('prev');
        }
        
        // Add active class to current slide
        setTimeout(() => {
            this.slides[slideNumber - 1].classList.add('active');
            this.updateUI();
            
            // Reset animation flag after transition
            setTimeout(() => {
                this.isAnimating = false;
                // Clean up prev class
                this.slides.forEach(slide => {
                    slide.classList.remove('prev');
                });
            }, 300);
        }, 50);
    }
    
    updateUI() {
        // Update slide counter
        this.currentSlideSpan.textContent = this.currentSlide;
        this.totalSlidesSpan.textContent = this.totalSlides;
        
        // Update progress bar
        const progressPercentage = (this.currentSlide / this.totalSlides) * 100;
        this.progressFill.style.width = `${progressPercentage}%`;
        
        // Update navigation buttons
        this.prevBtn.disabled = this.currentSlide === 1;
        this.nextBtn.disabled = this.currentSlide === this.totalSlides;
        
        // Update button text for last slide
        if (this.currentSlide === this.totalSlides) {
            this.nextBtn.innerHTML = `
                Конец
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 12l2 2 4-4"></path>
                    <path d="M21 12c-1 0-3-1-3-3s2-3 3-3 3 1 3 3-2 3-3 3"></path>
                    <path d="M3 12c1 0 3-1 3-3s-2-3-3-3-3 1-3 3 2 3 3 3"></path>
                </svg>
            `;
        } else {
            this.nextBtn.innerHTML = `
                Вперед
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="9,18 15,12 9,6"></polyline>
                </svg>
            `;
        }
        
        // Update document title
        const slideTitle = this.slides[this.currentSlide - 1].querySelector('.slide-title, .main-title');
        if (slideTitle) {
            document.title = `${slideTitle.textContent} - Scopus Alerts`;
        }
    }
    
    toggleFullscreen() {
        if (!document.fullscreenElement) {
            this.enterFullscreen();
        } else {
            this.exitFullscreen();
        }
    }
    
    enterFullscreen() {
        const elem = document.documentElement;
        
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.webkitRequestFullscreen) {
            elem.webkitRequestFullscreen();
        } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen();
        }
    }
    
    exitFullscreen() {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }
    
    handleFullscreenChange() {
        const isFullscreen = !!(document.fullscreenElement || 
                               document.webkitFullscreenElement || 
                               document.mozFullScreenElement || 
                               document.msFullscreenElement);
        
        if (isFullscreen) {
            this.fullscreenBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"></path>
                </svg>
            `;
            this.fullscreenBtn.title = 'Выйти из полноэкранного режима';
        } else {
            this.fullscreenBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>
                </svg>
            `;
            this.fullscreenBtn.title = 'Полноэкранный режим';
        }
    }
    
    // Public methods for external control
    getCurrentSlide() {
        return this.currentSlide;
    }
    
    getTotalSlides() {
        return this.totalSlides;
    }
    
    // Auto-advance functionality (optional)
    startAutoAdvance(intervalMs = 30000) {
        this.autoAdvanceInterval = setInterval(() => {
            if (this.currentSlide < this.totalSlides) {
                this.nextSlide();
            } else {
                this.stopAutoAdvance();
            }
        }, intervalMs);
    }
    
    stopAutoAdvance() {
        if (this.autoAdvanceInterval) {
            clearInterval(this.autoAdvanceInterval);
            this.autoAdvanceInterval = null;
        }
    }
    
    // Utility method to add presentation controls info
    showHelp() {
        const helpText = `
Управление презентацией:
→ / ↓ / Space - Следующий слайд
← / ↑ - Предыдущий слайд  
Home - Первый слайд
End - Последний слайд
F11 / Ctrl+F - Полноэкранный режим
Swipe влево/вправо на мобильных устройствах
        `;
        
        alert(helpText);
    }
}

// Enhanced slide content animations
class SlideAnimations {
    static animateSlideContent(slide) {
        const elements = slide.querySelectorAll('.benefit-item, .step-item, .tech-item, .limitation-item, .solution-item');
        
        elements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateX(-30px)';
            
            setTimeout(() => {
                element.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
                element.style.opacity = '1';
                element.style.transform = 'translateX(0)';
            }, index * 100 + 200);
        });
    }
    
    static resetSlideAnimations(slide) {
        const elements = slide.querySelectorAll('.benefit-item, .step-item, .tech-item, .limitation-item, .solution-item');
        
        elements.forEach(element => {
            element.style.transition = '';
            element.style.opacity = '';
            element.style.transform = '';
        });
    }
}

// Keyboard shortcuts helper
class KeyboardShortcuts {
    static init(presentation) {
        document.addEventListener('keydown', (e) => {
            // Prevent default browser shortcuts during presentation
            if (e.key === 'F5' || (e.ctrlKey && e.key === 'r')) {
                e.preventDefault();
                // Optional: show help instead of refresh
                if (e.shiftKey) {
                    presentation.showHelp();
                }
            }
            
            // Quick slide navigation with numbers
            if (e.key >= '1' && e.key <= '9') {
                const slideNumber = parseInt(e.key);
                if (slideNumber <= presentation.getTotalSlides()) {
                    presentation.goToSlide(slideNumber);
                }
            }
            
            // Help shortcut
            if (e.key === 'h' || e.key === 'H' || e.key === '?') {
                presentation.showHelp();
            }
        });
    }
}

// Initialize presentation when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const presentation = new ScopusAlertsPresentation();
    KeyboardShortcuts.init(presentation);
    
    // Add presentation instance to window for debugging
    window.presentation = presentation;
    
    // Show initial slide with animation
    setTimeout(() => {
        SlideAnimations.animateSlideContent(document.querySelector('.slide.active'));
    }, 500);
    
    // Add slide change observer for animations
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                const slide = mutation.target;
                if (slide.classList.contains('active')) {
                    setTimeout(() => {
                        SlideAnimations.animateSlideContent(slide);
                    }, 100);
                } else {
                    SlideAnimations.resetSlideAnimations(slide);
                }
            }
        });
    });
    
    // Observe all slides for class changes
    document.querySelectorAll('.slide').forEach(slide => {
        observer.observe(slide, { attributes: true, attributeFilter: ['class'] });
    });
    
    // Prevent accidental page navigation
    window.addEventListener('beforeunload', (e) => {
        if (presentation.getCurrentSlide() > 1) {
            e.preventDefault();
            e.returnValue = 'Вы уверены, что хотите покинуть презентацию?';
        }
    });
    
    // Handle visibility change (tab switching)
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            presentation.stopAutoAdvance();
        }
    });
    
    // Console message for developers
    console.log(`
🎯 Scopus Alerts Presentation
📊 Слайдов: ${presentation.getTotalSlides()}
⌨️  Нажмите 'h' для помощи по управлению
🔧 Доступ к презентации: window.presentation
    `);
});