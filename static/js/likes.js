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

var Buttons = document.querySelectorAll('button[data-id]')
Buttons.forEach(button => {
  const id = button.getAttribute('data-id');
  const type = button.getAttribute('data-type');
  const cur = button.getAttribute('data-cur');
  const object = button.getAttribute('data-object');
  const score = document.querySelector(`div[data-id="${id}"]`);
  const b1 = document.querySelector(`button[data-id="${id}"][data-type="like"]`);
  const b2 = document.querySelector(`button[data-id="${id}"][data-type="dislike"]`);
  if (cur === "True") {
    b1.style.backgroundImage = "url('/static/img/like-outline.png')";
    b2.style.backgroundImage = "url('/static/img/dislike.png')";
  } else if (cur === "False") {
    b1.style.backgroundImage = "url('/static/img/like.png')";
    b2.style.backgroundImage = "url('/static/img/dislike-outline.png')";
  } else {
    b1.style.backgroundImage = "url('/static/img/like.png')";
    b2.style.backgroundImage = "url('/static/img/dislike.png')";
  }
  });

var Checkboxes = document.querySelectorAll('input[data-id]')
Checkboxes.forEach(checkbox => {
  const id = checkbox.getAttribute('data-id');
  var cur = checkbox.getAttribute('data-cur');
  if (cur == "True") {
    checkbox.checked = true;
  } else {
    checkbox.checked = false;
  }
  });


document.addEventListener('click', function(event) {
  if (event.target.matches('button[data-id][data-type]')) {
      const button = event.target;
      const id = button.getAttribute('data-id');
      const type = button.getAttribute('data-type');
      const object = button.getAttribute('data-object');
      const score = document.querySelector(`div[data-id="${id}"]`);
      const b1 = document.querySelector(`button[data-id="${id}"][data-type="like"]`);
      const b2 = document.querySelector(`button[data-id="${id}"][data-type="dislike"]`);
      
      console.log(`Кнопка с data-id="${id}" была нажата`);
      const csrftoken = getCookie('csrftoken');
      const request = new Request(
          `/like/${id}/`,
          {
              method: 'POST',
              headers: {'X-CSRFToken': csrftoken},
              mode: 'same-origin',
              body: JSON.stringify({type: type, object: object}) 
          }
      );
      
      fetch(request).then(function(response) {
          return response.json();
      }).then(function(data) {         
          console.log(`"${data.status}"`);                                                              
          if (data.status == "None") {
              b1.style.backgroundImage = "url('/static/img/like.png')";
              b2.style.backgroundImage = "url('/static/img/dislike.png')";
          } else if (data.status == "True") {
              b1.style.backgroundImage = "url('/static/img/like-outline.png')";
              b2.style.backgroundImage = "url('/static/img/dislike.png')";
          } else {
              b1.style.backgroundImage = "url('/static/img/like.png')";
              b2.style.backgroundImage = "url('/static/img/dislike-outline.png')";
          }
          score.innerText = data.score;
          console.log(data); 
      }).catch(function(error) {
          console.error('Error:', error);
      });
  }
});

document.addEventListener('change', function(event) {
  if (event.target.matches('input[data-id]')) {
      const checkbox = event.target;
      const id = checkbox.getAttribute('data-id');
      
      console.log(`checked с data-id="${id}"`);
      const csrftoken = getCookie('csrftoken');
      const request = new Request(
          `/check/${id}/`,
          {
              method: 'POST',
              headers: {'X-CSRFToken': csrftoken},
              mode: 'same-origin',
          }
      );
      
      fetch(request).then(function(response) {
          return response.json();
      }).then(function(data) {         
          console.log(`"${data.status}"`);   
          checkbox.setAttribute('data-cur', data.status);
      }).catch(function(error) {
          console.error('Error:', error);
      });
  }
});
