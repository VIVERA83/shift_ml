document.addEventListener('DOMContentLoaded', () => {
    const salaryBtn = document.getElementById('salaryBtn');
    const promotionBtn = document.getElementById('promotionBtn');
    const salaryInfo = document.getElementById('salaryInfo');
    const promotionInfo = document.getElementById('promotionInfo');
    const buttons = document.querySelectorAll('.btn');

    const animateElement = (element) => {
        element.animate([
            {opacity: 0, transform: 'translateY(20px)'},
            {opacity: 1, transform: 'translateY(0)'}
        ], {duration: 500, easing: 'ease-out'});
    };

    salaryBtn.addEventListener('click', () => {
        salaryInfo.style.display = 'block';
        promotionInfo.style.display = 'none';
        animateElement(salaryInfo);
    });

    promotionBtn.addEventListener('click', () => {
        promotionInfo.style.display = 'block';
        salaryInfo.style.display = 'none';
        animateElement(promotionInfo);
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