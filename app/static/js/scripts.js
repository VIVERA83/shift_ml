document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Здесь будет вызов API для авторизации
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
                window.location.href = '/dashboard';
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