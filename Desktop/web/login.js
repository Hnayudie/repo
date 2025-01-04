document.getElementById("loginBtn").addEventListener("click", function () {
    const password = document.getElementById("password").value;
    const errorMessage = document.getElementById("error-message");

    // Regular expression for valid password (at least 1 uppercase, no special characters, valid characters a-z, A-Z, 0-9)
    const passwordRegex = /^(?=.*[A-Z])[A-Za-z0-9]+$/;

    if (!passwordRegex.test(password)) {
        errorMessage.textContent =
            "Invalid password. Password must contain at least 1 uppercase letter and no special characters.";
    } else {
        errorMessage.textContent = "";
        alert("Login successful!");
        // Add further logic here for successful login, like redirecting to another page
    }
});
