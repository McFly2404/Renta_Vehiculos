/**
 * main.js — Lógica de la página principal (index).
 *
 * Módulos:
 * 1. Utils compartidos
 * 2. Estado de sesión en la página
 * 3. Select de vehículos disponibles
 * 4. Formulario de reserva
 * 5. Formulario de pago
 * 6. Modales
 * 7. Skeleton → cards de flota
 */


/* ── 1. Utils ─────────────────────────────────────────────── */

function getCsrf() {
  return document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] ?? '';
}

function setLoading(btn, on) {
  btn.classList.toggle('btn--loading', on);
  btn.disabled = on;
}

function showAlert(el, msg) {
  el.textContent = msg;
  el.removeAttribute('hidden');
}

function clearAlert(el) {
  el.setAttribute('hidden', '');
}

function parseError(data) {
  if (typeof data === 'string') return data;
  if (data.error)               return data.error;
  return Object.entries(data)
    .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`)
    .join(' · ');
}

async function apiPost(url, payload) {
  const res  = await fetch(url, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body:    JSON.stringify(payload),
  });
  return { status: res.status, data: await res.json() };
}

function detailRows(rows) {
  return rows.map(([k, v]) =>
    `<div class="modal__detail-row"><dt>${k}</dt><dd>${v}</dd></div>`
  ).join('');
}


/* ── 2. Estado de sesión en la página ─────────────────────── */

(function syncSessionUI() {
  const user = Session.get();

  const banner    = document.getElementById('sessionBanner');
  const noSession = document.getElementById('noSessionTip');
  const bannerName = document.getElementById('sessionBannerName');
  const bannerId   = document.getElementById('sessionBannerId');

  if (user) {
    banner?.removeAttribute('hidden');
    noSession?.setAttribute('hidden', '');
    if (bannerName) bannerName.textContent = user.nombre.split(' ')[0];
    if (bannerId)   bannerId.textContent   = `#${user.id}`;

    // Pre-llenar ID de usuario
    const input = document.getElementById('usuario_id');
    if (input && !input.value) input.value = user.id;
  } else {
    banner?.setAttribute('hidden', '');
    noSession?.removeAttribute('hidden');
  }
})();


/* ── 3. Select de vehículos disponibles ───────────────────── */

const ICONS = { SEDAN:'🚗', SUV:'🚙', CAMIONETA:'🚐', DEPORTIVO:'🏎️', FURGON:'🚌' };

async function loadVehicleSelect() {
  const select  = document.getElementById('placa_vehiculo');
  const hint    = document.getElementById('vehiculoHint');
  if (!select) return;

  try {
    const res  = await fetch('/api/vehiculos/?disponible=true');
    const list = await res.json();

    if (!list.length) {
      select.innerHTML = '<option value="">No hay vehículos disponibles</option>';
      return;
    }

    select.innerHTML = '<option value="">— Selecciona un vehículo —</option>'
      + list.map(v =>
          `<option value="${v.placa}"
             data-modelo="${v.modelo}"
             data-cat="${v.categoria}"
             data-tarifa="${v.tarifa_diaria}"
             data-icon="${ICONS[v.categoria] ?? '🚗'}">
            ${ICONS[v.categoria] ?? '🚗'}  ${v.placa} — ${v.modelo} ($${Number(v.tarifa_diaria).toLocaleString('es-CO')}/día)
          </option>`
        ).join('');

    // Mostrar detalle del vehículo seleccionado
    select.addEventListener('change', () => {
      const opt = select.selectedOptions[0];
      if (!opt.value) { hint.textContent = ''; return; }
      hint.textContent =
        `${opt.dataset.icon} ${opt.dataset.cat} · ${opt.dataset.modelo} · $${Number(opt.dataset.tarifa).toLocaleString('es-CO')}/día`;
    });

  } catch {
    select.innerHTML = '<option value="">Error al cargar vehículos</option>';
  }
}

loadVehicleSelect();


/* ── 4. Fechas ────────────────────────────────────────────── */

const today       = new Date().toISOString().split('T')[0];
const inputInicio = document.getElementById('fecha_inicio');
const inputFin    = document.getElementById('fecha_fin');

if (inputInicio && inputFin) {
  inputInicio.min = today;
  inputFin.min    = today;
  inputInicio.addEventListener('change', () => {
    inputFin.min = inputInicio.value;
    if (inputFin.value && inputFin.value <= inputInicio.value) inputFin.value = '';
  });
}


/* ── 5. Formulario de reserva ─────────────────────────────── */

const reservaForm  = document.getElementById('reservaForm');
const alertReserva = document.getElementById('alertReserva');
const btnReserva   = document.getElementById('btnReserva');

reservaForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearAlert(alertReserva);
  setLoading(btnReserva, true);

  const payload = {
    usuario_id:     parseInt(document.getElementById('usuario_id').value, 10),
    placa_vehiculo: document.getElementById('placa_vehiculo').value.trim(),
    fecha_inicio:   inputInicio.value,
    fecha_fin:      inputFin.value,
  };

  try {
    const { status, data } = await apiPost('/api/reservas/crear/', payload);

    if (status === 201) {
      document.getElementById('modalReservaDetail').innerHTML = detailRows([
        ['ID Reserva',   `#${data.id}`],
        ['Usuario',      data.usuario?.nombre  ?? `#${payload.usuario_id}`],
        ['Vehículo',     data.vehiculo?.placa  ?? payload.placa_vehiculo],
        ['Modelo',       data.vehiculo?.modelo ?? '—'],
        ['Fecha inicio', data.fecha_inicio],
        ['Fecha fin',    data.fecha_fin],
        ['Estado',       data.estado],
      ]);

      // Pre-llenar ID en el formulario de pago
      const pagoInput = document.getElementById('pago_reserva_id');
      if (pagoInput) pagoInput.value = data.id;

      // Calcular monto sugerido
      const tarifa = data.vehiculo?.tarifa_diaria;
      if (tarifa) {
        const dias = Math.ceil(
          (new Date(data.fecha_fin) - new Date(data.fecha_inicio)) / 86400000
        );
        const montoInput = document.getElementById('pago_monto');
        if (montoInput) montoInput.value = (parseFloat(tarifa) * dias).toFixed(2);
      }

      openModal('modalReserva');
      reservaForm.reset();
      loadVehicleSelect(); // recargar select para reflejar cambio de disponibilidad
    } else {
      showAlert(alertReserva, parseError(data));
    }
  } catch {
    showAlert(alertReserva, 'No se pudo conectar al servidor.');
  } finally {
    setLoading(btnReserva, false);
  }
});


/* ── 6. Formulario de pago ────────────────────────────────── */

const pagoForm  = document.getElementById('pagoForm');
const alertPago = document.getElementById('alertPago');
const btnPago   = document.getElementById('btnPago');

const pagoFecha = document.getElementById('pago_fecha');
if (pagoFecha) pagoFecha.value = today;

pagoForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearAlert(alertPago);
  setLoading(btnPago, true);

  const payload = {
    reserva_id:  parseInt(document.getElementById('pago_reserva_id').value, 10),
    monto:       parseFloat(document.getElementById('pago_monto').value),
    metodo_pago: document.getElementById('pago_metodo').value,
    fecha_pago:  document.getElementById('pago_fecha').value,
  };

  try {
    const { status, data } = await apiPost('/api/pagos/', payload);

    if (status === 201) {
      document.getElementById('modalPagoDetail').innerHTML = detailRows([
        ['ID Pago',   `#${data.id}`],
        ['Reserva',   `#${data.reserva}`],
        ['Monto',     `$${Number(data.monto).toLocaleString('es-CO')}`],
        ['Método',    data.metodo_pago_display],
        ['Estado',    data.estado_pago_display],
        ['Fecha',     data.fecha_pago],
      ]);
      openModal('modalPago');
      pagoForm.reset();
      if (pagoFecha) pagoFecha.value = today;
    } else {
      showAlert(alertPago, parseError(data));
    }
  } catch {
    showAlert(alertPago, 'No se pudo conectar al servidor.');
  } finally {
    setLoading(btnPago, false);
  }
});


/* ── 7. Modales ───────────────────────────────────────────── */

function openModal(id) {
  document.getElementById(id)?.removeAttribute('hidden');
}
function closeModal(overlay) {
  overlay.setAttribute('hidden', '');
}

document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(overlay); });
});
document.querySelectorAll('.modal-close-btn').forEach(btn => {
  btn.addEventListener('click', () => closeModal(btn.closest('.modal-overlay')));
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape')
    document.querySelectorAll('.modal-overlay:not([hidden])').forEach(closeModal);
});

// "Ir a pagar" → cierra modal y hace scroll
document.getElementById('btnModalReservaIrPagar')?.addEventListener('click', () => {
  closeModal(document.getElementById('modalReserva'));
  setTimeout(() => document.getElementById('pagar')?.scrollIntoView({ behavior: 'smooth' }), 150);
});


/* ── 8. Cards de flota ────────────────────────────────────── */

async function loadFlota() {
  const grid = document.getElementById('vehiculosGrid');
  if (!grid) return;

  try {
    const res  = await fetch('/api/vehiculos/');
    const list = await res.json();
    if (!list.length) { grid.innerHTML = '<p style="color:var(--c-muted)">No hay vehículos registrados aún.</p>'; return; }

    grid.innerHTML = list.slice(0, 6).map((v, i) => `
      <article class="vehicle-card" style="cursor:pointer;animation-delay:${i * .08}s"
               data-placa="${v.placa}" title="Seleccionar ${v.placa}">
        <div class="vehicle-card__icon">${ICONS[v.categoria] ?? '🚗'}</div>
        <div class="vehicle-card__body">
          <span class="vehicle-card__cat">${v.categoria} · ${v.capacidad} pax</span>
          <h3 class="vehicle-card__name">${v.modelo}</h3>
          <p style="font-size:.78rem;color:var(--c-muted);margin:.15rem 0 .6rem">
            Placa: <strong>${v.placa}</strong>
          </p>
          <p class="vehicle-card__price">
            $${Number(v.tarifa_diaria).toLocaleString('es-CO')} <span>/ día</span>
          </p>
        </div>
        <span class="vehicle-card__badge ${v.disponible ? '' : 'vehicle-card__badge--alt'}">
          ${v.disponible ? 'Disponible' : 'Ocupado'}
        </span>
      </article>`
    ).join('');

    // Click en tarjeta de flota → selecciona placa en el formulario
    grid.querySelectorAll('.vehicle-card[data-placa]').forEach(card => {
      card.addEventListener('click', () => {
        const select = document.getElementById('placa_vehiculo');
        if (select) {
          select.value = card.dataset.placa;
          select.dispatchEvent(new Event('change'));  // dispara el hint
        }
        document.getElementById('reservar')?.scrollIntoView({ behavior: 'smooth' });
      });
    });

  } catch {
    grid.innerHTML = '';
  }
}

loadFlota();
