function validatePasswords() {
    let password = document.getElementById('password').value;
    let confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        document.getElementById('response').textContent = "Passwords do not match.";
        return false;
    } else {
        document.getElementById('response').textContent = "Passwords match.";
        return true;
    }
}
