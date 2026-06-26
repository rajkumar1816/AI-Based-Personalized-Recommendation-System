/* Main frontend interactions: search, recommendations, suggestions, and favorites */
document.addEventListener('DOMContentLoaded', async () => {
  const form = document.querySelector('#search-form');
  const queryInput = document.querySelector('#query');
  const suggestionsEl = document.querySelector('#suggestions');
  const ratingInput = document.querySelector('#rating');
  const ratingValue = document.querySelector('#rating-value');
  const resultsEl = document.querySelector('#results');

  if (ratingInput && ratingValue) {
    ratingValue.textContent = ratingInput.value;
    ratingInput.addEventListener('input', () => {
      ratingValue.textContent = ratingInput.value;
    });
  }

  if (queryInput && suggestionsEl) {
    let suggestionTimer;
    queryInput.addEventListener('input', () => {
      const value = queryInput.value.trim();
      if (suggestionTimer) clearTimeout(suggestionTimer);
      if (!value) {
        suggestionsEl.innerHTML = '';
        return;
      }
      suggestionTimer = setTimeout(() => {
        fetchSuggestions(value);
      }, 250);
    });
  }

  if (form) {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const query = queryInput?.value.trim();
      if (!query) {
        showToast('Please enter a search query to get recommendations.');
        return;
      }

      const category = document.querySelector('#category')?.value || 'all';
      const genre = document.querySelector('#genre')?.value || 'All';
      const language = document.querySelector('#language')?.value || 'All';
      const rating = document.querySelector('#rating')?.value || '';
      const year = document.querySelector('#year')?.value || 'All';

      const urlParams = new URLSearchParams();
      urlParams.set('q', query);
      urlParams.set('category', category);
      if (genre && genre !== 'All') urlParams.set('genre', genre);
      if (language && language !== 'All') urlParams.set('language', language);
      if (rating) urlParams.set('rating', rating);
      if (year && year !== 'All') urlParams.set('year', year);

      window.location.href = `/recommend?${urlParams.toString()}`;
    });
  }

  if (resultsEl) {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    if (query) {
      const params = {
        query,
        category: urlParams.get('category') || 'all',
        genre: urlParams.get('genre') || 'All',
        language: urlParams.get('language') || 'All',
        rating: urlParams.get('rating') || '',
        year: urlParams.get('year') || 'All',
      };
      if (queryInput) queryInput.value = params.query;
      if (document.querySelector('#category')) document.querySelector('#category').value = params.category;
      if (document.querySelector('#genre')) document.querySelector('#genre').value = params.genre;
      if (document.querySelector('#language')) document.querySelector('#language').value = params.language;
      if (document.querySelector('#rating')) document.querySelector('#rating').value = params.rating;
      if (document.querySelector('#year')) document.querySelector('#year').value = params.year;
      // Use server-rendered results for query-loaded pages instead of fetching again.
    }
  }

  function getSearchParams() {
    return {
      query: document.querySelector('#query')?.value.trim() || '',
      category: document.querySelector('#category')?.value || 'all',
      genre: document.querySelector('#genre')?.value || 'All',
      language: document.querySelector('#language')?.value || 'All',
      rating: document.querySelector('#rating')?.value || '',
      year: document.querySelector('#year')?.value || 'All',
    };
  }

  function redirectToRecommend(params) {
    const urlParams = new URLSearchParams();
    urlParams.set('q', params.query);
    urlParams.set('category', params.category);
    if (params.genre && params.genre !== 'All') urlParams.set('genre', params.genre);
    if (params.language && params.language !== 'All') urlParams.set('language', params.language);
    if (params.rating) urlParams.set('rating', params.rating);
    if (params.year && params.year !== 'All') urlParams.set('year', params.year);
    window.location.href = `/recommend?${urlParams.toString()}`;
  }

  async function requestRecommendations(params) {
    if (!resultsEl) return;
    resultsEl.innerHTML = '<div class="spinner"></div>';
    try {
      const response = await fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: params.query,
          category: params.category,
          genre: params.genre,
          language: params.language,
          rating: params.rating,
          year: params.year,
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        showToast(data.error || 'Unable to fetch recommendations.');
        resultsEl.innerHTML = '<div class="card">No recommendations found.</div>';
        return;
      }
      renderResults(data.recommendations || []);
    } catch (error) {
      console.error('recommend fetch failed', error);
      resultsEl.innerHTML = '<div class="card">Failed to fetch recommendations.</div>';
    }
  }
});

async function fetchSuggestions(query) {
  const suggestionsEl = document.querySelector('#suggestions');
  if (!suggestionsEl) return;

  try {
    const response = await fetch(`/suggestions?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    if (!Array.isArray(data.suggestions) || data.suggestions.length === 0) {
      suggestionsEl.innerHTML = '';
      return;
    }

    suggestionsEl.innerHTML = data.suggestions
      .slice(0, 6)
      .map((text) => `<button type="button" class="suggestion-item" onclick="applySuggestion('${escapeHtml(text)}')">${text}</button>`)
      .join('');
  } catch (error) {
    suggestionsEl.innerHTML = '';
  }
}

function applySuggestion(value) {
  const queryInput = document.querySelector('#query');
  const suggestionsEl = document.querySelector('#suggestions');
  if (!queryInput) return;
  queryInput.value = value;
  if (suggestionsEl) suggestionsEl.innerHTML = '';
}

function renderResults(items) {
  const resultsEl = document.querySelector('#results');
  if (!resultsEl) return;
  if (!items || items.length === 0) {
    resultsEl.innerHTML = '<div class="card">No recommendations found. Try a different search query.</div>';
    return;
  }

  resultsEl.innerHTML = items
    .map((item) => {
      const explanationList = item.explanation
        ? `<ul class="explanation-list">${item.explanation.map((reason) => `<li>${reason}</li>`).join('')}</ul>`
        : '';

      return `
        <article class="card result-card">
          <div class="card-header">
            <div>
              <h3>${item.title}</h3>
              <p class="caption">${item.genre} • ${item.language} • ${item.year}</p>
            </div>
            <span class="match-pill">${item.match}% match</span>
          </div>
          <p>${item.description}</p>
          ${explanationList}
          <div class="card-actions">
            <button class="btn btn-secondary" onclick="saveFavorite('${escapeHtml(item.title)}','${escapeHtml(item.genre)}')">Save Favorite</button>
            <button class="btn" onclick="showDetails()">View Details</button>
          </div>
        </article>
      `;
    })
    .join('');
}

function showDetails() {
  showToast('Details will be available in the next release.');
}

function escapeHtml(value) {
  return String(value).replace(/'/g, "\\'").replace(/"/g, '\\"');
}

async function saveFavorite(title, genre) {
  try {
    const response = await fetch('/favorites', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, genre }),
    });
    const data = await response.json();
    if (!response.ok) {
      showToast(data.error || 'Unable to save favorite.');
      return;
    }
    showToast('Saved to favorites successfully.');
  } catch (error) {
    showToast('Failed to save favorite.');
  }
}

function showToast(message) {
  const toast = document.querySelector('#toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.remove('hidden');
  toast.classList.add('active');
  window.clearTimeout(window.__toastTimeout);
  window.__toastTimeout = window.setTimeout(() => {
    toast.classList.remove('active');
    toast.classList.add('hidden');
  }, 3000);
}
