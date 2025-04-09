document.addEventListener('DOMContentLoaded', function() {
    
  
  function setAsideHeight() {
    const navbar = document.querySelector('.navbar');
    const footer = document.querySelector('.footer');
    const section = document.querySelector('section');
    const aside = document.querySelector('aside');

    if (navbar && footer && aside && section) {
      const navbarHeight = navbar.offsetHeight;
      const footerHeight = footer.offsetHeight;
      const windowHeight = window.innerHeight;
      const sectionHeight = section.offsetHeight;

      aside.style.minHeight = `${windowHeight - navbarHeight - footerHeight - 16}px`;

      if (windowHeight - sectionHeight  - footerHeight - navbarHeight <= 0) {
        aside.style.height = '100hv';
        console.log("100hv");
      }
    }
  }

  window.addEventListener('load', setAsideHeight);
  window.addEventListener('resize', setAsideHeight);
});


document.addEventListener('DOMContentLoaded', function() {
  const themeSwitch = document.getElementById('theme');

  themeSwitch.addEventListener('change', function() {
      if (this.checked) {
          document.body.setAttribute('data-bs-theme', 'dark');
          console.log("dark");
      } else {
          document.body.setAttribute('data-bs-theme', 'light');
          console.log("light");
      }
  });
});

