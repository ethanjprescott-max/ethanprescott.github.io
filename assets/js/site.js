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
