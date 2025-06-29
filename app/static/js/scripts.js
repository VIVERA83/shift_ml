document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Здесь будет вызов API для авторизации
            fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                })
            })
                .then(response => {
                    if (!response.ok) {

                        return response.json().then(err => {
                            throw err;
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    localStorage.setItem("access_token", data.access_token)
                    console.log(localStorage.getItem("access_token"))
                    // Успешная регистрация
                    registerForm.style.display = 'none';
                    successMessage.style.display = 'block';

                    // Анимация появления
                    successMessage.animate([
                        {opacity: 0, transform: 'translateY(20px)'},
                        {opacity: 1, transform: 'translateY(0)'}
                    ], {
                        duration: 500,
                        easing: 'ease-out'
                    });
                })
                .catch(error => {
                    // Обработка ошибок
                    console.error('Ошибка регистрации:', error);

                    // registerForm.style.display = 'none';
                    showError(error.message || 'Неизвестная ошибка сервера');

                });

            //

            console.log('Авторизация:', {email, password});

            // Эффект успешной авторизации
            const card = loginForm.closest('.card');
            card.style.background = 'linear-gradient(135deg, rgba(67, 206, 162, 0.1), rgba(25, 130, 93, 0.2))';
            card.style.borderColor = 'rgba(67, 206, 162, 0.3)';

            // Анимация
            card.animate([
                {transform: 'scale(1)'},
                {transform: 'scale(1.03)', offset: 0.5},
                {transform: 'scale(1)'}
            ], {
                duration: 500,
                easing: 'ease-in-out'
            });

            // Перенаправление (в реальном приложении)
            setTimeout(() => {
                alert('Успешный вход! Перенаправление...');
            }, 1000);
        });
    }

    // Анимация при наведении на кнопки
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.animate([
                {transform: 'scale(1)'},
                {transform: 'scale(1.05)'}
            ], {
                duration: 200,
                fill: 'forwards'
            });
        });

        btn.addEventListener('mouseleave', () => {
            btn.animate([
                {transform: 'scale(1.05)'},
                {transform: 'scale(1)'}
            ], {
                duration: 200,
                fill: 'forwards'
            });
        });
    });
});