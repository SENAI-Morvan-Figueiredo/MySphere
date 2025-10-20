const tabs = document.querySelectorAll('.tab');
const contents = document.querySelectorAll('.tab-content');
tabs.forEach(tab => {
  tab.addEventListener('click', () => {
    // remove estado ativo anterior
    tabs.forEach(t => t.classList.remove('active'));
    contents.forEach(c => c.classList.remove('active'));
    // ativa o clicado
    tab.classList.add('active');
    document.getElementById(tab.dataset.tab).classList.add('active');
  });
});