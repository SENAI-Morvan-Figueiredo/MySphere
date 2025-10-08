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
