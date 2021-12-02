var ws = new WebSocket(document.currentScript.getAttribute('ws-url'));
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