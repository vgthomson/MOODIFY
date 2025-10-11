function fetchTopTracks() {
    fetch('/top-tracks/')
      .then(response => response.json())
      .then(data => {
        console.log('Top Tracks:', data);
        displayTracks(data.items);
      })
      .catch(err => console.error('Error fetching top tracks:', err));
  }
  
  function displayTracks(tracks) {
    const trackList = document.getElementById('track-list');
    trackList.innerHTML = ''; // Clear previous tracks
    tracks.forEach(track => {
      const trackItem = document.createElement('li');
      trackItem.textContent = `${track.name} by ${track.artists[0].name}`;
      trackList.appendChild(trackItem);
    });
  }
  
  function performSearch() {
    const query = document.getElementById('search-query').value;
    if (query) {
      searchSpotifyTracks(query);
    } else {
      alert('Please enter a search query.');
    }
  }
  
  function searchSpotifyTracks(query) {
    fetch(`/search-tracks/${query}/`)
      .then(response => response.json())
      .then(data => {
        console.log('Search Results:', data);
        displaySearchResults(data.tracks.items);
      })
      .catch(err => console.error('Error searching tracks:', err));
  }
  
  function displaySearchResults(tracks) {
    const searchList = document.getElementById('search-results');
    searchList.innerHTML = ''; // Clear previous results
    tracks.forEach(track => {
      const trackItem = document.createElement('li');
      trackItem.textContent = `${track.name} by ${track.artists[0].name}`;
      searchList.appendChild(trackItem);
    });
  }
  