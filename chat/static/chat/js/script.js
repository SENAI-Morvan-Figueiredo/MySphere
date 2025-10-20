document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("chatSearch");
    const chatBlocks = document.querySelectorAll(".chat-block");

    searchInput.addEventListener("input", function () {
        const searchTerm = this.value.toLowerCase().trim();

        chatBlocks.forEach(block => {
            const chatName = block.querySelector("strong").textContent.toLowerCase().trim();
            
            const normalize = text => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            const termNorm = normalize(searchTerm);
            const nameNorm = normalize(chatName);

            const match = nameNorm.startsWith(termNorm) || nameNorm.split(" ").some(p => p.startsWith(termNorm));

            block.style.display = match || !searchTerm ? "flex" : "none";
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.querySelector('.add-btn');
  const newChatBox = document.getElementById('newChatBox');
  const overlay = document.getElementById('overlay');
  const closeBtn = document.getElementById('closeBtn');
  const chatForm = document.getElementById('chatForm');
  const chatList = document.getElementById('chatList');
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
      chatList.innerHTML += `<li>${data.chat.user2} (${data.chat.email})</li>`;
      chatForm.reset();
      setTimeout(closeModal, 800);
    } else {
      formMessage.style.color = "red";
      const errors = Object.values(data.errors).flat().join(" ");
      formMessage.textContent = errors;
    }
  });
});