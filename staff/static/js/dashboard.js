const ctx = document.getElementById("postsChart");
if (ctx) {
  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
      datasets: [
        {
          label: "Posts",
          data: [65, 59, 80, 81, 56, 55, 90],
          fill: true,
          backgroundColor: "rgba(99, 102, 241, 0.2)",
          borderColor: "rgba(99, 102, 241, 1)",
          tension: 0.4,
          pointBackgroundColor: "rgba(99, 102, 241, 1)",
          pointBorderColor: "#fff",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "rgba(99, 102, 241, 1)",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: "rgba(203, 213, 225, 0.5)",
          },
          ticks: {
            color: "#64748b",
          },
        },
        x: {
          grid: {
            display: false,
          },
          ticks: {
            color: "#64748b",
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
      },
    },
  });
}