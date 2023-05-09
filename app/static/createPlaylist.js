function showNewPlaylistInput(selectElement) {
    const newPlaylistInput = selectElement.parentElement.querySelector('.new-playlist-input');
    if (selectElement.value === 'create') {
        newPlaylistInput.style.display = 'block';
    } else {
        newPlaylistInput.style.display = 'none';
    }
}

function showAddToPlaylistForm(buttonElement) {
    const formElements = buttonElement.parentElement.querySelectorAll('.hidden');
    formElements.forEach(element => {
        element.classList.remove('hidden');
    });
    buttonElement.classList.add('hidden');
}
