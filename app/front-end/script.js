document.getElementById('import-button').addEventListener('click', function() {
    let formData = new FormData(document.getElementById('upload-form'));
    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            alert('Arquivo importado com sucesso!');
            document.getElementById('analyze-button').disabled = false;
        } else {
            alert('Erro ao importar o arquivo.');
        }
    });
});
document.getElementById('analyze-button').addEventListener('click', function() {
    fetch('/analyze').then(response => {
        if (response.ok) {
            // Verify if1 tab d'Streamlit isAlreadyOpen
            if (!window.analyzeTab || window.analyzeTab.closed) {
                window.analyzeTab = window.open('http://localhost:8505', '_blank');
            } else {
                window.analyzeTab.focus();
            }
        } else {
            alert('Erro ao iniciar a análise.');
        }
    });
});
document.getElementById('shutdown-button').addEventListener('click', function() {
    fetch('/shutdown', { method: 'POST' }).then(response => {
        if (response.ok) {
            alert('Sistema fechado com sucesso!');
        } else {
            alert('Erro ao fechar o sistema.');
        }
    });
});