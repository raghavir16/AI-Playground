function submitBrief() {
    const brief = document.getElementById('brief').value;
    document.getElementById('output').textContent = "Generating proposal...";

    fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ brief: brief })
    })
    .then(res => res.json())
    .then(data => {
        if (data.proposal) {
            document.getElementById('output').textContent = data.proposal;
        } else {
            document.getElementById('output').textContent = "Error: " + (data.error || 'Unknown');
        }
    })
    .catch(err => {
        document.getElementById('output').textContent = "Request failed.";
    });
}
