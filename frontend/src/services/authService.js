const TOKEN_KEY = 'vaultupload_token';

const authService = {
  register: async ({ username, password, email, hcaptchaToken }) => {
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, email, hcaptcha_token: hcaptchaToken })
    });
    if (!res.ok) throw new Error((await res.json()).detail || 'Register failed');
    return res.json();
  },
  // hcaptchaToken optional (when captcha enabled)
  login: async (username, password, hcaptchaToken) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, hcaptcha_token: hcaptchaToken })
    });
    if (!res.ok) throw new Error((await res.json()).detail || 'Login failed');
    const { token } = await res.json();
    localStorage.setItem(TOKEN_KEY, token);
  },
  forgot: async (username) => {
    const res = await fetch('/api/auth/forgot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username })
    });
    if (!res.ok) throw new Error('Request failed');
    return res.json();
  },
  resetPassword: async (token, newPassword) => {
    const res = await fetch('/api/auth/reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, new_password: newPassword })
    });
    if (!res.ok) throw new Error('Reset failed');
    return res.json();
  },
  logout: () => {
    localStorage.removeItem(TOKEN_KEY);
  },
  getToken: () => localStorage.getItem(TOKEN_KEY),
  isAuthenticated: () => !!localStorage.getItem(TOKEN_KEY)
};

export default authService;
