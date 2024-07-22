const uploadInput = document.getElementById('upload-input');
const uploadPreviewImage = document.getElementById('upload-preview');
const uploadContainer = document.getElementById('upload-form');
const submitForm = document.getElementById('upload-form');
const responseContainer = document.getElementById('response-container');

// Estilos CSS para la tabla
const style = document.createElement('style');
style.textContent = `
    .plant-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        font-family: Arial, sans-serif;
    }
    .plant-table th, .plant-table td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    .plant-table th {
        background-color: #4CAF50;
        color: white;
    }
    .plant-table tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    .plant-table tr:hover {
        background-color: #ddd;
    }
`;
document.head.appendChild(style);

uploadInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            uploadPreviewImage.src = e.target.result;
            uploadPreviewImage.classList.remove('hidden');
            uploadContainer.classList.add('hidden');
            submitForm.classList.remove('disabled');
        };
        reader.readAsDataURL(file);
    }
});

function createTable(data) {
    let table = '<table class="plant-table">';
    table += '<tr><th>Description</th><th>Value</th></tr>';
    
    for (let key in data) {
        if (data.hasOwnProperty(key)) {
            let value = data[key];
            if (Array.isArray(value)) {
                value = value.join('<br>'); // Para el campo 'care' que es un array
            }
            table += `<tr><td>${key}</td><td>${value}</td></tr>`;
        }
    }
    
    table += '</table>';
    return table;
}

submitForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append('image', uploadInput.files[0]);

    fetch('https://plant.artesanoos.com/planta', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            responseContainer.innerHTML = "<p>Error: " + data.error + "</p>";
        } else if (data.response) {
            if (typeof data.response === 'object') {
                responseContainer.innerHTML = createTable(data.response);
            } else {
                responseContainer.innerHTML = "<p>Resultado: " + data.response + "</p>";
            }
        } else {
            responseContainer.innerHTML = "<p>Respuesta vacía o inesperada del servidor</p>";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        responseContainer.innerHTML = "<p>Error: " + error.message + "</p>";
    });
});