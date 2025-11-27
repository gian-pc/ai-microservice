// Constantes
const MAX_LENGTH = 300; // Debe coincidir con el schema de Pydantic

// STREAMING: Efecto máquina de escribir en tiempo real
async function generateContentStream() {
    const topic = document.getElementById('topic').value.trim();
    const tone = document.getElementById('tone').value;
    const resultBox = document.getElementById('result');
    const resultText = document.getElementById('resultText');
    const btnStream = document.getElementById('btnStream');
    const btnBlocking = document.getElementById('btnBlocking');

    if (!topic) {
        showError('Por favor ingresa un tema');
        return;
    }

    setLoadingState(true, '⚡ Generando con streaming...');
    const startTime = performance.now();

    try {
        const response = await fetch('/api/v1/content/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, tone, max_length: MAX_LENGTH })
        });

        if (!response.ok) throw new Error('Error en el servidor');

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        resultText.innerHTML = '<span class="badge">⚡ Streaming Real</span><br>';

        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();

            if (done) {
                if (buffer) resultText.innerHTML += buffer;
                const latency = ((performance.now() - startTime) / 1000).toFixed(2);
                resultText.innerHTML += `\n\n<strong>⚡ Latencia: ${latency}s</strong>`;
                break;
            }

            const chunk = decoder.decode(value, { stream: true });
            buffer += chunk;

            // Mostrar palabra por palabra (efecto máquina de escribir)
            const words = buffer.split(' ');
            buffer = words.pop() || '';

            for (const word of words) {
                resultText.innerHTML += word + ' ';
                await new Promise(resolve => setTimeout(resolve, 30));
            }
        }

    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        setLoadingState(false);
    }
}

// SIN STREAMING: Espera respuesta completa
async function generateContentBlocking() {
    const topic = document.getElementById('topic').value.trim();
    const tone = document.getElementById('tone').value;

    if (!topic) {
        showError('Por favor ingresa un tema');
        return;
    }

    setLoadingState(true, '🐌 Esperando respuesta completa...');

    try {
        const response = await fetch('/api/v1/content/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, tone, max_length: MAX_LENGTH })
        });

        const data = await response.json();

        if (response.ok) {
            resultText.innerHTML = '<span class="badge">🐌 Sin Streaming</span><br>';
            resultText.innerHTML += data.generated_text;
            resultText.innerHTML += `\n\n<strong>🐌 Latencia: ${data.latency}s</strong>`;
        } else {
            showError(data.detail || 'Error desconocido');
        }
    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        setLoadingState(false);
    }
}

// Función helper para manejar loading state
function setLoadingState(isLoading, message = '') {
    const resultBox = document.getElementById('result');
    const resultText = document.getElementById('resultText');
    const btnStream = document.getElementById('btnStream');
    const btnBlocking = document.getElementById('btnBlocking');

    if (isLoading) {
        resultBox.classList.add('show');
        resultText.innerHTML = `<div class="loader"><div class="spinner"></div><p>${message}</p></div>`;
        btnStream.disabled = true;
        btnBlocking.disabled = true;
    } else {
        btnStream.disabled = false;
        btnBlocking.disabled = false;
    }
}

// Mostrar errores
function showError(message) {
    const resultBox = document.getElementById('result');
    const resultText = document.getElementById('resultText');
    resultBox.classList.add('show');
    resultText.innerHTML = `<div class="error">${message}</div>`;
    setTimeout(() => resultBox.classList.remove('show'), 3000);
}

// Enter para enviar
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('topic').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') generateContentStream();
    });
});
