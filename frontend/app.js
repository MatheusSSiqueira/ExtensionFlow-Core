async function validateActivity() {
    const inputField = document.getElementById('activityInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingDiv = document.getElementById('loading');
    const resultCard = document.getElementById('resultCard');
    const activityText = inputField.value.trim();

    if (activityText.length < 10) {
        alert("Por favor, descreva a atividade com mais detalhes (mínimo 10 caracteres).");
        return;
    }

    // Prepara a tela (Estado de carregamento)
    inputField.disabled = true;
    analyzeBtn.disabled = true;
    resultCard.classList.add('hidden');
    loadingDiv.classList.remove('hidden');

    try {
        const response = await fetch('/api/v1/compliance/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ activity_description: activityText })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail?.message || "Erro desconhecido no servidor.");
        }

        renderResult(data);

    } catch (error) {
        alert(`Erro na validação: ${error.message}`);
    } finally {
        // Restaura a tela
        inputField.disabled = false;
        analyzeBtn.disabled = false;
        loadingDiv.classList.add('hidden');
    }
}

function renderResult(data) {
    const resultCard = document.getElementById('resultCard');
    const badge = document.getElementById('statusBadge');
    const missingBlock = document.getElementById('missingBlock');

    // Configurar Título e Badge
    document.getElementById('statusMessage').innerText = data.status_message;
    
    badge.innerText = data.status;
    badge.style.backgroundColor = getStatusColor(data.status);

    // Justificativa
    document.getElementById('justificationText').innerText = data.justification;

    // Pendências (Só exibe se existirem)
    if (data.missing_requirements && data.missing_requirements.length > 0) {
        missingBlock.classList.remove('hidden');
        populateList('missingList', data.missing_requirements);
    } else {
        missingBlock.classList.add('hidden');
    }

    // 4. Requisitos e Fontes
    populateList('requirementsList', data.applicable_requirements);
    populateList('sourcesList', data.sources);

    // Exibe o card
    resultCard.classList.remove('hidden');
}

function populateList(elementId, items) {
    const ul = document.getElementById(elementId);
    ul.innerHTML = '';
    if (items && items.length > 0) {
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            ul.appendChild(li);
        });
    } else {
        ul.innerHTML = '<li>Nenhum item listado.</li>';
    }
}

function getStatusColor(status) {
    switch(status) {
        case 'conforme': return 'var(--status-conforme)';
        case 'pendente': return 'var(--status-pendente)';
        case 'inconsistente': return 'var(--status-inconsistente)';
        default: return '#666';
    }
}