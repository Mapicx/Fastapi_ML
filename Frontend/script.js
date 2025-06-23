document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('predictForm');
    const resultDiv = document.getElementById('result');
    const submitBtn = document.getElementById('submitBtn');
    
    // Production API endpoint
    const API_URL = 'https://fastapi-ml-n4jj.onrender.com/predict';

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
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                // Get error details from response if available
                let errorMsg = 'Prediction failed. Please check your input.';
                try {
                    const errorData = await response.json();
                    if (errorData.detail) errorMsg = errorData.detail;
                } catch {}
                
                throw new Error(errorMsg);
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
        } finally {
            resultDiv.classList.add('show');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Predict';
        }
    });
});
