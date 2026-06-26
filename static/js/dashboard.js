/* Dashboard chart rendering using Chart.js */
document.addEventListener('DOMContentLoaded', async () => {
  const searchesChartEl = document.querySelector('#searchesChart');
  const genresChartEl = document.querySelector('#genresChart');
  const activityChartEl = document.querySelector('#activityChart');

  if (!searchesChartEl || !genresChartEl || !activityChartEl) {
    return;
  }

  try {
    const response = await fetch('/dashboard/data');
    const data = await response.json();

    const searchLabels = Object.keys(data.searches_per_day);
    const searchValues = Object.values(data.searches_per_day);

    new Chart(searchesChartEl, {
      type: 'line',
      data: {
        labels: searchLabels,
        datasets: [
          {
            label: 'Searches',
            data: searchValues,
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56,189,248,0.2)',
            tension: 0.35,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { ticks: { color: '#cbd5e1' } },
          y: { ticks: { color: '#cbd5e1' }, beginAtZero: true },
        },
        plugins: {
          legend: { labels: { color: '#f8fafc' } },
        },
      },
    });

    new Chart(genresChartEl, {
      type: 'bar',
      data: {
        labels: Object.keys(data.favorite_genres),
        datasets: [
          {
            label: 'Favorites by genre',
            data: Object.values(data.favorite_genres),
            backgroundColor: '#f97316',
            borderRadius: 8,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { ticks: { color: '#cbd5e1' } },
          y: { ticks: { color: '#cbd5e1' }, beginAtZero: true },
        },
        plugins: { legend: { display: false } },
      },
    });

    new Chart(activityChartEl, {
      type: 'doughnut',
      data: {
        labels: ['Searches', 'Favorites', 'Movie Catalog'],
        datasets: [
          {
            data: [
              data.user_activity.searches,
              data.user_activity.favorites,
              data.user_activity.movie_catalog,
            ],
            backgroundColor: ['#38bdf8', '#34d399', '#f59e0b'],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#f8fafc' } },
        },
      },
    });
  } catch (error) {
    console.error('Dashboard data fetch failed', error);
  }
});
