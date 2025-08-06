// 🌿 Smooth Scroll on Anchor Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// 🌿 Shrink Navbar on Scroll (like Sugar Cosmetics)
window.addEventListener('scroll', () => {
  const navbar = document.querySelector('.header');
  if (window.scrollY > 60) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

// 🌿 Scroll to Top Button
const scrollBtn = document.createElement('button');
scrollBtn.innerText = "↑";
scrollBtn.className = "scroll-to-top";
document.body.appendChild(scrollBtn);

scrollBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

window.addEventListener('scroll', () => {
  scrollBtn.style.display = window.scrollY > 300 ? 'block' : 'none';
});

// 🌿 Fade-in Animation on Scroll
const faders = document.querySelectorAll('.fade-in');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.3
});

faders.forEach(el => observer.observe(el));
