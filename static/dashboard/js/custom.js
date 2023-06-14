const imageInput = document.getElementById('image-input');
    const imageError = document.getElementById('image-error');
    imageInput.addEventListener('change', function() {
    const file = this.files[0];
    const allowedTypes = ['image/png', 'image/jpeg', 'image/svg+xml'];

    if (!file || !allowedTypes.includes(file.type)) {
        imageError.textContent = 'Please select a valid image file (PNG, JPEG, or SVG).';
        imageInput.value = ''; // Clear the file input value
    } else {
        imageError.textContent = ''; // Clear any previous error message
    }
    });
const imageInp = document.getElementById('image-inputs');
  const imageErro = document.getElementById('image-errors');
    console.log(imageInp,'sifNdaxo');
    imageInp.addEventListener('change', function() {
    const file = this.files[0];
    const allowedTypes = ['image/png', 'image/jpeg', 'image/svg+xml'];

    if (!file || !allowedTypes.includes(file.type)) {
      imageErro.textContent = 'Please select a valid image file (PNG, JPEG, or SVG).';
      imageInp.value = ''; // Clear the file input value
    } else {
      imageErro.textContent = ''; // Clear any previous error message
    }
  });
