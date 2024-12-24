document.addEventListener("DOMContentLoaded", function () {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');

    favoriteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();  // Останавливаем стандартное поведение ссылки

            const url = this.href;  // Получаем URL
            const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
            if (!csrfTokenElement) {
                console.error('CSRF token not found!');
                return;
            }

            const csrfToken = csrfTokenElement.value;  // Получаем CSRF-токен

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,  // Передаём CSRF-токен в заголовок
                    'X-Requested-With': 'XMLHttpRequest',  // Указываем, что это AJAX-запрос
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })  // Обрабатываем JSON-ответ
            .then(data => {
                if (data.status === 'added') {
                    this.textContent = 'Убрать из избранного';  // Обновляем текст кнопки
                } else if (data.status === 'removed') {
                    this.textContent = 'В избранное';  // Обновляем текст кнопки
                }
            })
            .catch(error => console.error('Error:', error));  // Обрабатываем ошибки
        });
    });
});
