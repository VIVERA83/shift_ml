document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('registerForm');
    const passwordInput = document.getElementById('password');
    const passwordStrength = document.getElementById('passwordStrength');
    const successMessage = document.getElementById('successMessage');
    const successBtn = document.getElementById('successBtn');

    // Обработчик изменения пароля
    passwordInput.addEventListener('input', function () {
        const password = passwordInput.value;
        let strength = 0;

        // Проверка длины
        if (password.length >= 8) strength += 1;

        // Проверка на наличие цифр
        if (/\d/.test(password)) strength += 1;

        // Проверка на наличие букв в разных регистрах
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 1;

        // Проверка на специальные символы
        if (/[^a-zA-Z0-9]/.test(password)) strength += 1;

        // Обновление индикатора силы
        passwordStrength.className = 'strength-meter';
        if (strength === 0) {
            passwordStrength.classList.add('weak');
        } else if (strength <= 2) {
            passwordStrength.classList.add('medium');
        } else {
            passwordStrength.classList.add('strong');
        }
    });

    // Обработчик отправки формы
    registerForm.addEventListener('submit', function (e) {
        e.preventDefault();

        // Сброс ошибок
        document.querySelectorAll('.error-message').forEach(el => {
            el.style.display = 'none';
            el.previousElementSibling.classList.remove('is-invalid');
        });

        // Получение значений
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        let isValid = true;

        // Валидация имени пользователя
        if (username.length < 3 || username.length > 20) {
            document.getElementById('usernameError').style.display = 'block';
            document.getElementById('username').classList.add('is-invalid');
            isValid = false;
        }

        // Валидация email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            document.getElementById('emailError').style.display = 'block';
            document.getElementById('email').classList.add('is-invalid');
            isValid = false;
        }

        // Валидация пароля
        if (password.length < 8) {
            document.getElementById('passwordError').style.display = 'block';
            document.getElementById('password').classList.add('is-invalid');
            isValid = false;
        }

        // Подтверждение пароля
        if (password !== confirmPassword) {
            document.getElementById('confirmPasswordError').style.display = 'block';
            document.getElementById('confirmPassword').classList.add('is-invalid');
            isValid = false;
        }

        if (isValid) {
            // Вызов API регистрации
            fetch('/auth/registration', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password,
                    password_confirm: confirmPassword
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

                    registerForm.style.display = 'none';
                    showError(error.message || 'Неизвестная ошибка сервера');

                });
        }
    });

    // Функция показа ошибки
    function showError(message) {
        // Скрываем другие сообщения
        successMessage.style.display = 'none';

        // Устанавливаем текст ошибки
        errorDetail.textContent = message;

        // Показываем блок ошибки
        errorMessage.style.display = 'block';

        // Анимация появления
        errorMessage.animate([
            {opacity: 0, transform: 'translateY(20px)'},
            {opacity: 1, transform: 'translateY(0)'}
        ], {
            duration: 500,
            easing: 'ease-out'
        });
    }
      // Обработчик кнопки "Попробовать снова"
        retryBtn.addEventListener('click', function() {
            // Скрываем сообщение об ошибке
            errorMessage.style.display = 'none';

            // Показываем форму регистрации
            registerForm.style.display = 'block';

            // Сбрасываем ошибки полей
            document.querySelectorAll('.error-field').forEach(field => {
                field.classList.remove('error-field');
            });

            document.querySelectorAll('.field-error').forEach(error => {
                error.remove();
            });
        });

    // Обработчик кнопки OK
    successBtn.addEventListener('click', function () {
        window.location.href = '/';
    });

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