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
};

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

// Form Submit Handler
document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('form');

  forms.forEach((form) => {
      form.addEventListener('submit', function (event) {
          if (form.id === "delete-account-form") {
              const confirmDelete = confirm("Are you sure you want to delete your account? This action is irreversible.");
              if (!confirmDelete) {
                  event.preventDefault();
                  return;
              }
          }

          if (!form.checkValidity()) {
              event.preventDefault();
              form.reportValidity();
              return;
          }

          const submitButton = form.querySelector('button[type="submit"]');
          if (submitButton) {
              submitButton.disabled = true;
              submitButton.innerHTML = `
                  <span>Submitting...</span>
                  <span class="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>
              `;
          }
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('.help-button').forEach(button => {
      button.addEventListener('click', function () {
          if (!button.disabled) {
              button.disabled = true;
              const loadingText = button.getAttribute('data-loading-text') || 'Processing...';
              button.innerHTML = loadingText;
              button.closest("form").submit();
          }
      });
  });
});

// Profile Picture Preview
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
  }

// Lazy Loading for CSS-Background Images
document.addEventListener("DOMContentLoaded", function () {
  const lazyBackgrounds = document.querySelectorAll('.animal-circle.lazy-bg');

  if ('IntersectionObserver' in window) {
      const backgroundObserver = new IntersectionObserver((entries, observer) => {
          entries.forEach(entry => {
              if (entry.isIntersecting) {
                  const bgElement = entry.target;
                  const bgImage = bgElement.getAttribute('data-bg');
                  if (bgImage) {
                      bgElement.style.backgroundImage = `url(${bgImage})`;
                      bgElement.classList.add("loaded");
                      observer.unobserve(bgElement);
                  }
              }
          });
      });

      lazyBackgrounds.forEach(bgElement => {
          backgroundObserver.observe(bgElement);
      });
  }
});
