
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCookie(value) {
    const date = new Date();
    date.setTime(date.getTime() + (3 * 24 * 60 * 60 * 1000));
    let expires = "expires=" + date.toUTCString();
    document.cookie = `theme_cookie=${value}; ${expires}; path=/; SameSite=Lax`;
}

const theme = getCookie('theme_cookie');
console.log('Значение куки:', theme);
const themeSwitch = document.getElementById('theme');

if (theme === 'dark') {
    document.body.setAttribute('data-bs-theme', 'dark');
    if (themeSwitch) themeSwitch.checked = true;
} else {
    document.body.setAttribute('data-bs-theme', 'light');
    if (themeSwitch) themeSwitch.checked = false;
}

document.addEventListener('DOMContentLoaded', function() {
    const theme = getCookie('theme_cookie');
    console.log('Значение куки:', theme);

    const themeSwitch = document.getElementById('theme');
    
    
    if (themeSwitch) {
        themeSwitch.addEventListener('change', function() {
            if (this.checked) {
                document.body.setAttribute('data-bs-theme', 'dark');
                setCookie('dark');
                console.log("dark");
            } else {
                document.body.setAttribute('data-bs-theme', 'light');
                setCookie('light');
                console.log("light");
            }
        });
    }

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
  
        if (windowHeight - sectionHeight - footerHeight - navbarHeight <= 0) {
          aside.style.height = '100hv';
          console.log("100hv");
        }
      }
    }
  
    window.addEventListener('load', setAsideHeight);
    window.addEventListener('resize', setAsideHeight);
  
    const avatarElement = document.getElementById('avatar');
  
    if (avatarElement) {
      avatarElement.addEventListener('change', function(event) {
        const file = event.target.files[0];
        
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
    }
  });
  
  document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('search-input');
    const list = document.getElementById('list');
    const searchForm = document.getElementById('search-form');
  
    let lastResults = [];
  
    input.addEventListener('input', function() {
      const query = this.value.trim();
      const curlen = query.length;
      if (curlen % 2 === 0) {
        Search(query);
      }
    });
    
    function Search(query) {
      console.log("start search");
      fetch(`/suggestions/?q=${encodeURIComponent(query)}`)
        .then(response => {
          if (!response.ok) throw new Error('Network error');
          return response.json();
        })
        .then(data => {
          console.log("get");
          if (data.results?.length > 0) {
            lastResults = data.results;
            show(lastResults);
          } else {
            lastResults = [];
            hide();
          }
        })
        .catch(error => {
          console.error('Search error:', error);
          lastResults = [];
          hide();
        });
    }
    
    function show(results) {
      console.log("change");
      list.innerHTML = results.map(item => `
        <a class="dropdown-item d-block" href="/question/${item.id}/">
          <div class="fw-bold">${item.title}</div>
          <small class="text-muted">${item.text.substring(0, 70)}${item.text.length > 70 ? '...' : ''}</small>
        </a>
      `).join('');
      
      list.classList.add('show');
      list.style.display = 'block';
    }
    
    function hide() {
      list.classList.remove('show');
      list.style.display = 'none';
    }
    
    document.addEventListener('click', function(e) {
      if (!searchForm.contains(e.target)) {
        hide();
      } else if (input.value.trim().length >= 3 && lastResults.length > 0) {
        show(lastResults);
      }
    });
    
    searchForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const query = input.value.trim();
      if (query) {
        window.location.href = `/search/?q=${encodeURIComponent(query)}`;
      }
    });
  });