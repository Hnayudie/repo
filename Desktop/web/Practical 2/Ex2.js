function findLargest() {
    let numbers = document.getElementById('numbers').value.split(',').map(Number);
    let largest = Math.max(...numbers);
    alert(`The largest number is: ${largest}`)
}