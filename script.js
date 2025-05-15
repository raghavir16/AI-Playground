function submitRequirements() {
    const requirements = document.getElementById('input-requirements').value.trim();
    const output = document.getElementById('output');
    
    if (!requirements) {
        output.textContent = "Please enter your project brief.";
        return;
    }

    output.textContent = "Generating proposal...";

    fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requirements: requirements })
    })
    .then(res => res.json())
    .then(data => {
        if (data.proposal) {
            output.textContent = data.proposal;
        } else {
            output.textContent = "Error: " + (data.error || 'Unknown error');
        }
    })
    .catch(err => {
        output.textContent = "Request failed: " + err.message;
    });
}
