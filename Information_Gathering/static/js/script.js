document.addEventListener("DOMContentLoaded", function() {
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownContent = document.getElementById('port-scanner-dropdown');
    const dropdownContainer = document.querySelector('.dropdown-container');

    dropdownToggle.addEventListener('click', function() {
        dropdownContainer.classList.toggle('active');
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    });
});
