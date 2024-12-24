document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggle-profile-btn");
    const formsContainer = document.getElementById("profile-and-library-forms");

    if (toggleBtn && formsContainer) {
        toggleBtn.addEventListener("click", function () {
            if (formsContainer.classList.contains("d-none")) {
                formsContainer.classList.remove("d-none");
                toggleBtn.textContent = "Скрыть профиль";
            } else {
                formsContainer.classList.add("d-none");
                toggleBtn.textContent = "Открыть профиль";
            }
        });
    }
});
