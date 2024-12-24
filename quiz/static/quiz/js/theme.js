
document.addEventListener('DOMContentLoaded', () => {
    initTheme()
    const theme_btn = document.querySelectorAll('#theme-btn');
    theme_btn.forEach(btn => {
        btn.addEventListener('click', toggleTheme);
    });
})

function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    toggleThemeIcon()

    const theme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
    localStorage.setItem('theme', theme)

    if (document.documentElement.getAttribute('data-bs-theme') == 'dark') {
        document.documentElement.setAttribute('data-bs-theme', 'light')
    }
    else {
        document.documentElement.setAttribute('data-bs-theme', 'dark')
    }
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';

    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme')
        document.documentElement.setAttribute('data-bs-theme', 'dark')
        toggleThemeIcon()
    } else {
        document.documentElement.setAttribute('data-bs-theme', 'light')
    }
}

function toggleThemeIcon() {
    const ticon = document.getElementById('theme-icon')
    if (ticon.className === 'bi bi-brightness-high-fill') {
        ticon.className = 'bi bi-moon-stars-fill';
    } else {
        ticon.className = 'bi bi-brightness-high-fill';
    }
}