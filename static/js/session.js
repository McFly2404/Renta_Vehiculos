/**
 * session.js — Gestión de sesión del usuario en el navegador.
 *
 * Usa sessionStorage para guardar los datos del usuario activo.
 * No requiere autenticación real en el backend (fuera del alcance
 * del proyecto). El "login" verifica que el usuario exista via API.
 */

const SESSION_KEY = 'drivenow_user';

const Session = {
  /** Guarda el usuario en sesión */
  set(usuario) {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(usuario));
  },

  /** Recupera el usuario de sesión o null */
  get() {
    try {
      return JSON.parse(sessionStorage.getItem(SESSION_KEY));
    } catch {
      return null;
    }
  },

  /** Cierra la sesión */
  clear() {
    sessionStorage.removeItem(SESSION_KEY);
  },

  /** ¿Hay usuario en sesión? */
  isActive() {
    return this.get() !== null;
  },
};
