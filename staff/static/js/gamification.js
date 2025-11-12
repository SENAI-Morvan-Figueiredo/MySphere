document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".tab");
    const contents = document.querySelectorAll(".tab-content");
    const btnContainer = document.querySelector(".btn-container");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {

            tabs.forEach(t => t.classList.remove("active"));
            contents.forEach(c => c.classList.remove("active"));

            tab.classList.add("active");
            const section = document.getElementById(tab.dataset.tab);
            section.classList.add("active");

            if (tab.dataset.tab === "tarefas") {
                btnContainer.innerHTML = `
                    <a href="${btnContainer.dataset.urlTask}" class="btn-form">
                        <i class="fa-solid fa-plus"></i> Nova Tarefa
                    </a>`;
                btnContainer.style.display = "flex";
            } else if (tab.dataset.tab === "tarefas_user") {
                btnContainer.innerHTML = `
                    <a href="${btnContainer.dataset.urlUserTask}" class="btn-form">
                        <i class="fa-solid fa-plus"></i> Nova Atribuição
                    </a>`;
                btnContainer.style.display = "flex";
            } else {
                btnContainer.style.display = "none";
            }
        });
    });
});
