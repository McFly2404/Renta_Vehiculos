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

function t(key, fallback) {
  return window.DRIVENOW_I18N?.[key] ?? fallback;
}

function parseError(data) {
  if (typeof data === 'string') return data;
  if (data.error) return data.error;
  return Object.entries(data)
    .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`)
    .join(' - ');
}

async function apiPost(url, payload) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body: JSON.stringify(payload),
  });
  return { status: res.status, data: await res.json() };
}

function detailRows(rows) {
  return rows.map(([k, v]) =>
    `<div class="modal__detail-row"><dt>${k}</dt><dd>${v}</dd></div>`
  ).join('');
}

function formatCurrency(value) {
  return Number(value).toLocaleString('es-CO');
}

const CATEGORY_LABELS = {
  SEDAN: 'SEDAN',
  SUV: 'SUV',
  CAMIONETA: 'CAMIONETA',
  DEPORTIVO: 'DEPORTIVO',
  FURGON: 'FURGON',
};

const CATEGORY_TAGS = {
  SEDAN: '🚗',
  SUV: '🚙',
  CAMIONETA: '🚚',
  DEPORTIVO: '🏎️',
  FURGON: '🚐',
};

function categoryLabel(category) {
  return CATEGORY_LABELS[category] ?? category ?? 'VEHICULO';
}

function categoryTag(category) {
  return CATEGORY_TAGS[category] ?? 'AUTO';
}

(function syncSessionUI() {
  const user = Session.get();

  const banner = document.getElementById('sessionBanner');
  const noSession = document.getElementById('noSessionTip');
  const bannerName = document.getElementById('sessionBannerName');
  const bannerId = document.getElementById('sessionBannerId');

  if (user) {
    banner?.removeAttribute('hidden');
    noSession?.setAttribute('hidden', '');
    if (bannerName) bannerName.textContent = user.nombre.split(' ')[0];
    if (bannerId) bannerId.textContent = `#${user.id}`;

    const input = document.getElementById('usuario_id');
    if (input && !input.value) input.value = user.id;
  } else {
    banner?.setAttribute('hidden', '');
    noSession?.removeAttribute('hidden');
  }
})();

async function loadVehicleSelect() {
  const select = document.getElementById('placa_vehiculo');
  const hint = document.getElementById('vehiculoHint');
  if (!select) return;

  try {
    const res = await fetch('/api/vehiculos/?disponible=true');
    const list = await res.json();

    if (!list.length) {
      select.innerHTML = `<option value="">${t('noVehiclesAvailable', 'No hay vehiculos disponibles')}</option>`;
      return;
    }

    select.innerHTML = `<option value="">${t('selectVehicle', 'Selecciona un vehiculo')}</option>`
      + list.map(v =>
          `<option value="${v.placa}"
             data-modelo="${v.modelo}"
             data-cat="${categoryLabel(v.categoria)}"
             data-tarifa="${v.tarifa_diaria}">
            ${v.placa} - ${v.modelo} ($${formatCurrency(v.tarifa_diaria)}/${t('day', 'dia')})
          </option>`
        ).join('');

    select.addEventListener('change', () => {
      const opt = select.selectedOptions[0];
      if (!opt.value) {
        hint.textContent = '';
        return;
      }
      hint.textContent =
        `${opt.dataset.cat} - ${opt.dataset.modelo} - $${formatCurrency(opt.dataset.tarifa)}/${t('day', 'dia')}`;
    });
  } catch {
    select.innerHTML = `<option value="">${t('fleetLoadError', 'Error al cargar vehiculos')}</option>`;
  }
}

loadVehicleSelect();

const today = new Date().toISOString().split('T')[0];
const inputInicio = document.getElementById('fecha_inicio');
const inputFin = document.getElementById('fecha_fin');

if (inputInicio && inputFin) {
  inputInicio.min = today;
  inputFin.min = today;
  inputInicio.addEventListener('change', () => {
    inputFin.min = inputInicio.value;
    if (inputFin.value && inputFin.value <= inputInicio.value) inputFin.value = '';
  });
}

const reservaForm = document.getElementById('reservaForm');
const alertReserva = document.getElementById('alertReserva');
const btnReserva = document.getElementById('btnReserva');

reservaForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearAlert(alertReserva);
  setLoading(btnReserva, true);

  const payload = {
    usuario_id: parseInt(document.getElementById('usuario_id').value, 10),
    placa_vehiculo: document.getElementById('placa_vehiculo').value.trim(),
    fecha_inicio: inputInicio.value,
    fecha_fin: inputFin.value,
  };

  try {
    const { status, data } = await apiPost('/api/reservas/crear/', payload);

    if (status === 201) {
      document.getElementById('modalReservaDetail').innerHTML = detailRows([
        [t('reservationId', 'ID Reserva'), `#${data.id}`],
        [t('user', 'Usuario'), data.usuario?.nombre ?? `#${payload.usuario_id}`],
        [t('vehicle', 'Vehiculo'), data.vehiculo?.placa ?? payload.placa_vehiculo],
        [t('model', 'Modelo'), data.vehiculo?.modelo ?? '-'],
        [t('reservationStart', 'Fecha inicio'), data.fecha_inicio],
        [t('reservationEnd', 'Fecha fin'), data.fecha_fin],
        [t('status', 'Estado'), data.estado],
      ]);

      const pagoInput = document.getElementById('pago_reserva_id');
      if (pagoInput) pagoInput.value = data.id;

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
      loadVehicleSelect();
    } else {
      showAlert(alertReserva, parseError(data));
    }
  } catch {
    showAlert(alertReserva, t('connectingError', 'No se pudo conectar al servidor.'));
  } finally {
    setLoading(btnReserva, false);
  }
});

const pagoForm = document.getElementById('pagoForm');
const alertPago = document.getElementById('alertPago');
const btnPago = document.getElementById('btnPago');
const pagoFecha = document.getElementById('pago_fecha');
if (pagoFecha) pagoFecha.value = today;

async function registrarPago(payload) {
  const endpoints = ['/api/v2/pagos/', '/api/pagos/'];

  for (const endpoint of endpoints) {
    try {
      const result = await apiPost(endpoint, payload);
      if (result.status !== 404 || endpoint === '/api/pagos/') {
        return result;
      }
    } catch (err) {
      if (endpoint === '/api/pagos/') {
        throw err;
      }
    }
  }

  return { status: 500, data: { error: t('paymentRegisterError', 'No se pudo registrar el pago.') } };
}

function normalizarPago(data, payload) {
  return {
    id: data.id,
    reserva: data.reserva ?? data.reserva_id ?? payload.reserva_id,
    monto: data.monto,
    metodo_pago_display: data.metodo_pago_display ?? data.metodo_pago ?? payload.metodo_pago,
    estado_pago_display: data.estado_pago_display ?? data.estado_pago ?? 'APROBADO',
    fecha_pago: data.fecha_pago ?? payload.fecha_pago,
  };
}

pagoForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearAlert(alertPago);
  setLoading(btnPago, true);

  const payload = {
    reserva_id: parseInt(document.getElementById('pago_reserva_id').value, 10),
    monto: parseFloat(document.getElementById('pago_monto').value),
    metodo_pago: document.getElementById('pago_metodo').value,
    fecha_pago: document.getElementById('pago_fecha').value,
  };

  try {
    const { status, data } = await registrarPago(payload);

    if (status === 201) {
      const pago = normalizarPago(data, payload);
      document.getElementById('modalPagoDetail').innerHTML = detailRows([
        [t('paymentId', 'ID Pago'), `#${pago.id}`],
        [t('reservation', 'Reserva'), `#${pago.reserva}`],
        [t('amount', 'Monto'), `$${formatCurrency(pago.monto)}`],
        [t('method', 'Metodo'), pago.metodo_pago_display],
        [t('status', 'Estado'), pago.estado_pago_display],
        [t('paymentDate', 'Fecha'), pago.fecha_pago],
      ]);
      openModal('modalPago');
      pagoForm.reset();
      if (pagoFecha) pagoFecha.value = today;
    } else {
      showAlert(alertPago, parseError(data));
    }
  } catch {
    showAlert(alertPago, t('connectingError', 'No se pudo conectar al servidor.'));
  } finally {
    setLoading(btnPago, false);
  }
});

function openModal(id) {
  document.getElementById(id)?.removeAttribute('hidden');
}

function closeModal(overlay) {
  overlay.setAttribute('hidden', '');
}

document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', e => {
    if (e.target === overlay) closeModal(overlay);
  });
});

document.querySelectorAll('.modal-close-btn').forEach(btn => {
  btn.addEventListener('click', () => closeModal(btn.closest('.modal-overlay')));
});

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay:not([hidden])').forEach(closeModal);
  }
});

document.getElementById('btnModalReservaIrPagar')?.addEventListener('click', () => {
  closeModal(document.getElementById('modalReserva'));
  setTimeout(() => document.getElementById('pagar')?.scrollIntoView({ behavior: 'smooth' }), 150);
});

async function loadFlota() {
  const grid = document.getElementById('vehiculosGrid');
  if (!grid) return;

  try {
    const res = await fetch('/api/vehiculos/');
    const list = await res.json();
    if (!list.length) {
      grid.innerHTML = `<p style="color:var(--c-muted)">${t('noVehiclesRegistered', 'No hay vehiculos registrados aun.')}</p>`;
      return;
    }

    grid.innerHTML = list.slice(0, 6).map((v, i) => `
      <article class="vehicle-card" style="cursor:pointer;animation-delay:${i * .08}s"
               data-placa="${v.placa}" title="${t('select', 'Seleccionar')} ${v.placa}">
        <div class="vehicle-card__icon vehicle-card__icon--text">${categoryTag(v.categoria)}</div>
        <div class="vehicle-card__body">
          <span class="vehicle-card__cat">${categoryLabel(v.categoria)} - ${v.capacidad} pax</span>
          <h3 class="vehicle-card__name">${v.modelo}</h3>
          <p style="font-size:.78rem;color:var(--c-muted);margin:.15rem 0 .6rem">
            ${t('plate', 'Placa')}: <strong>${v.placa}</strong>
          </p>
          <p class="vehicle-card__price">
            $${formatCurrency(v.tarifa_diaria)} <span>/ ${t('day', 'dia')}</span>
          </p>
        </div>
        <span class="vehicle-card__badge ${v.disponible ? '' : 'vehicle-card__badge--alt'}">
          ${v.disponible ? t('available', 'Disponible') : t('occupied', 'Ocupado')}
        </span>
      </article>`
    ).join('');

    grid.querySelectorAll('.vehicle-card[data-placa]').forEach(card => {
      card.addEventListener('click', () => {
        const select = document.getElementById('placa_vehiculo');
        if (select) {
          select.value = card.dataset.placa;
          select.dispatchEvent(new Event('change'));
        }
        document.getElementById('reservar')?.scrollIntoView({ behavior: 'smooth' });
      });
    });
  } catch {
    grid.innerHTML = '';
  }
}

loadFlota();
