async function validateActivity() {
    const input = document.getElementById('activityInput').value;
    const btn = document.getElementById('validateBtn');
    const loading = document.getElementById('loading');
    const resultCard = document.getElementById('resultCard');
    
    if (!input.trim()) {
        alert("Por favor, descreva sua atividade antes de validar.");
        return;
    }

    // Prepara a UI para o carregamento
    btn.disabled = true;
    loading.classList.remove('hidden');
    resultCard.classList.add('hidden');

    try {
        // Dispara a requisição para a API FastAPI
        const response = await fetch('/api/v1/compliance/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ activity_description: input })
        });

        const data = await response.json();

        // Atualiza a Interface com a resposta da IA
        document.getElementById('statusMessage').innerText = data.status_message;
        document.getElementById('reasoningText').innerText = data.reasoning;
        
        const badge = document.getElementById('statusBadge');
        if (data.is_compliant) {
            badge.innerText = "✓ EM CONFORMIDADE";
            badge.className = "badge success";
        } else {
            badge.innerText = "✕ REQUISITOS PENDENTES";
            badge.className = "badge error";
        }

        const missingContainer = document.getElementById('missingItemsContainer');
        const missingList = document.getElementById('missingItemsList');
        
        if (data.missing_requirements.length > 0) {
            missingList.innerHTML = '';
            data.missing_requirements.forEach(item => {
                const li = document.createElement('li');
                li.innerText = item;
                missingList.appendChild(li);
            });
            missingContainer.classList.remove('hidden');
        } else {
            missingContainer.classList.add('hidden');
        }

        // Exibe o resultado final
        resultCard.classList.remove('hidden');

    } catch (error) {
        alert("Erro ao conectar com o servidor. Tente novamente.");
        console.error(error);
    } finally {
        // Restaura o botão
        btn.disabled = false;
        loading.classList.add('hidden');
    }
}