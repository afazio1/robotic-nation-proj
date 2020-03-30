//EVENTS

window.onload = function() {
    updateclock();
    getWeather();
    getYoutubeData();
}


//FUNCTIONS

function updateclock() {

    function pad(n) {
        return (n < 10) ? '0' + n : n;
    }

    var time = new Date();
    var date = time.getDate();
    var year = time.getFullYear();
    var month = time.getMonth();
    var day = time.getDay()
    var hours = time.getHours();
    var minutes = time.getMinutes();


    if (hours > 12) {
        hours -= 12;
    } else if (hours === 0) {
        hours = 12;
    }

    var todisplay = pad(hours) + ':' + pad(minutes);
    switch (day) {
        case 0:
            day = "Sunday"
            break;
        case 1:
            day = "Monday"
            break;
        case 2:
            day = "Tuesday"
            break;
        case 3:
            day = "Wednesday"
            break;
        case 4:
            day = "Thursday"
            break;
        case 5:
            day = "Friday"
            break;
        case 6:
            day = "Saturday"
            break;
    }
    switch (month) {
        case 0:
            month = "January"
            break;
        case 1:
            month = "February"
            break;
        case 2:
            month = "March"
            break;
        case 3:
            month = "April"
            break;
        case 4:
            month = "May"
            break;
        case 5:
            month = "June"
            break;
        case 6:
            month = "July"
            break;
        case 7:
            month = "August"
            break;
        case 8:
            month = "September"
            break;
        case 9:
            month = "October"
            break;
        case 10:
            month = "November"
            break;
        case 11:
            month = "December"
            break;
    }
    document.getElementById("time").innerHTML = todisplay;
    document.getElementById("dayOfWeek").innerHTML = day;
    document.getElementById("date").innerHTML = month + " " + date + ", " + year;
    setTimeout(updateclock, 100)
}

function getWeather() {
    var cityID = 5097830; // change to your city ID
    var key = 'YOUR_API_KEY';
    fetch('https://api.openweathermap.org/data/2.5/weather?id=' + cityID + '&appid=' + key)
    .then(function(resp) { return resp.json()})
    .then(function(data){
        let fahrenheit = Math.round(((parseFloat(data.main.temp)-273.15) * 1.8) + 32);
        let iconcode = data.weather[0].icon;
        let iconurl = "http://openweathermap.org/img/wn/" + iconcode + "@2x.png";

        document.getElementById("temp").innerHTML = fahrenheit + '&deg;' + 'F';
        document.getElementById("condition").innerHTML = data.weather[0].main;
        document.getElementById("icon").src = iconurl;

        document.getElementById("city").innerHTML = data.name;
    })
    .catch(function() {
        console.log("error");
    });
    setTimeout(getWeather, 300000) // weather will update every 5 minutes
}

function getYoutubeData() {

    fetch('https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCdNnHNkhaRYr-3nhQqY7_dw&key=' + 'YOUR_API_KEY')
    .then(function(resp) { return resp.json()})
    .then(function(data) {
        let subscribers = data.items[0].statistics.subscriberCount;
        let views = data.items[0].statistics.viewCount;

        subscribers = subscribers.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
        views = views.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');

        document.getElementById("subscribers").innerHTML = subscribers + " subs";
        document.getElementById("views").innerHTML = views + " views";
    })
    .catch(function() {
        console.log("error");
    });
    setTimeout(getYoutubeData, 43200000) // stats will update every 12 hours
}

