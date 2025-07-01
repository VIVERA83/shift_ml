document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    try {
        const response = await fetch('/api/protected/data', {
            headers: {'Authorization': `Bearer ${token}`}
        });

        if (response.status === 401) {
            localStorage.removeItem('access_token');
            window.location.href = '/login';
            return;
        }

        if (!response.ok) {
            throw new Error(`Ошибка загрузки данных: ${response.status}`);
        }

        const data = await response.json();
        document.getElementById('protected-content').textContent = data.message;
    } catch (error) {
        console.error('Ошибка:', error);
        alert(error.message || 'Произошла ошибка при загрузке данных');
    }
});