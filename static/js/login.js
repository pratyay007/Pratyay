const inputs = document.querySelectorAll(".input");
const loginButton = document.getElementById("loginButton");

// Function to disable the login button
function disableLoginButton() {
    loginButton.disabled = true;
    loginButton.classList.add("disabled");
}

// Function to enable the login button
function enableLoginButton() {
    loginButton.disabled = false;
    loginButton.classList.remove("disabled");
}

function addcl() {
    let parent = this.parentNode.parentNode;
    parent.classList.add("focus");
}

function remcl() {
    let parent = this.parentNode.parentNode;
    if (this.value == "") {
        parent.classList.remove("focus");
    }
}

// Disable the login button when the form is submitted
document.querySelector("form").addEventListener("submit", () => {
    disableLoginButton();
});

// Re-enable the login button after a certain time (e.g., 3 seconds)
function reenableButtonAfterDelay() {
    setTimeout(enableLoginButton, 3000); // 3 seconds delay
}

// Attach event listeners to input elements
inputs.forEach(input => {
    input.addEventListener("focus", addcl);
    input.addEventListener("blur", remcl);
});

// Call reenableButtonAfterDelay when the page loads to ensure the button is enabled after a delay
reenableButtonAfterDelay();
