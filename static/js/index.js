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

  document.getElementById('avatar').addEventListener('change', function(event) {
    console.log("av");
    const file = event.target.files[0];
    const previewContainer = document.getElementById('avatar-preview');
    const previewImage = document.getElementById('preview-image');
    
    if (file) {
      const reader = new FileReader();
      
      reader.onload = function(e) {
        previewImage.src = e.target.result;
        previewContainer.style.display = 'block';
      }
      
      reader.readAsDataURL(file);
    } else {
      previewImage.src = '#';
      previewContainer.style.display = 'none';
    }
  });
});