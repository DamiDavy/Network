document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.edit').forEach(function (div) {
    div.style.display = 'none';
  })

  document.addEventListener('click', event => {
    const element = event.target;

    if (element.classList.contains("editbtn")) {
      document.querySelectorAll('.post').forEach(function (div) {
        div.style.display = 'block';
      })
      element.parentElement.style.display = 'none';

      const num = element.id.slice(1);
      document.querySelectorAll('.edit').forEach(function (div) {
        div.style.display = 'none';
      })
      document.querySelector(`#edit${num}`).style.display = 'block';
    }
  })


  document.querySelectorAll('.like').forEach(function (a) {
    a.addEventListener('click', () => {
      const n = a.id.slice(1);
      const user = document.querySelector('#user').innerHTML;
      fetch(`/like/${n}`, {
        method: 'PUT',
        body: JSON.stringify({
          likes: "action"
        })
      })
      fetch(`/like/${n}`)
      .then(response => response.json())
      .then(post => {
        const likes = post["likes"];
        console.log(likes);
        document.querySelector(`#likes${n}`).innerHTML = likes.length;
        if (likes.includes(user)) {
          document.querySelector(`#i${n}`).style.color = 'Blue';
        }
        else {
          document.querySelector(`#i${n}`).style.color = 'Red';
        }
      })
    });
  })
})
