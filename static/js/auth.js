function getCsrf() {
  return document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] ?? '';
}

function setLoading(btn, on) {
  btn.classList.toggle('btn--loading', on);
  btn.disabled = on;
}

function showAlert(el, msg, type = 'error') {
  el.textContent = msg;
  el.className = `alert alert--${type}`;
  el.removeAttribute('hidden');
}

function clearAlert(el) {
  el.setAttribute('hidden', '');
}

function t(key, fallback) {
  return window.DRIVENOW_I18N?.[key] ?? fallback;
}

const registroForm = document.getElementById('registroForm');
const alertRegistro = document.getElementById('alertRegistro');
const btnRegistro = document.getElementById('btnRegistro');

registroForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearAlert(alertRegistro);
  setLoading(btnRegistro, true);

  const payload = {
    nombre: document.getElementById('reg_nombre').value.trim(),
    cedula: document.getElementById('reg_cedula').value.trim(),
    correo: document.getElementById('reg_correo').value.trim(),
    licencia: document.getElementById('reg_licencia').value.trim(),
  };

  try {
    const res = await fetch('/api/usuarios/crear/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (res.status === 201) {
      Session.set({ id: data.id, nombre: data.nombre, cedula: data.cedula });
      window.location.href = '/';
    } else {
      const msg = data.error
        ?? Object.entries(data).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' - ');
      showAlert(alertRegistro, msg);
    }
  } catch {
    showAlert(alertRegistro, t('connectingError', 'No se pudo conectar al servidor.'));
  } finally {
    setLoading(btnRegistro, false);
  }
});

const loginForm = document.getElementById('loginForm');
const alertLogin = document.getElementById('alertLogin');
const alertSuccess = document.getElementById('alertSuccess');
const btnLogin = document.getElementById('btnLogin');

loginForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearAlert(alertLogin);
  clearAlert(alertSuccess);
  setLoading(btnLogin, true);

  const id = parseInt(document.getElementById('login_id').value, 10);

  try {
    const res = await fetch(`/api/usuarios/${id}/`);
    const data = await res.json();

    if (res.status === 200) {
      Session.set({ id: data.id, nombre: data.nombre, cedula: data.cedula });
      showAlert(alertSuccess, `${t('welcome', 'Bienvenido')}, ${data.nombre}. ${t('redirecting', 'Redirigiendo...')}`, 'success');
      setTimeout(() => { window.location.href = '/'; }, 900);
    } else {
      showAlert(alertLogin, `${t('user', 'Usuario')} #${id} ${t('userNotFoundSuffix', 'no encontrado. Verifica tu ID.')}`);
    }
  } catch {
    showAlert(alertLogin, t('connectingError', 'No se pudo conectar al servidor.'));
  } finally {
    setLoading(btnLogin, false);
  }
});
