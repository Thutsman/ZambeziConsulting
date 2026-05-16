const navbar = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
const navLinks = document.querySelectorAll('.nav-links a, .nav-mobile a');

window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 60);
  const sections = ['home', 'about', 'services', 'portfolio', 'contact'];
  let current = 'home';
  for (const id of sections) {
    const el = document.getElementById(id);
    if (el && window.scrollY >= el.offsetTop - 130) current = id;
  }
  navLinks.forEach((a) => {
    a.classList.toggle('active', a.getAttribute('href') === '#' + current);
  });
});

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
