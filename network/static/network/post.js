document.addEventListener('DOMContentLoaded', function () {

  document.addEventListener('click', event => {
    const element = event.target;
    const classList = element.classList;

    //editing post
    //hide post text, show textarea
    if (classList.contains("editbtn")) {
      const postId = element.id.slice(1);
      element.style.visibility = 'hidden';
      document.querySelector(`#post-content${postId}`).style.display = 'none';
      document.querySelector(`#edit-content${postId}`).style.display = 'block';
    }

    //cansel editing
    else if (classList.contains("cansel-edit-btn")) {
      const postId = element.id.slice(1);
      showPost(postId);
    }

    //confirm editing, save new post content
    else if (classList.contains("confirm-edit-btn")) {
      const domain = window.location.origin
      const postId = element.id.slice(1);
      const newText = document.querySelector(`#new-message-text${postId}`).value;
      fetch(`${domain}/edit`, {
        method: 'PUT',
        body: JSON.stringify({
          text: newText,
          id: postId
        })
      })
        .then(() => {
          document.querySelector(`#post-content${postId}`).innerHTML = newText;
          showPost(postId);
        })
    }

    //adding or deleting like
    else if (classList.contains("bi-suit-heart-fill")) {
      const domain = window.location.origin
      const postId = element.id.slice(1);
      fetch(`${domain}/like`, {
        method: 'PUT',
        body: JSON.stringify({
          id: postId
        })
      })
        .then((res) => {
          const likesCount = document.querySelector(`#likes${postId}`).innerHTML;
          if (res.status === 200) {
            document.querySelector(`#likes${postId}`).innerHTML = +likesCount + 1;
            document.querySelector(`#l${postId}`).style.color = 'rgb(255, 0, 98)';
          } else {
            document.querySelector(`#likes${postId}`).innerHTML = likesCount > 0 ? likesCount - 1 : 0;
            document.querySelector(`#l${postId}`).style.color = 'gray';
          }
        })
    }
  })
})

//hiding edit-post-form, showing post
function showPost(postId) {
  document.querySelector(`#e${postId}`).style.visibility = 'visible';
  document.querySelector(`#post-content${postId}`).style.display = 'block';
  document.querySelector(`#edit-content${postId}`).style.display = 'none';
}