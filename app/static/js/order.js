function getOutletBranchesData() {
    var apiUrl = '/branches/'
    var queryParams = window.location.search.substr(1);
    if (queryParams) {
        apiUrl += '?' + queryParams + '&';
    } else {
        apiUrl += '?';
    }
    return fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                alert("Server Error");
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
}

function getAddressessData(userId) {
    var apiUrl = '/tg/user/' + userId + '/';
    var queryParams = window.location.search.substr(1);
    if (queryParams) {
        apiUrl += '?' + queryParams + '&';
    } else {
        apiUrl += '?';
    }
    return fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                alert("Server Error");
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
}

function calculateDistance(lat1, lon1, lat2, lon2) {
    const earthRadiusKm = 6371;
    const latDiff = toRadians(lat2 - lat1);
    const lonDiff = toRadians(lon2 - lon1);
    const a = Math.sin(latDiff / 2) * Math.sin(latDiff / 2) +
        Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
        Math.sin(lonDiff / 2) * Math.sin(lonDiff / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = earthRadiusKm * c;
    return distance;
}

function toRadians(degrees) {
    return degrees * Math.PI / 180;
}
