(function initNav() {
  const user = Session.get();
  const navGuest = document.getElementById('navGuest');
  const navUser = document.getElementById('navUser');
  const nameEl = document.getElementById('navUserName');
  const idEl = document.getElementById('navUserId');
  const avatarEl = document.getElementById('navUserAvatar');
  const btnLogout = document.getElementById('btnLogout');

  if (user) {
    navGuest.setAttribute('hidden', '');
    navUser.removeAttribute('hidden');
    nameEl.textContent = user.nombre.split(' ')[0];
    idEl.textContent = `#${user.id}`;
    avatarEl.textContent = user.nombre.charAt(0).toUpperCase();

    const usuarioInput = document.getElementById('usuario_id');
    if (usuarioInput && !usuarioInput.value) {
      usuarioInput.value = user.id;
    }
  } else {
    navGuest.removeAttribute('hidden');
    navUser.setAttribute('hidden', '');
  }

  btnLogout?.addEventListener('click', () => {
    Session.clear();
    window.location.href = '/';
  });
})();
