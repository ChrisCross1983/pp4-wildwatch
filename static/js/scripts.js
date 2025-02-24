// Scroll-to-Top Button
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.onscroll = function () {
  var scrollToTopBtn = document.getElementById('scrollToTopBtn');
  if (scrollToTopBtn) {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
      scrollToTopBtn.style.display = 'block';
    } else {
      scrollToTopBtn.style.display = 'none';
    }
  }
}

// Toggle Bubble Visibility
function toggleFab() {
  var fab = document.querySelector('.fab');
  if (fab) {
    if (window.innerWidth < 993) {
      fab.style.display = 'flex';
    } else {
      fab.style.display = 'none';
    }
  }
}

toggleFab();
window.addEventListener('resize', toggleFab);

// Sign Up Form and Profile Picture Preview
document.addEventListener('DOMContentLoaded', () => {
  console.log('>>> DOMContentLoaded - Form and Profil Image Preview <<<');

  // --- Form Submit Button Handling ---
  const form = document.querySelector('form');
  if (form) {
      form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
              event.preventDefault();
              form.reportValidity();
              return;
          }

          const submitButton = form.querySelector('button[type="submit"]');
          submitButton.disabled = true;
          const loadingText = submitButton.getAttribute('data-loading-text') || 'Signing up...';
          submitButton.innerHTML = loadingText;
      });
  } else {
      console.error('>>> Form not found! <<<');
  }

  // Profil Picture Preview
  const profilePictureInput = document.getElementById('id_profile_picture');
  const profilePicturePreview = document.getElementById('profilePicturePreview');

  if (profilePictureInput && profilePicturePreview) {
      profilePictureInput.addEventListener('change', (event) => {
          const file = event.target.files[0];
          if (file && file.type.startsWith('image/')) {
              const reader = new FileReader();
              reader.onload = (e) => {
                  profilePicturePreview.src = e.target.result;
              };
              reader.readAsDataURL(file);
          } else {
              profilePicturePreview.src = "/static/images/placeholder.jpg";
          }
      });
  } else {
      console.error('>>> Profile Picture Input or Preview not found! <<<');
  }
});
