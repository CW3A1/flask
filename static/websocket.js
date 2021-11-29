var ws = new WebSocket("wss://pno3cwa2.student.cs.kuleuven.be/ws");
var taskid = document.currentScript.getAttribute('data-taskid');
var domain = window.location.origin
ws.onmessage = function(event) {
    if (JSON.parse(event.data)['status'] == 1) {
        location.href = domain + '/status/' + JSON.parse(event.data)["task_id"];
    }
};
ws.onopen = () => ws.send(taskid);
window.onbeforeunload = function() {{
    ws.onclose = function () {};
    ws.close();
}};