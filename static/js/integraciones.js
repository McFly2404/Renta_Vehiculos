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
          <span class="vehicle-card__cat">Servicio a Proveer</span>
          <h3 class="vehicle-card__name">Resumen del Sistema</h3>
          <p style="font-size:.82rem;color:var(--c-muted);margin-top:.4rem;">
            Usuarios: <strong>${resumen.usuarios ?? 0}</strong><br>
            Reservas: <strong>${resumen.reservas ?? 0}</strong><br>
            Pagos: <strong>${resumen.pagos ?? 0}</strong>
          </p>
        </div>
        <span class="vehicle-card__badge">Activo</span>
      </article>

      <article class="vehicle-card">
        <div class="vehicle-card__icon">HTTP</div>
        <div class="vehicle-card__body">
          <span class="vehicle-card__cat">Servicio Aliado</span>
          <h3 class="vehicle-card__name">${aliado.source ?? 'No configurado'}</h3>
          <p style="font-size:.82rem;color:var(--c-muted);margin-top:.4rem;">
            Estado: <strong>${aliado.status ?? 'unknown'}</strong>
          </p>
        </div>
        <span class="vehicle-card__badge ${aliado.status === 'ok' ? '' : 'vehicle-card__badge--alt'}">
          ${aliado.status === 'ok' ? 'Conectado' : 'Pendiente'}
        </span>
      </article>

      <article class="vehicle-card">
        <div class="vehicle-card__icon">WX</div>
        <div class="vehicle-card__body">
          <span class="vehicle-card__cat">API de Terceros (Adapter)</span>
          <h3 class="vehicle-card__name">${tercero.city ?? 'Open-Meteo'}</h3>
          <p style="font-size:.82rem;color:var(--c-muted);margin-top:.4rem;">
            Temp: <strong>${tercero.temperature_c ?? '--'} C</strong><br>
            Humedad: <strong>${tercero.humidity_pct ?? '--'}%</strong><br>
            Viento: <strong>${tercero.wind_kmh ?? '--'} km/h</strong>
          </p>
        </div>
        <span class="vehicle-card__badge ${tercero.status === 'ok' ? '' : 'vehicle-card__badge--alt'}">
          ${tercero.status === 'ok' ? 'Disponible' : 'Sin datos'}
        </span>
      </article>
    `;
  } catch {
    grid.innerHTML = '<p style="color:var(--c-muted)">No se pudo cargar el estado de integraciones.</p>';
  }
}

loadIntegraciones();
