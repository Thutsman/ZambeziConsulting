const navbar = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
const navLinks = document.querySelectorAll('.nav-links a, .nav-mobile a');
const hero = document.querySelector('.hero');
const heroBg = document.getElementById('heroBg');

function initHero() {
  if (!hero) return;
  requestAnimationFrame(() => hero.classList.add('is-mounted'));

  if (!heroBg || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  let parallaxTicking = false;
  const onParallax = () => {
    if (parallaxTicking) return;
    parallaxTicking = true;
    requestAnimationFrame(() => {
      const rect = hero.getBoundingClientRect();
      if (rect.bottom > 0 && rect.top < window.innerHeight) {
        const progress = Math.min(1, Math.max(0, -rect.top / (rect.height * 0.85)));
        const y = progress * 28;
        const scale = 1.04 + progress * 0.02;
        heroBg.style.transform = `scale(${scale}) translate3d(0, ${y}px, 0)`;
      }
      parallaxTicking = false;
    });
  };
  window.addEventListener('scroll', onParallax, { passive: true });
  onParallax();
}

initHero();

function updateNavbar() {
  const navH = navbar.offsetHeight;
  const heroRect = hero?.getBoundingClientRect();
  const heroAtTop = heroRect && heroRect.top <= 0 && heroRect.bottom > navH + 48;
  const scrolled = window.scrollY > 72 || !heroAtTop;
  navbar.classList.toggle('scrolled', scrolled);

  const sections = ['home', 'about', 'services', 'team', 'portfolio', 'contact'];
  let current = 'home';
  for (const id of sections) {
    const el = document.getElementById(id);
    if (el && window.scrollY >= el.offsetTop - 130) current = id;
  }
  navLinks.forEach((a) => {
    a.classList.toggle('active', a.getAttribute('href') === '#' + current);
  });
}

window.addEventListener('scroll', updateNavbar, { passive: true });
window.addEventListener('resize', updateNavbar);
updateNavbar();

if (hero) {
  const heroObserver = new IntersectionObserver(
    () => updateNavbar(),
    { threshold: [0, 0.01, 0.5, 1], rootMargin: `-${navbar.offsetHeight}px 0px 0px 0px` }
  );
  heroObserver.observe(hero);
}

hamburger.addEventListener('click', () => {
  mobileMenu.classList.toggle('open');
});

mobileMenu.querySelectorAll('a').forEach((a) => {
  a.addEventListener('click', () => mobileMenu.classList.remove('open'));
});

const revealEls = document.querySelectorAll('.reveal');
const revealObs = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        revealObs.unobserve(e.target);
      }
    });
  },
  { threshold: 0.12 }
);
revealEls.forEach((el) => revealObs.observe(el));

document.querySelectorAll('a[href^="#"]').forEach((a) => {
  a.addEventListener('click', (e) => {
    e.preventDefault();
    const target = document.querySelector(a.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth' });
  });
});

document.querySelectorAll('img[data-fallback]').forEach((img) => {
  img.addEventListener('error', function onError() {
    const fallback = this.dataset.fallback;
    if (fallback && this.src !== fallback) {
      this.src = fallback;
      this.removeEventListener('error', onError);
    }
  });
});

function showLogoFallback(img) {
  const fallback = img.nextElementSibling;
  if (fallback && fallback.classList.contains('nav-logo-fallback')) {
    img.style.display = 'none';
    fallback.classList.add('show');
  }
}

function showFooterLogoFallback(img) {
  const fallback = img.nextElementSibling;
  if (fallback && fallback.classList.contains('footer-logo-fallback')) {
    img.style.display = 'none';
    fallback.classList.add('show');
  }
}

document.querySelectorAll('.nav-logo-img').forEach((img) => {
  img.addEventListener('error', () => showLogoFallback(img));
});

document.querySelectorAll('.footer-logo-img').forEach((img) => {
  img.addEventListener('error', () => showFooterLogoFallback(img));
});

const contactForm = document.getElementById('contactForm');
const formSuccess = document.getElementById('formSuccess');

if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    formSuccess.classList.add('show');
    contactForm.reset();
    setTimeout(() => formSuccess.classList.remove('show'), 5000);
  });
}
