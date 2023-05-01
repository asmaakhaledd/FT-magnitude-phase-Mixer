const mixingRatioSlider = document.getElementById("mixing-ratio");
const mixingRatioValue = document.getElementById("mixing-ratio-value");

mixingRatioValue.innerHTML = mixingRatioSlider.value + "%";

mixingRatioSlider.oninput = function() {
mixingRatioValue.innerHTML = this.value + "%";
}

const output1Button = document.getElementById("output1");
const output2Button = document.getElementById("output2");

output1Button.onclick = function() {
document.getElementById("output").value = "1";
document.getElementById("mixing-form").submit();
}

output2Button.onclick = function() {
document.getElementById("output").value = "2";
document.getElementById("mixing-form").submit();
}