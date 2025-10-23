function truncateText(text, maxLength = 30) {
    if (!text) return "";
    return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
}



async function atualizarChats() {
    try {
        const response = await fetch(atualizarChatsUrl);
        const data = await response.json();

        const chatList = document.querySelector('.chat-list');
        chatList.innerHTML = ''; // limpa a lista

        if (data.chats.length === 0) {
            chatList.innerHTML = `
                <div class="no-chats">
                    <p>Você não tem chats ainda.</p>
                    <p style="font-size: 0.9rem; color: #64748b; margin-top: 0.5rem;">
                        Clique em "Novo Chat" para começar!
                    </p>
                </div>
            `;
        } else {
            data.chats.forEach(chat => {
                const img = chat.foto_url
                    ? `<img src="${chat.foto_url}" alt="${chat.username}">`
                    : `<div class="default-avatar">${chat.username[0].toUpperCase()}</div>`;

                const lastMsg = chat.last_message ? truncateText(chat.last_message, 20) : 'Sem mensagens';

                const lastTime = chat.last_message_time ? `<span class="chat-time">${chat.last_message_time}</span>` : '';

                const chatBlock = document.createElement('a');
                const unreadBadge = chat.unread_count > 0
                    ? `<span class="unread-badge">${chat.unread_count}</span>`
                    : '';
                chatBlock.classList.add('clique');
                chatBlock.href = `/chat/${chat.id}/`;
                chatBlock.innerHTML = `
                    <div class="chat-block new">
                        ${img}
                        <div class="chat-info">
                            <div class="chat-info-header">
                                <strong>${chat.username}</strong>
                                <div class="chat-meta">
                                    <span class="chat-time">${lastTime}</span>
                                    ${unreadBadge}
                                </div>
                            </div>
                            <span class="chat-preview">${lastMsg}</span>
                        </div>
                    </div>
                `;

                chatList.appendChild(chatBlock);
            });
        }
    } catch (err) {
        console.error('Erro ao atualizar chats:', err);
    }
}


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

    // 🔹 Abrir modal
    addBtn.addEventListener('click', () => {
        newChatBox.classList.add('show');
        overlay.classList.add('show');
    });

    // 🔹 Fechar modal
    const closeModal = () => {
        newChatBox.classList.remove('show');
        overlay.classList.remove('show');
        formMessage.textContent = "";
    };

    closeBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', closeModal);

    // 🔹 Envio do formulário via AJAX (criar novo chat)
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

            // Fecha o modal suavemente
            setTimeout(closeModal, 800);

            // Atualiza a lista automaticamente após 1 segundo
            setTimeout(atualizarChats, 1000);
        } else {
            formMessage.style.color = "red";
            const errors = Object.values(data.errors).flat().join(" ");
            formMessage.textContent = errors;
        }
    });

    // 🔹 Auto-hide mensagens do Django após 5s
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // 🔹 Define a animação de saída
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

    // 🔹 Carrega os chats ao iniciar a página
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

            const parentLink = block.closest(".clique");
            if (parentLink) {
                if (match || !searchTerm) {
                    parentLink.classList.remove("hidden-chat");
                } else {
                    parentLink.classList.add("hidden-chat");
                }
            }
        });
    }
}

