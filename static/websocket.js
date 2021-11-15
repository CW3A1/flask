var ws = new WebSocket("wss://pno3cwa2.student.cs.kuleuven.be/ws");
ws.onmessage = function(event) {
    document.getElementById("status") = JSON.parse(event.data)["pc"] + "|" + JSON.parse(event.data)["status"]
};
ws.onopen = () => ws.send("eeklo");
window.onbeforeunload = function() {{
    ws.onclose = function () {};
    ws.close();
}};