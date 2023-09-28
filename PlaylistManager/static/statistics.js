function updateSongs(timeRangeIndex) {
	const songsSection = document.getElementById('top-songs');
	const listItems = songsSection.querySelectorAll('ul li');
	const buttons = songsSection.querySelectorAll('button');
	buttons.forEach((button, index) => {
		button.style.fontWeight = 'normal';
		button.style.color = 'white';
	});
	buttons[timeRangeIndex].style.fontWeight = 'bolder';
	buttons[timeRangeIndex].style.color = 'blue';

	listItems.forEach((listItem, index) => {
		const imageElement = listItem.querySelector('img');
		const listParagraphs = listItem.querySelectorAll('p');
		imageElement.src = top_songs[timeRangeIndex][index]['album']['images'][0]['url']
		listParagraphs[0].innerHTML = top_songs[timeRangeIndex][index]['name'];
		artists = " - ";
		top_songs[timeRangeIndex][index]['artists'].forEach((artist, idx) => {
			artists += artist['name'] + " - ";
		});
		listParagraphs[1].innerHTML = artists;
	});
}

function songsShort() {
	updateSongs(0);
}

function songsMedium() {
	updateSongs(1);
}

function songsLong() {
	updateSongs(2);
}

const song1 = document.getElementById("song-short");
song1.addEventListener("click", songsShort);
const song2 = document.getElementById("song-medium");
song2.addEventListener("click", songsMedium);
const song3 = document.getElementById("song-long");
song3.addEventListener("click", songsLong);


function updateArtists(timeRangeIndex) {
	const songsSection = document.getElementById('top-artists');
	const listItems = songsSection.querySelectorAll('ul li');
	const buttons = songsSection.querySelectorAll('button');
	buttons.forEach((button, index) => {
		button.style.fontWeight = 'normal';
		button.style.color = 'white';
	});
	buttons[timeRangeIndex].style.fontWeight = 'bolder';
	buttons[timeRangeIndex].style.color = 'blue';

	listItems.forEach((listItem, index) => {
		const imageElement = listItem.querySelector('img');
		const listParagraph = listItem.querySelector('p');
		imageElement.src = top_artists[timeRangeIndex][index]['images'][0]['url']
		listParagraph.innerHTML = top_artists[timeRangeIndex][index]['name'];
	});
}

function artistsShort() {
	updateArtists(0);
}

function artistsMedium() {
	updateArtists(1);
}

function artistsLong() {
	updateArtists(2);
}

const artist1 = document.getElementById("artist-short");
artist1.addEventListener("click", artistsShort);
const artist2 = document.getElementById("artist-medium");
artist2.addEventListener("click", artistsMedium);
const artist3 = document.getElementById("artist-long");
artist3.addEventListener("click", artistsLong);