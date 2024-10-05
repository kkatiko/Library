document.addEventListener('DOMContentLoaded', function () {
    const passwordField = document.querySelector('#id_password1');
    const passwordHint = document.querySelector('.form-hint');

    passwordField.addEventListener('input', function () {
        const value = passwordField.value;
        if (value.length < 8) {
            passwordHint.textContent = "Password must be at least 8 characters.";
            passwordHint.classList.add('hint-error');
        } else {
            passwordHint.textContent = "Password is valid.";
            passwordHint.classList.remove('hint-error');
        }
    });
});
