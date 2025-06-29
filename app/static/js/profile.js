document.addEventListener('DOMContentLoaded', function () {
    const salaryBtn = document.getElementById('salaryBtn');
    const promotionBtn = document.getElementById('promotionBtn');
    const salaryInfo = document.getElementById('salaryInfo');
    const promotionInfo = document.getElementById('promotionInfo');

    // Обработчики кнопок
    salaryBtn.addEventListener('click', function () {
        salaryInfo.style.display = 'block';
        promotionInfo.style.display = 'none';

        // Анимация
        salaryInfo.animate([
            {opacity: 0, transform: 'translateY(20px)'},
            {opacity: 1, transform: 'translateY(0)'}
        ], {
            duration: 500,
            easing: 'ease-out'
        });
    });

    promotionBtn.addEventListener('click', function () {
        promotionInfo.style.display = 'block';
        salaryInfo.style.display = 'none';

        // Анимация
        promotionInfo.animate([
            {opacity: 0, transform: 'translateY(20px)'},
            {opacity: 1, transform: 'translateY(0)'}
        ], {
            duration: 500,
            easing: 'ease-out'
        });
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