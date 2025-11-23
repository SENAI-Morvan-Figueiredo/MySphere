const canvas = document.getElementById("postsChart");

if (canvas) {

  const labels = JSON.parse(document.getElementById("labels-data").textContent);
  const counts = JSON.parse(document.getElementById("counts-data").textContent);

  new Chart(canvas, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Posts",
          data: counts,
          fill: true,
          backgroundColor: "rgba(99, 102, 241, 0.2)",
          borderColor: "rgba(99, 102, 241, 1)",
          tension: 0.4,
          pointBackgroundColor: "rgba(99, 102, 241, 1)",
          pointBorderColor: "#fff",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
        beginAtZero: true,
        ticks: {
            color: "#64748b",
            callback: function(value) {
            return Number.isInteger(value) ? value : null;
            }
        },
        grid: { color: "rgba(203, 213, 225, 0.5)" }
        },
        x: {
          ticks: { color: "#64748b" },
          grid: { display: false },
        },
      },
      plugins: { legend: { display: false } },
    },
  });
}
