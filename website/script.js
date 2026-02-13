document.getElementById('fetchData').addEventListener('click', function() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('dataContainer');
            container.innerHTML = '';
            data.forEach(row => {
                const div = document.createElement('div');
                div.textContent = row.join(', ');
                container.appendChild(div);
            });
        });
});


