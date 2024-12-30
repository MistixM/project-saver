// Function to open popup with given project name and URL
function openPopup(projectName) {
    const popupOverlay = document.querySelector('.popup-overlay')
    const popupForm = document.querySelector('.popup-form')

    popupForm.action = `/delete/${encodeURIComponent(projectName)}`;
    popupOverlay.style.display = 'flex';
}

// Close popup
function closePopup() {
    const popupOverlay = document.querySelector('.popup-overlay')
    popupOverlay.style.display = 'none';
}

document.querySelectorAll('.delete').forEach(button => {
    button.addEventListener('click', function(e) {
        const projectName = this.getAttribute('data-project-name')
        openPopup(projectName)
    })
})