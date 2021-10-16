url = 'http://localhost:11001/api/scheduler/list'
obj = await (await fetch(url)).json();
console.log(obj)