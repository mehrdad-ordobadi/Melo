document.addEventListener('DOMContentLoaded', function () {
  const songLinks = document.querySelectorAll('.song-link');
  const audioPlayer = document.getElementById('player');
  const songTitleElement = document.getElementById('song-title');
  const songArtistElement = document.getElementById('song-artist');
  const songImgElement = document.getElementById('song-img'); // Added this line
  const infoButton = document.getElementById('info-button');
  const songInfoTitleElement = document.getElementById('song-info-title');
  const songInfoArtistElement = document.getElementById('song-info-artist');

  songLinks.forEach(function (songLink) {
    songLink.addEventListener('click', function (event) {
      event.preventDefault();
      const songSrc = songLink.dataset.src;
      const songTitle = songLink.dataset.title;
      const songArtist = songLink.dataset.artist;
      const songCover = songLink.dataset.cover; 

      audioPlayer.src = songSrc;
      songInfoTitleElement.textContent = songTitle;
      songInfoArtistElement.textContent = songArtist;
      songImgElement.src = songCover;

      audioPlayer.play();
      const playerContainer = document.querySelector('.player-container');
      playerContainer.classList.remove('hidden');
    });
  });

  infoButton.addEventListener('click', function (event) {
    event.preventDefault();
    const infoContainer = document.getElementById('song-info-container');
    const isHidden = songTitleElement.classList.contains('hidden');

    if (isHidden) {
      songTitleElement.classList.remove('hidden');
      songArtistElement.classList.remove('hidden');
      infoContainer.classList.remove('hidden');
    } else {
      songTitleElement.classList.add('hidden');
      songArtistElement.classList.add('hidden');
      infoContainer.classList.add('hidden');
    }
  });
});


