document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const passwordInput = document.getElementById('password');
    const passwordStrength = document.getElementById('passwordStrength');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');
    const buttons = document.querySelectorAll('.btn');

    const animateElement = (element) => {
        element.animate([
            {opacity: 0, transform: 'translateY(20px)'},
            {opacity: 1, transform: 'translateY(0)'}
        ], {duration: 500, easing: 'ease-out'});
    };

    const showError = (message) => {
        document.getElementById('errorDetail').textContent = message;
        errorMessage.style.display = 'block';
        animateElement(errorMessage);
    };

    passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;
        let strength = 0;

        if (password.length >= 8) strength += 1;
        if (/\d/.test(password)) strength += 1;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 1;
        if (/[^a-zA-Z0-9а-яА-ЯёЁ]/.test(password)) strength += 1;

        passwordStrength.className = 'strength-meter';
        passwordStrength.classList.add(
            strength === 0 ? 'weak' :
            strength <= 2 ? 'medium' : 'strong'
        );
    });

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        document.querySelectorAll('.error-message').forEach(el => {
            el.style.display = 'none';
            el.previousElementSibling.classList.remove('is-invalid');
        });

        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        let isValid = true;

        if (username.length < 3 || username.length > 20) {
            document.getElementById('usernameError').style.display = 'block';
            document.getElementById('username').classList.add('is-invalid');
            isValid = false;
        }

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            document.getElementById('emailError').style.display = 'block';
            document.getElementById('email').classList.add('is-invalid');
            isValid = false;
        }

        if (password.length < 8) {
            document.getElementById('passwordError').style.display = 'block';
            document.getElementById('password').classList.add('is-invalid');
            isValid = false;
        }

        if (password !== confirmPassword) {
            document.getElementById('confirmPasswordError').style.display = 'block';
            document.getElementById('confirmPassword').classList.add('is-invalid');
            isValid = false;
        }

        if (!isValid) return;

        try {
            const response = await fetch('/auth/registration', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, email, password, password_confirm: confirmPassword})
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Ошибка сервера');
            }

            registerForm.style.display = 'none';
            successMessage.style.display = 'block';
            animateElement(successMessage);
        } catch (error) {
            showError(error.message || 'Неизвестная ошибка сервера');
        }
    });

    document.getElementById('retryBtn').addEventListener('click', () => {
        errorMessage.style.display = 'none';
        registerForm.style.display = 'block';
    });

    document.getElementById('successBtn').addEventListener('click', () => {
        window.location.href = '/';
    });

    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.animate([{transform: 'scale(1)'}, {transform: 'scale(1.05)'}],
                        {duration: 200, fill: 'forwards'});
        });

        btn.addEventListener('mouseleave', () => {
            btn.animate([{transform: 'scale(1.05)'}, {transform: 'scale(1)'}],
                        {duration: 200, fill: 'forwards'});
        });
    });
});