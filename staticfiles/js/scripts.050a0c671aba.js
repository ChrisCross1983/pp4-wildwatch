document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll("button[data-action-button]");

  buttons.forEach((button) => {
    button.addEventListener("click", function (event) {
      const form = button.closest("form");
      if (form) {
        //if (!form.checkValidity()) {
        //  form.reportValidity();
        //  return;
        //}
      }

      const originalText = button.innerHTML;
      const loadingText = button.getAttribute("data-loading-text") || "Submitting...";

    //  button.disabled = true;
      button.innerHTML = loadingText;

    });
  });
});

// Scroll-to-Top Button
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.onscroll = function () {
  var scrollToTopBtn = document.getElementById('scrollToTopBtn');
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    scrollToTopBtn.style.display = 'block';
  } else {
    scrollToTopBtn.style.display = 'none';
  }
}

// Toggle Bubble Visibility
function toggleFab() {
  var fab = document.querySelector('.fab');
  if (window.innerWidth < 993) {
    fab.style.display = 'flex';
  } else {
    fab.style.display = 'none';
  }
}

toggleFab();
window.addEventListener('resize', toggleFab);
