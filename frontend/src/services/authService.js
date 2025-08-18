const TOKEN_KEY = 'vaultupload_token';

const authService = {
  login: async (username, password) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!res.ok) throw new Error('Login failed');
    const { token } = await res.json();
    localStorage.setItem(TOKEN_KEY, token);
  },
  logout: () => {
    localStorage.removeItem(TOKEN_KEY);
  },
  getToken: () => localStorage.getItem(TOKEN_KEY),
  isAuthenticated: () => !!localStorage.getItem(TOKEN_KEY)
};

export default authService;
