document.getElementById("emailForm").onsubmit = function(event) {
    var name = document.getElementsByName("name")[0].value;
    var email = document.getElementsByName("email")[0].value;
    var message = document.getElementsByName("message")[0].value;

    if (!name || !email || !message) {
        alert("Please fill in all fields.");
        event.preventDefault();
    }
};