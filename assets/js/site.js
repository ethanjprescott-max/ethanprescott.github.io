document.documentElement.classList.add('js-enabled');

const menuButton = document.querySelector('.menu-toggle');
const sidebar = document.querySelector('.sidebar');
if (menuButton && sidebar) {
  const closeMenu = () => {
    sidebar.classList.remove('menu-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Open navigation');
  };
  menuButton.addEventListener('click', () => {
    const open = sidebar.classList.toggle('menu-open');
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  document.querySelectorAll('.sidebar-nav a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeMenu();
  });
}

const sections = document.querySelectorAll('main > section[id]');
if ('IntersectionObserver' in window && sections.length) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      document.querySelectorAll('.sidebar-nav a').forEach(link => {
        if (link.getAttribute('href') === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    });
  }, {rootMargin: '-15% 0px -60% 0px'});
  sections.forEach(section => observer.observe(section));
}

const dialog = document.querySelector('.lightbox');
if (dialog && typeof dialog.showModal === 'function') {
  const image = dialog.querySelector('img');
  const caption = dialog.querySelector('p');
  document.querySelectorAll('[data-gallery]').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      image.src = link.href;
      image.alt = link.dataset.caption || '';
      caption.textContent = link.dataset.caption || '';
      dialog.showModal();
    });
  });
  dialog.querySelector('.close-dialog').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
}

// Gentle background parallax, matching the reference portfolio's scroll behavior.
const photoMotion = window.matchMedia('(min-width: 761px) and (prefers-reduced-motion: no-preference)');
let photoFrame = false;
function updatePhotoPosition() {
  const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
  const progress = maxScroll > 0 ? Math.min(1, Math.max(0, window.scrollY / maxScroll)) : 0;
  if (sidebar) sidebar.style.setProperty('--photo-position', photoMotion.matches ? `${progress * 100}%` : '0%');
  photoFrame = false;
}
window.addEventListener('scroll', () => {
  if (!photoFrame) { photoFrame = true; window.requestAnimationFrame(updatePhotoPosition); }
}, { passive: true });
photoMotion.addEventListener('change', updatePhotoPosition);
window.addEventListener('resize', updatePhotoPosition, { passive: true });
window.addEventListener('load', updatePhotoPosition);
if ('ResizeObserver' in window) new ResizeObserver(updatePhotoPosition).observe(document.querySelector('main'));
updatePhotoPosition();

// Reveal headings once as they enter the viewport; content stays visible without JS.
const headingMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if ('IntersectionObserver' in window && !headingMotion.matches) {
  const headings = document.querySelectorAll('main h1, main .section-head, main .detail-heading, main .gallery-section > h2, main .video-section > h2, main .project-title');
  const headingObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -20px 0px' });
  headings.forEach((heading, index) => {
    heading.style.setProperty('--reveal-delay', `${Math.min(index % 2, 1) * 80}ms`);
    heading.classList.add('reveal-heading');
    headingObserver.observe(heading);
  });
  headingMotion.addEventListener('change', event => {
    if (event.matches) {
      headingObserver.disconnect();
      headings.forEach(heading => heading.classList.add('is-visible'));
    }
  });
}
