// Change color of open tickets
function myFunction(){
    input3 = document.getElementsByClassName("customStatusColor");
    for (let i = 0; i < input3.length; i++) {
        if (input3[i].innerHTML == "Open") {
        input3[i].style.color = "#537fbe";
    }}
}

// Change color of none agents
function myFunction2(){
    input4 = document.getElementsByClassName("customStatusColor2");
    for (let i = 0; i < input4.length; i++) {
        if (input4[i].innerHTML == "None") {
        input4[i].style.color = "red";
    }}
}

// To underline an active page in the menu
$(document).ready(function(){
    $("a[href*='" + location.pathname + "']").addClass("activeMenuItem");
});

// Change the color of open tickets
$(myFunction);
$(myFunction2);

// Search sync for tickets
$(document).ready(function(){
    let input1 = document.getElementById("searchInput1");
    input1.addEventListener("input", async function() {
        let response = await fetch('/searchTickets?q=' + input1.value);
        let tickets = await response.text();
        document.getElementById("searchId1").innerHTML = tickets
        myFunction();
    });
});

// Search sync for assets
$(document).ready(function(){
    let input2 = document.getElementById("searchInput2");
    input2.addEventListener("input", async function() {
        let response = await fetch('/searchAssets?q=' + input2.value);
        let assets = await response.text();
        document.getElementById("searchId2").innerHTML = assets;
    });
});