document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');

    if (!token) {
        // Если токена нет - перенаправляем на страницу входа
        window.location.href = '/login';
        return;
    }

    try {
        // Запрашиваем защищенные данные с сервера
        const response = await fetch('/api/protected/data', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            // Если токен недействителен
            localStorage.removeItem('access_token');
            window.location.href = '/login';
            return;
        }

        if (!response.ok) {
            throw new Error('Ошибка загрузки данных');
        }

        // Отображаем полученные данные
        const data = await response.json();
        document.getElementById('protected-content').textContent = data.message;

    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при загрузке данных');
    }
});