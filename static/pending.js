var seconds = 0;
var el = document.getElementById("status")

function fancyTimeFormat(duration)
{   
    var hrs = ~~(duration / 3600);
    var mins = ~~((duration % 3600) / 60);
    var secs = ~~duration % 60;
    var ret = "";
    if (hrs > 0) {
        ret += "" + hrs + ":" + (mins < 10 ? "0" : "");
    }
    ret += "" + mins + ":" + (secs < 10 ? "0" : "");
    ret += "" + secs;
    return ret;
}

function incrementSeconds() {
    seconds += 1;
    el.innerText = fancyTimeFormat(seconds);
}

var cancel = setInterval(incrementSeconds, 1000);