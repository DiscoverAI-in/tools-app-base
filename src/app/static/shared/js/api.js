/**
 * Shared API client — import via <script src="/static/js/api.js"></script>
 * then use: const data = await api.get('/api/v1/health')
 */
const api = {
  base: '',  // same origin

  async request(method, path, body = null) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body) opts.body = JSON.stringify(body);

    const res = await fetch(`${this.base}${path}`, opts);

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    return res.json();
  },

  get(path)        { return this.request('GET', path); },
  post(path, body) { return this.request('POST', path, body); },
  put(path, body)  { return this.request('PUT', path, body); },
  del(path)        { return this.request('DELETE', path); },
};
