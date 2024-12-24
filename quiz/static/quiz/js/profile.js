document.addEventListener('DOMContentLoaded', () => {
  console.log('script is loading')
  const inputphoto = document.querySelector('#nprofile-img')
  const picon = document.getElementById('picon');

  inputphoto.addEventListener('change', (e) => {
    const [file] = inputphoto.files
    if (file) {
      const pimage = document.getElementById('profile-img')
      console.log(pimage)
      pimage.src = URL.createObjectURL(file)
      document.getElementById('save-btn').disabled = false
      picon.style.display = 'none';
    } else {
      console.log('something went wrong')
    }
  })

  window.onload = function () {
    document.getElementById('nprofile-img').value = '';
  }

  const deleteButton = document.getElementById('delete-btn');

  deleteButton.addEventListener('click', function (event) {
    const confirmed = confirm('Are you sure you want to delete your account? This action cannot be undone.');

    if (!confirmed) {
      event.preventDefault();
    }
  });
})