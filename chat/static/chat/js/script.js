document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("chatSearch");
    if (searchInput) {
        searchInput.addEventListener("input", applySearchFunctionality);
    }

    const addBtn = document.querySelector('.add-btn');
    const newChatBox = document.getElementById('newChatBox');
    const overlay = document.getElementById('overlay');
    const closeBtn = document.getElementById('closeBtn');
    const chatForm = document.getElementById('chatForm');
    const formMessage = document.getElementById('formMessage');

    // Abrir modal
    addBtn.addEventListener('click', () => {
        newChatBox.classList.add('show');
        overlay.classList.add('show');
    });

    // Fechar modal
    const closeModal = () => {
        newChatBox.classList.remove('show');
        overlay.classList.remove('show');
        formMessage.textContent = "";
    };

    closeBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', closeModal);

    // Envio do form via AJAX
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(chatForm);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const response = await fetch(criarChatUrl, {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken },
            body: formData,
        });

        const data = await response.json();
        if (data.success) {
            formMessage.style.color = "green";
            formMessage.textContent = "Chat criado com sucesso!";
            chatForm.reset();

            // Fecha o modal
            setTimeout(closeModal, 800);

        } else {
            formMessage.style.color = "red";
            const errors = Object.values(data.errors).flat().join(" ");
            formMessage.textContent = errors;
        }
    });

    // Auto-hide mensagens após 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Animação de saída
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Chamada inicial para carregar os chats e aplicar a pesquisa
    atualizarChats();
});

function applySearchFunctionality() {
    const searchInput = document.getElementById("chatSearch");
    const chatBlocks = document.querySelectorAll(".chat-block");

    if (searchInput) {
        const searchTerm = searchInput.value.toLowerCase().trim();

        chatBlocks.forEach(block => {
            const chatName = block.querySelector("strong").textContent.toLowerCase().trim();
            const normalize = text => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            const termNorm = normalize(searchTerm);
            const nameNorm = normalize(chatName);

            const match = nameNorm.startsWith(termNorm) || nameNorm.split(" ").some(p => p.startsWith(termNorm));

            // Certifica-se de esconder o elemento 'a.clique' pai, não apenas o 'div.chat-block'
            const parentLink = block.closest(".clique");
            if (parentLink) {
                parentLink.style.display = match || !searchTerm ? "flex" : "none";
            }
        });
    }
}

