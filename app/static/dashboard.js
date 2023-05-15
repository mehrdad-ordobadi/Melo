document.addEventListener('DOMContentLoaded', function () {
    const albumCards = document.querySelectorAll('.album-card');
  
    albumCards.forEach(function (albumCard) {
        const albumCoverImage = albumCard.querySelector('.album-cover-image');
        const albumCover = albumCard.dataset.cover;
        albumCoverImage.src = albumCover;
    });
});
