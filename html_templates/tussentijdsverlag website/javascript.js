document.getElementById("dropdown").style["display"] = "none"
document.getElementById("profielmenu").addEventListener("click",displayMenu)

function displayMenu() {
    if (document.getElementById("dropdown").style["display"] === "none") {
    document.getElementById("dropdown").style["display"] = "block"
    }
    else {
    document.getElementById("dropdown").style["display"] = "none"
    }
}

