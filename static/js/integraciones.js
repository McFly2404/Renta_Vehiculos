function t(key, fallback) {
  return window.DRIVENOW_I18N?.[key] ?? fallback;
}

async function loadIntegraciones() {
  const grid = document.getElementById('integracionesGrid');
  if (!grid) return;

  try {
    const [snapshotRes, resumenRes] = await Promise.all([
      fetch('/api/integraciones/snapshot/'),
      fetch('/api/integraciones/resumen/'),
    ]);

    const snapshot = await snapshotRes.json();
    const resumen = await resumenRes.json();
    const aliado = snapshot.ally_service ?? {};
    const tercero = snapshot.third_party ?? {};

    grid.innerHTML = `
      <article class="vehicle-card">
        <div class="vehicle-card__icon">API</div>
        <div class="vehicle-card__body">
          <span class="vehicle-card__cat">${t('ownService', 'Servicio a Proveer')}</span>
          <h3 class="vehicle-card__name">${t('systemSummary', 'Resumen del Sistema')}</h3>
          <p style="font-size:.82rem;color:var(--c-muted);margin-top:.4rem;">
            ${t('users', 'Usuarios')}: <strong>${resumen.usuarios ?? 0}</strong><br>
            ${t('reservations', 'Reservas')}: <strong>${resumen.reservas ?? 0}</strong><br>
            ${t('payments', 'Pagos')}: <strong>${resumen.pagos ?? 0}</strong>
          </p>
        </div>
        <span class="vehicle-card__badge">${t('active', 'Activo')}</span>
      </article>

      <article class="vehicle-card">
        <div class="vehicle-card__icon">HTTP</div>
        <div class="vehicle-card__body">
          <span class="vehicle-card__cat">${t('allyService', 'Servicio Aliado')}</span>
          <h3 class="vehicle-card__name">${aliado.source ?? t('notConfigured', 'No configurado')}</h3>
          <p style="font-size:.82rem;color:var(--c-muted);margin-top:.4rem;">
            ${t('status', 'Estado')}: <strong>${aliado.status ?? 'unknown'}</strong>
          </p>
        </div>
        <span class="vehicle-card__badge ${aliado.status === 'ok' ? '' : 'vehicle-card__badge--alt'}">
          ${aliado.status === 'ok' ? t('connected', 'Conectado') : t('pending', 'Pendiente')}
        </span>
      </article>

      <article class="vehicle-card">
        <div class="vehicle-card__icon">WX</div>
        <div class="vehicle-card__body">
          <span class="vehicle-card__cat">${t('apiThirdPartyAdapter', 'API de Terceros (Adapter)')}</span>
          <h3 class="vehicle-card__name">${tercero.city ?? 'Open-Meteo'}</h3>
          <p style="font-size:.82rem;color:var(--c-muted);margin-top:.4rem;">
            ${t('temperature', 'Temp')}: <strong>${tercero.temperature_c ?? '--'} C</strong><br>
            ${t('humidity', 'Humedad')}: <strong>${tercero.humidity_pct ?? '--'}%</strong><br>
            ${t('wind', 'Viento')}: <strong>${tercero.wind_kmh ?? '--'} km/h</strong>
          </p>
        </div>
        <span class="vehicle-card__badge ${tercero.status === 'ok' ? '' : 'vehicle-card__badge--alt'}">
          ${tercero.status === 'ok' ? t('available', 'Disponible') : t('noData', 'Sin datos')}
        </span>
      </article>
    `;
  } catch {
    grid.innerHTML = `<p style="color:var(--c-muted)">${t('integrationsLoadError', 'No se pudo cargar el estado de integraciones.')}</p>`;
  }
}

loadIntegraciones();
