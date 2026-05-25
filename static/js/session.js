const SESSION_KEY = 'drivenow_user';

const Session = {
  set(usuario) {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(usuario));
  },

  get() {
    try {
      return JSON.parse(sessionStorage.getItem(SESSION_KEY));
    } catch {
      return null;
    }
  },

  clear() {
    sessionStorage.removeItem(SESSION_KEY);
  },

  isActive() {
    return this.get() !== null;
  },
};
