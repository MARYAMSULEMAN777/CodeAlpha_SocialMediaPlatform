const picInput = document.querySelector('input[type="file"][name="profile_pic"]');

if (picInput) {
  picInput.addEventListener('change', () => {
    const file = picInput.files[0];
    if (!file) return;

    let preview = document.getElementById('profile-pic-preview');
    if (!preview) {
      preview = document.createElement('img');
      preview.id = 'profile-pic-preview';
      preview.style.width = '72px';
      preview.style.height = '72px';
      preview.style.borderRadius = '50%';
      preview.style.objectFit = 'cover';
      preview.style.marginBottom = '10px';
      picInput.parentElement.insertBefore(preview, picInput);
    }
    preview.src = URL.createObjectURL(file);
  });
}
