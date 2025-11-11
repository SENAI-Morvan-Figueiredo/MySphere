const tabs = document.querySelectorAll('.tab');
const contents = document.querySelectorAll('.tab-content');
const btn = document.querySelector('.btn-form');

const routes = {
  "tarefas": "{% url 'task_create' %}",
  "tarefas_user": "{% url 'user_task_create' %}",
};

tabs.forEach(tab => {
  tab.addEventListener('click', () => {
    tabs.forEach(t => t.classList.remove('active'));
    contents.forEach(c => c.classList.remove('active'));

    tab.classList.add('active');
    document.getElementById(tab.dataset.tab).classList.add('active');

    const selected = tab.dataset.tab;
    if (routes[selected]) {
      btn.href = routes[selected];
    }
  });
});
