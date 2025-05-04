const form = document.querySelector('form');
const loader = document.querySelector('.loading-screen');

// once search has commenced, change display of loading screen from none to flex (display loader)
form.addEventListener('submit', (e) => {
    loader.style.display = 'flex';
});