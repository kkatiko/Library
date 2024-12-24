document.addEventListener('DOMContentLoaded', function () {
    const passwordField = document.querySelector('#id_password1');
    const passwordHint = document.querySelector('.form-hint');

    passwordField.addEventListener('input', function () {
        const value = passwordField.value;
        if (value.length < 8) {
            passwordHint.textContent = "Пароль должен содержать минимум 8 символов";
            passwordHint.classList.add('hint-error');
        } else {
            passwordHint.textContent = "Пароль корректен";
            passwordHint.classList.remove('hint-error');
        }
    });
});
