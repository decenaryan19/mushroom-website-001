document.addEventListener('DOMContentLoaded', () => {
  initHeroCarousel();
  initMobileMenu();
  initBackToTop();
  initGallery();
  initProductPage();
  initSampleForm();
  initContactForm();
});

function initHeroCarousel() {
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.hero-dot');
  if (!slides.length) return;

  let current = 0;

  function goToSlide(index) {
    slides[current].classList.remove('is-active');
    dots[current]?.classList.remove('is-active');
    current = index;
    slides[current].classList.add('is-active');
    dots[current]?.classList.add('is-active');
  }

  dots.forEach((dot) => {
    dot.addEventListener('click', () => {
      goToSlide(Number(dot.dataset.slide));
    });
  });
}

function initMobileMenu() {
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');
  if (!btn || !menu) return;

  btn.addEventListener('click', () => {
    const isOpen = menu.classList.contains('is-open');
    menu.classList.toggle('is-open', !isOpen);
    btn.setAttribute('aria-expanded', String(!isOpen));
  });

  menu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      menu.classList.remove('is-open');
      btn.setAttribute('aria-expanded', 'false');
    });
  });
}

function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;
  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

function initGallery() {
  const pages = document.querySelectorAll('.gallery-page');
  const dots = document.querySelectorAll('.gallery-dot');
  const prev = document.getElementById('gallery-prev');
  const next = document.getElementById('gallery-next');
  if (!pages.length || !prev || !next) return;

  let current = 0;

  function showPage(index) {
    current = Math.max(0, Math.min(index, pages.length - 1));
    pages.forEach((page, i) => {
      const isActive = i === current;
      page.classList.toggle('is-active', isActive);
      page.hidden = !isActive;
    });
    dots.forEach((dot, i) => {
      const isActive = i === current;
      dot.classList.toggle('is-active', isActive);
      dot.setAttribute('aria-selected', String(isActive));
    });
    prev.disabled = current === 0;
    next.disabled = current === pages.length - 1;
  }

  prev.addEventListener('click', () => showPage(current - 1));
  next.addEventListener('click', () => showPage(current + 1));
  dots.forEach((dot) => {
    dot.addEventListener('click', () => showPage(Number(dot.dataset.page)));
  });
  showPage(0);
}

function initProductPage() {
  initQuantitySelector();
  initProductTabs();
  initImageLightbox();
  initProductForm();
}

function initQuantitySelector() {
  const input = document.getElementById('qty-input');
  const minus = document.getElementById('qty-minus');
  const plus = document.getElementById('qty-plus');
  if (!input || !minus || !plus) return;

  minus.addEventListener('click', () => {
    input.value = Math.max(1, parseInt(input.value, 10) - 1);
  });

  plus.addEventListener('click', () => {
    input.value = Math.min(99, parseInt(input.value, 10) + 1);
  });

  input.addEventListener('change', () => {
    let val = parseInt(input.value, 10);
    if (Number.isNaN(val) || val < 1) val = 1;
    if (val > 99) val = 99;
    input.value = val;
  });
}

function initProductTabs() {
  const tabs = document.querySelectorAll('.product-tab');
  if (!tabs.length) return;

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;
      tabs.forEach((t) => {
        t.classList.remove('is-active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('is-active');
      tab.setAttribute('aria-selected', 'true');

      document.querySelectorAll('.product-tab-panel').forEach((panel) => {
        const isActive = panel.id === `tab-${target}`;
        panel.classList.toggle('is-active', isActive);
        panel.hidden = !isActive;
      });
    });
  });
}

function initImageLightbox() {
  const lightbox = document.getElementById('image-lightbox');
  const expandBtn = document.getElementById('expand-image-btn');
  const closeBtn = document.getElementById('lightbox-close');
  const mainImage = document.getElementById('product-main-image');
  if (!lightbox || !expandBtn || !mainImage) return;

  expandBtn.addEventListener('click', () => {
    lightbox.querySelector('img').src = mainImage.currentSrc || mainImage.src;
    lightbox.hidden = false;
    document.body.style.overflow = 'hidden';
  });

  function closeLightbox() {
    lightbox.hidden = true;
    document.body.style.overflow = '';
  }

  closeBtn?.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !lightbox.hidden) closeLightbox();
  });
}

function initProductForm() {
  const form = document.getElementById('product-form');
  const packageSelect = document.getElementById('package-select');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!packageSelect?.value) {
      packageSelect?.focus();
      return;
    }
    alert('Thank you! Your order has been added to cart.');
  });
}

function initSampleForm() {
  const form = document.getElementById('sample-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thank you! Your free sample request has been submitted. We will contact you shortly.');
    form.reset();
  });
}

function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thank you for your message! We will get back to you soon.');
    form.reset();
  });
}

