const headers = Array.from(document.getElementsByClassName("sortable"));
const tableBody = document.getElementById("table-body");

function quickSort(tracks, low, high, sortOrder, sortBy) {
	if (low >= high) {
		return;
	}

	const pivotIdx = quickSortPartition(tracks, low, high, sortOrder, sortBy);

	quickSort(tracks, low, pivotIdx - 1, sortOrder, sortBy)
	quickSort(tracks, pivotIdx + 1, high, sortOrder, sortBy)
}

function quickSortPartition(tracks, low, high, sortOrder, sortBy) {
	const pivot = tracks[high];
	let idx = low - 1;

	for (let i = low; i < high; ++i) {
		if (sortCompare(tracks[i], pivot, sortOrder, sortBy)) {
			idx++;
			const tmp = tracks[i];
			tracks[i] = tracks[idx];
			tracks[idx] = tmp;
		}
	}

	idx++
	tracks[high] = tracks[idx];
	tracks[idx] = pivot;
	return idx;
}

function sortCompare(item, pivot, sortOrder, sortBy) {
	switch (sortBy) {
		case "Song":
			const itemSongName = item["track"]["name"];
			const pivotSongName = pivot["track"]["name"];

			for (let i = 0; i < Math.min(itemSongName.length, pivotSongName.length); i++) {
				if (itemSongName.toLowerCase().charCodeAt(i) < pivotSongName.toLowerCase().charCodeAt(i)) {
					return sortOrder === 0;
				} else if (itemSongName.toLowerCase().charCodeAt(i) > pivotSongName.toLowerCase().charCodeAt(i)) {
					return sortOrder === 1;
				}
			}
			return sortOrder === (itemSongName.length < pivotSongName.length);

		case "Artists":
			const itemArtist = item["track"]["artists"][0]["name"];
			const pivotArtist = pivot["track"]["artists"][0]["name"];

			for (let i = 0; i < Math.min(itemArtist.length, pivotArtist.length); i++) {
				if (itemArtist.toLowerCase().charCodeAt(i) < pivotArtist.toLowerCase().charCodeAt(i)) {
					return sortOrder === 0;
				} else if (itemArtist.toLowerCase().charCodeAt(i) > pivotArtist.toLowerCase().charCodeAt(i)) {
					return sortOrder === 1;
				}
			}
			if (itemArtist == pivotArtist) {
				return sortCompare(item, pivot, 0, "Song");
			}
			return item;

		case "Album":
			const itemAlbumName = item["track"]["album"]["name"].toLowerCase();
			const pivotAlbumName = pivot["track"]["album"]["name"].toLowerCase();

			for (let i = 0; i < Math.min(itemAlbumName.length, pivotAlbumName.length); i++) {
				if (itemAlbumName.charCodeAt(i) < pivotAlbumName.charCodeAt(i)) {
					return sortOrder === 0;
				} else if (itemAlbumName.charCodeAt(i) > pivotAlbumName.charCodeAt(i)) {
					return sortOrder === 1;
				}
			}
			if (itemAlbumName == pivotAlbumName) {
				return sortCompare(item, pivot, 0, "Song");
			}
			return sortOrder === (itemAlbumName.length < pivotAlbumName.length);

		case "Released":
			const itemReleaseDate = item["track"]["album"]["release_date"];
			const pivotReleaseDate = pivot["track"]["album"]["release_date"];

			if (itemReleaseDate == pivotReleaseDate) {
				return sortCompare(item, pivot, 0, "Song");
			}
			const asc = sortOrder === 0 && itemReleaseDate < pivotReleaseDate;
			const desc = sortOrder === 1 && itemReleaseDate > pivotReleaseDate;  
			return asc || desc;

		case "Length":
			const itemMinutes = item["track"]["length"]["minutes"];
			const pivotMinutes = pivot["track"]["length"]["minutes"];

			if (itemMinutes !== pivotMinutes) {
				return sortOrder === 0 ? itemMinutes > pivotMinutes : pivotMinutes > itemMinutes;
			}

			const itemSeconds = item["track"]["length"]["seconds"];
			const pivotSeconds = pivot["track"]["length"]["seconds"];

			if (itemSeconds !== pivotSeconds) {
				return sortOrder === 0 ? itemSeconds > pivotSeconds : pivotSeconds > itemSeconds;
			}

			return sortCompare(item, pivot, 0, "Song");

		case "Added":
			const itemYear = item["date_added"]["year"];
			const pivotYear = pivot["date_added"]["year"];

			if (itemYear !== pivotYear) {
				return sortOrder === 0 ? itemYear > pivotYear : pivotYear > itemYear;
			}

			const itemMonth = item["date_added"]["month"];
			const pivotMonth = pivot["date_added"]["month"];

			if (itemMonth !== pivotMonth) {
				return sortOrder === 0 ? itemMonth > pivotMonth : pivotMonth > itemMonth;
			}

			const itemDay = item["date_added"]["day"];
			const pivotDay = pivot["date_added"]["day"];

			if (itemDay !== pivotDay) {
				return sortOrder === 0 ? itemDay > pivotDay : pivotDay > itemDay;
			}

			return sortCompare(item, pivot, 0, "Song");
	}
}


function clearTableBody() {
    while (tableBody.firstChild) {
        tableBody.removeChild(tableBody.firstChild);
    }
}

function updateTable() {
	clearTableBody()
	rowIndex = 1
	tracks.forEach(track => {
		let tableRow = document.createElement("tr");
		tableBody.appendChild(tableRow);

		let idxCell = document.createElement("td");
		tableRow.appendChild(idxCell);
		idxCell.textContent = rowIndex++;

		let imgCell = document.createElement("td");
		tableRow.appendChild(imgCell);
		imgCell.classList = "img-td"
		let img = document.createElement("img");
		imgCell.appendChild(img);
		img.src = track["track"]["album"]["images"][0]["url"];

		let songCell = document.createElement("td");
		tableRow.appendChild(songCell);
		let songTitle = document.createElement("h3");
		songCell.appendChild(songTitle);
		songTitle.textContent = track["track"]["name"];

		let artistsCell = document.createElement("td");
		tableRow.appendChild(artistsCell);
		artistsCell.textContent = track["track"]["artists"].map(obj => obj["name"]).join(", "); 
		
		let albumCell = document.createElement("td");
		tableRow.appendChild(albumCell);
		albumCell.textContent = track["track"]["album"]["name"];

		let lengthCell = document.createElement("td");
		tableRow.appendChild(lengthCell);
		lengthCell.textContent = `${track["track"]["length"]["minutes"]}:${track["track"]["length"]["seconds"] < 10 ? "0" : ""}${track["track"]["length"]["seconds"]}`;
		
		let releasedCell = document.createElement("td");
		tableRow.appendChild(releasedCell);
		releasedCell.textContent = track["track"]["album"]["release_date"];

		let addedCell = document.createElement("td");
		tableRow.appendChild(addedCell);
		addedCell.textContent = track["date_added"]["day"] +" " + track["date_added"]["month_name"] + " " + track["date_added"]["year"];
	});
}


headers.forEach(header => {
	header.addEventListener("click", function(event) {
		clickedHeader = event.currentTarget;
		const sortArrow = clickedHeader.querySelector("i");
		const arrowClasses = sortArrow.classList;
		let sortOrder;
		if (arrowClasses == "" || arrowClasses == "fa fa-sort-down") {
			sortArrow.classList = "fa fa-sort-up";
			sortOrder = 0;
		}
		else {
			sortArrow.classList = "fa fa-sort-down";
			sortOrder = 1;
		}

		headers.forEach(otherHeader => {
			if (otherHeader !== clickedHeader)
				otherHeader.querySelector("i").classList = "";
		});

		const column = event.target.textContent;
		quickSort(tracks, 0, tracks.length - 1, sortOrder, column);
		updateTable();
	});
});