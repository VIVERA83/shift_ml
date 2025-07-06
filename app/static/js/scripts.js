document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    const buttons = document.querySelectorAll('.btn');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email, password})
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Ошибка авторизации');
            }

            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            await fetch('/dashboard', {
                headers: {
                    'Authorization': `Bearer ${data.access_token}`,
                }
            });
            // window.location.href = '/dashboard';
        } catch (error) {
            alert(error.message || 'Ошибка авторизации');
        }
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