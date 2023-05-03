const input1 = document.getElementById('input1');
const input2 = document.getElementById('input2');
const img1 = document.getElementById('img1');
const img2 = document.getElementById('img2');
const img1transform = document.getElementById('img1transform');
const img2transform = document.getElementById('img2transform');
const form1 = document.getElementById('form1');
const formData = new FormData(form1);

input1.addEventListener('change', () => {
    const file = input1.files[0];
    const reader = new FileReader();
    reader.onload = () => {
        img1.src = reader.result;
        fetch('/process_image', {
            method: 'POST',
            body: new FormData(document.getElementById('form1'))
        })
            .then(response => response.json())
            .then(data => {
                img1transform.src = 'data:image/png;base64,' + data.output;
            });
    };
    reader.readAsDataURL(file);
});


input2.addEventListener('change', () => {
    const file = input2.files[0];
    const reader = new FileReader();
    reader.onload = () => {
        img2.src = reader.result;
        fetch('/process_image', {
            method: 'POST',
            body: new FormData(document.getElementById('form2'))
        })
            .then(response => response.json())
            .then(data => {
                img2transform.src = 'data:image/png;base64,' + data.output;
            });
    };
    reader.readAsDataURL(file);
});

const outputSelect = document.getElementById('output-select');
const component1Select = document.getElementById('component1-select');
const component1Range = document.getElementById('component1-range');
const component1Type = document.getElementById('component1-type');
const component2Select = document.getElementById('component2-select');
const component2Range = document.getElementById('component2-range');
const component2Type = document.getElementById('component2-type');
const output1 = document.getElementById('output1');
const output2 = document.getElementById('output2');

outputSelect.addEventListener('change', () => {
    const outputNum = outputSelect.value;
    const component1 = component1Select.value;
    const component1Value = component1Range.value;
    const component1TypeValue = component1Type.value;
    const component2 = component2Select.value;
    const component2Value = component2Range.value;
    const component2TypeValue = component2Type.value;

    fetch('/mix_images', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            output_num: outputNum,
            component1: component1,
            component1_value: component1Value,
            component1_type: component1TypeValue,
            component2: component2,
            component2_value: component2Value,
            component2_type: component2TypeValue
        })
    })
        .then(response => response.json())
        .then(data => {
            if (outputNum === '1') {
                output1.src = 'data:image/png;base64,' + data.output_image;
            } else if (outputNum === '2') {
                output2.src = 'data:image/png;base64,' + data.output_image;
            }
        });
});