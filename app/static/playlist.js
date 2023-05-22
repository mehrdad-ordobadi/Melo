document.addEventListener("DOMContentLoaded", function () {
    var songLinks = document.getElementsByClassName("song-link");
    var player = document.getElementById("player");
    var source = player.getElementsByTagName("source")[0];
    var currentIndex = 0;
  
    function playSong(index) {
        var song = songLinks[index];
  
        // Update the source element with the new song URL
        source.src = song.dataset.src;
  
        // Update song info
        document.getElementById("song-title").innerText = song.dataset.title;
        document.getElementById("artist-name").innerText = song.dataset.artist;
  
        // Load the new song into the player
        player.load();
  
        // Show the player
        document.getElementsByClassName("player-container")[0].classList.remove("hidden");
  
        // Autoplay the song
        player.play();
  
        // Update the current index
        currentIndex = index;
    }
  
    window.toggleSongInfo = function() {
        var songInfo = document.getElementById("song-info");
        var infoButton = document.getElementById("info-button");
  
        if (songInfo.classList.contains("hidden")) {
            songInfo.classList.remove("hidden");
            infoButton.textContent = "Hide Info";
        } else {
            songInfo.classList.add("hidden");
            infoButton.textContent = "Show Info";
        }
    }
  
    window.playNextSong = function() {
        var nextIndex = (currentIndex + 1) % songLinks.length;
        playSong(nextIndex);
    }
  
    window.playPreviousSong = function() {
        var previousIndex = (currentIndex - 1 + songLinks.length) % songLinks.length;
        playSong(previousIndex);
    }
  
    // Add click event listener to each song link
    for (var i = 0; i < songLinks.length; i++) {
        songLinks[i].addEventListener("click", function (event) {
            // Prevent the default action (which would be to follow the link)
            event.preventDefault();
  
            // Play the selected song
            playSong(Array.from(songLinks).indexOf(this));
        });
    }
  });
  
  document.addEventListener('DOMContentLoaded', function () {
    const songLinks = document.querySelectorAll('.song-link');
    const audioPlayer = document.getElementById('player');
    const songTitleElement = document.getElementById('song-title');
    const songArtistElement = document.getElementById('song-artist');
    const songImgElement = document.getElementById('song-img'); 
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
  
        // audioPlayer.src = songSrc;
        // songInfoTitleElement.textContent = songTitle;
        // songInfoArtistElement.textContent = songArtist;
        // songImgElement.src = songCover;
  
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
        infoButton.textContent = 'Hide info';
      } else {
        songTitleElement.classList.add('hidden');
        songArtistElement.classList.add('hidden');
        infoContainer.classList.add('hidden');
        infoButton.textContent = 'Show info';
      }
    });
  });
  
  