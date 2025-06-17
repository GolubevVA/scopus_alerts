const TG_KEY = "tk961c232af3d8b4caea"

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initSmoothScrolling();
    initScrollAnimations();
    initHeaderScrollEffect();
    initButtonAnimations();
    initIntersectionObserver();
});

// Smooth scrolling for navigation links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('.nav__link[href^="#"]');
    const footerLinks = document.querySelectorAll('.footer__links a[href^="#"]');
    const allLinks = [...navLinks, ...footerLinks];

    allLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Header scroll effect
function initHeaderScrollEffect() {
    const header = document.querySelector('.header');

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > 100) {
            header.style.background = 'rgba(255, 255, 255, 0.98)';
            header.style.boxShadow = '0 2px 20px rgba(139, 92, 246, 0.1)';
        } else {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
            header.style.boxShadow = 'none';
        }
    });
}

// Button animations and interactions
function initButtonAnimations() {
    const buttons = document.querySelectorAll('.btn');

    buttons.forEach(button => {
        // Add ripple effect on click
        // button.addEventListener('click', function(e) {
        //     const ripple = document.createElement('span');
        //     const rect = this.getBoundingClientRect();
        //     const size = Math.max(rect.width, rect.height);
        //     const x = e.clientX - rect.left - size / 2;
        //     const y = e.clientY - rect.top - size / 2;
        //
        //     ripple.style.width = ripple.style.height = size + 'px';
        //     ripple.style.left = x + 'px';
        //     ripple.style.top = y + 'px';
        //     ripple.classList.add('ripple');
        //
        //     this.appendChild(ripple);
        //
        //     // Remove ripple after animation
        //     setTimeout(() => {
        //         ripple.remove();
        //     }, 600);
        // });

        // Add hover effect
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });

        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // CTA button special effects
    // const ctaButtons = document.querySelectorAll('.hero__cta, .cta__button');
    // ctaButtons.forEach(button => {
    //     button.addEventListener('click', function(e) {
    //         e.preventDefault();
    //
    //         // Show alert for demo purposes
    //         // showNotification('Скоро! Телеграм-бот находится в разработке 🚀');
    //     });
    // });
}

// Intersection Observer for scroll animations
function initIntersectionObserver() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-on-scroll');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements that should animate on scroll
    const animatedElements = document.querySelectorAll(
        '.feature, .audience-card, .advantage, .step'
    );

    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// Scroll animations for various elements
function initScrollAnimations() {
    const animateElements = document.querySelectorAll(
        '.section__header, .about__text, .hero__content'
    );

    const animationObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -30px 0px'
    });

    animateElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        animationObserver.observe(element);
    });
}

// Show notification function
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        <div class="notification__content">
            <span class="notification__icon">ℹ️</span>
            <span class="notification__message">${message}</span>
            <button class="notification__close" onclick="this.parentElement.parentElement.style.display='none'">×</button>
        </div>
    `;

    // Add notification styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: linear-gradient(135deg, #8B5CF6 0%, #A855F7 100%);
        color: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3);
        z-index: 10000;
        max-width: 400px;
        animation: slideInRight 0.3s ease-out;
    `;

    // Add animation styles to head if not exists
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            .notification__content {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .notification__icon {
                font-size: 1.2em;
            }
            
            .notification__message {
                flex: 1;
                font-weight: 500;
            }
            
            .notification__close {
                background: none;
                border: none;
                color: white;
                font-size: 1.5em;
                cursor: pointer;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: background-color 0.2s ease;
            }
            
            .notification__close:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            
            .ripple {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transform: scale(0);
                animation: ripple-animation 0.6s linear;
                pointer-events: none;
            }
            
            @keyframes ripple-animation {
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideInRight 0.3s ease-out reverse';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }, 5000);
}

// Add hover effects to cards
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.feature, .audience-card, .advantage');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.transition = 'all 0.3s ease';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Parallax effect for hero section
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');

    if (hero) {
        const rate = scrolled * -0.5;
        hero.style.transform = `translateY(${rate}px)`;
    }
});

// Add loading animation
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-in-out';

    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Keyboard navigation support
document.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', function() {
    document.body.classList.remove('keyboard-navigation');
});

// Add focus styles for keyboard navigation
const style = document.createElement('style');
style.textContent = `
    .keyboard-navigation *:focus {
        outline: 3px solid #A855F7 !important;
        outline-offset: 2px !important;
    }
`;
document.head.appendChild(style);

/* ------------------------------------------------------------------ */
/*  Language selector – Tom Select                                    */
/* ------------------------------------------------------------------ */

function initLanguageSelector() {
  // --- 1. Справочник языков (добавьте остальные при желании) --------

  var ISO6393 = [
    ["afr", "Afrikaans"], ["ara", "Arabic"],    ["eng", "English"],
    ["ces", "Czech"],     ["chv", "Chuvash"],   ["deu", "German"],
    ["fra", "French"],    ["ita", "Italian"],   ["jpn", "Japanese"],
    ["pol", "Polish"],    ["por", "Portuguese"],["rus", "Russian"],
    ["spa", "Spanish"],   ["zho", "Chinese"]
    // …
  ];

  // --- 2. DOM узлы --------------------------------------------------
  const modal   = document.getElementById('language-modal');
  const backdrop= modal.querySelector('.modal__backdrop');
  const select  = document.getElementById('language-select');
  const btnOk   = document.getElementById('language-confirm');
  const btnNo   = document.getElementById('language-cancel');

  // --- 3. Генерируем <option> --------------------------------------
  select.innerHTML = iso6393.map(
    (item) => `<option value="${item.iso6393}">${item.name} (${item.iso6393})</option>`
  ).join('');

  // --- 4. Инициализируем Tom Select --------------------------------
  const ts = new TomSelect(select, {
    // поиск одновременно по label и value
    searchField: ['text', 'value'],
    create: false,
    highlight: true,
    openOnFocus: true,
      allowEmptyOption : true,
    render: {
      option: (data, escape) =>
        `<div>${escape(data.text.replace(`(${data.value})`,''))} <span class="ts__code">(${escape(data.value)})</span></div>`
    }
  });

  ts.clear();



  // --- 5. Показ / скрытие модалки ----------------------------------
  const open  = () => { modal.classList.remove('hidden'); ts.clear(); ts.focus(); };
  const close = () => { modal.classList.add('hidden');  ts.clear(); ts.clear(); };

  // --- 6. Переход к боту -------------------------------------------
  function go() {
    const lang = ts.getValue();
    if (!lang) return;                                 // ничего не выбрано
    window.location.href = `https://t.me/PushyTgBot?start=sub_${TG_KEY}_${lang}`;
  }

  btnOk     .addEventListener('click',  go);
  select    .addEventListener('keydown', e => e.key==='Enter' && go());
  btnNo     .addEventListener('click',  close);
  backdrop  .addEventListener('click',  close);
  document  .addEventListener('keydown', e => e.key==='Escape' && close());

  // --- 7. Открываем по клику CTA-кнопок -----------------------------
  document.querySelectorAll('.hero__cta, .cta__button')
    .forEach(btn => btn.addEventListener('pointerdown', e => {
      e.preventDefault(); open();
    }));
}

document.addEventListener('DOMContentLoaded', initLanguageSelector);
