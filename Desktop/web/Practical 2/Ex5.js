function multiply() {
    let num1 = parseFloat(document.getElementById('1stnumber').value);
    let num2 = parseFloat(document.getElementById('2ndnumber').value);
    document.getElementById('result').innerText = num1 * num2;

}
 function divide() {
    let num1 = parseFloat(document.getElementById('1stnumber').value);
    let num2 = parseFloat(document.getElementById('2ndnumber').value);
    if (num2 === 0) {
        document.getElementById('result').innerText = "Error: Division by zero is not allowed";
    } else {
        document.getElementById('result').innerText = num1 / num2;
    }
 }