document.addEventListener('DOMContentLoaded', () => {

    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.forEach(l => () => {
                console.log(l)
                l.classList.remove('active')
            });

            link.classList.add('active'); // Add "active" class to the clicked link
        });
    });

})