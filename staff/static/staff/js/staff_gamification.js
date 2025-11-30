document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".tab");
    const contents = document.querySelectorAll(".tab-content");
    const btnContainer = document.querySelector(".btn-container");

    // Verifica se os elementos existem antes de rodar para evitar erros
    if(tabs.length > 0 && btnContainer) {
        tabs.forEach(tab => {
            tab.addEventListener("click", () => {

                tabs.forEach(t => t.classList.remove("active"));
                contents.forEach(c => c.classList.remove("active"));

                tab.classList.add("active");
                const section = document.getElementById(tab.dataset.tab);
                if(section) section.classList.add("active");

                // Lógica de troca de botões (Mantida a original)
                if (tab.dataset.tab === "tarefas") {
                    btnContainer.innerHTML = `
                        <a href="${btnContainer.dataset.urlTask}" class="btn-form">
                            <i class="fa-solid fa-plus"></i> Nova Tarefa
                        </a>`;
                    btnContainer.style.display = "block"; // Mudado para block ou flex via CSS
                } else if (tab.dataset.tab === "tarefas_user") {
                    btnContainer.innerHTML = `
                        <a href="${btnContainer.dataset.urlUserTask}" class="btn-form">
                            <i class="fa-solid fa-plus"></i> Nova Atribuição
                        </a>`;
                    btnContainer.style.display = "block";
                } else if (tab.dataset.tab === "conquistas") {
                    btnContainer.innerHTML = `
                        <a href="${btnContainer.dataset.urlConquistas}" class="btn-form">
                            <i class="fa-solid fa-plus"></i> Nova Conquista
                        </a>`;
                    btnContainer.style.display = "block";
                } else {
                    btnContainer.style.display = "none";
                }
            });
        });
    }
});