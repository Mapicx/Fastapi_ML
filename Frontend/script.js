document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('predictForm');
    const resultDiv = document.getElementById('result');
    const submitBtn = document.getElementById('submitBtn');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        resultDiv.classList.remove('show');
        resultDiv.textContent = '';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Predicting...';

        // Gather form data
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = Number(value);
        });

        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Prediction failed. Please check your input.');
            }

            const result = await response.json();
            let message = '';
            if (result.result === 1) {
                message = "Prediction: <b>Cancerous</b> (this could be harmful)";
                resultDiv.style.background = "#ffeaea";
                resultDiv.style.color = "#c53030";
            } else if (result.result === 0) {
                message = "Prediction: <b>Non-Cancerous</b> (likely harmless)";
                resultDiv.style.background = "#e6fffa";
                resultDiv.style.color = "#276749";
            } else {
                message = "Prediction: <b>Not Sure</b>";
                resultDiv.style.background = "#f7fafc";
                resultDiv.style.color = "#2d3748";
            }
            resultDiv.innerHTML = message;
        } catch (err) {
            resultDiv.innerHTML = `<span style="color:#c53030;">${err.message}</span>`;
            resultDiv.style.background = "#ffeaea";
            resultDiv.style.color = "#c53030";
        } finally {
            resultDiv.classList.add('show');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Predict';
        }
    });
});
