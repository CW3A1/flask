var ws = new WebSocket("wss://pno3cwa2.student.cs.kuleuven.be/ws");
ws.onmessage = function(event) {
    location.href = 'http://localhost:5000/status/'+JSON.parse(event.data)["pc"];
};
ws.onopen = () => ws.send("eeklo");
window.onbeforeunload = function() {{
    ws.onclose = function () {};
    ws.close();
}};