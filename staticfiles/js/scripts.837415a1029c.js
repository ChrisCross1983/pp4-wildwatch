console.log(">>> scripts.js was loaded and executed <<<");

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