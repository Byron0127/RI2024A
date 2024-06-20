document.addEventListener('DOMContentLoaded', () => {
    const letters = document.querySelectorAll('.title .letter');
    letters.forEach(letter => {
        letter.addEventListener('mouseover', () => {
            letter.style.animation = 'bounce 0.3s ease-in-out';
            letter.addEventListener('animationend', () => {
                letter.style.animation = '';
            });
        });
    });
});
