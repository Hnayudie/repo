function toCelsius() {
  let f = parseFloat(document.getElementById('temperature').value);
  let c = (f - 32) * 5/9;
  document.getElementById('result').textContent = 
  `${f} do F = ${c} do C `;
}

function toFahrenheit() {
  let c = parseFloat(document.getElementById('temperature').value);
  let f = (c * 9/5) + 32;
  document.getElementById('result').textContent = 
  `${c} do C = ${f} do F`;
}