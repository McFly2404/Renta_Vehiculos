"""
Microservicio de Pagos — DriveNow
Patrón Estrangulador (Strangler Fig Pattern)

Reemplaza la lógica de pagos del monolito Django.
Expone la API en /api/v2/pagos/ y se conecta a la misma PostgreSQL.
"""
import os
import uuid
from decimal import Decimal, InvalidOperation

import psycopg2
import psycopg2.extras
from flask import Flask, request, jsonify

app = Flask(__name__)

# ── Conexión DB ───────────────────────────────────────────────────────────────

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "drivenow"),
        user=os.getenv("DB_USER", "drivenow"),
        password=os.getenv("DB_PASSWORD", "drivenow"),
    )


# ── Pasarela simulada (replica PasarelaFactory del monolito) ─────────────────

def _pasarela_simulada(monto: Decimal, metodo: str, referencia: str) -> dict:
    print(f"[DEV] Pago simulado: ${monto} | {metodo} | ref={referencia}")
    return {
        "aprobado": True,
        "codigo_transaccion": str(uuid.uuid4())[:8].upper(),
        "mensaje": "Pago aprobado (simulado)",
    }


# ── Constantes de dominio ─────────────────────────────────────────────────────

METODOS_VALIDOS = ["EFECTIVO", "TARJETA_CREDITO", "TARJETA_DEBITO", "TRANSFERENCIA"]


# ── Validación de payload ─────────────────────────────────────────────────────

def _validar(data: dict):
    """Retorna (errores_dict, monto_decimal)."""
    errores = {}

    if not data.get("reserva_id"):
        errores["reserva_id"] = "Requerido."

    monto_raw = data.get("monto")
    monto_dec = None
    if monto_raw is None:
        errores["monto"] = "Requerido."
    else:
        try:
            monto_dec = Decimal(str(monto_raw))
            if monto_dec <= 0:
                errores["monto"] = "Debe ser mayor a 0."
        except InvalidOperation:
            errores["monto"] = "Valor numérico inválido."

    if data.get("metodo_pago", "EFECTIVO") not in METODOS_VALIDOS:
        errores["metodo_pago"] = f"Opciones válidas: {METODOS_VALIDOS}"

    if not data.get("fecha_pago"):
        errores["fecha_pago"] = "Requerido. Formato: YYYY-MM-DD"

    return errores, monto_dec


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.route("/api/v2/pagos/", methods=["POST"])
def crear_pago():
    """
    POST /api/v2/pagos/
    Body JSON: { reserva_id, monto, metodo_pago, fecha_pago }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo debe ser JSON válido."}), 400

    errores, monto_dec = _validar(data)
    if errores:
        return jsonify({"errores": errores}), 400

    reserva_id  = int(data["reserva_id"])
    metodo_pago = data.get("metodo_pago", "EFECTIVO")
    fecha_pago  = data["fecha_pago"]

    try:
        conn = get_db()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # 1. Reserva existe?
        cur.execute("SELECT id, estado FROM reservas_reserva WHERE id = %s", (reserva_id,))
        reserva = cur.fetchone()
        if not reserva:
            cur.close(); conn.close()
            return jsonify({"error": f"Reserva #{reserva_id} no encontrada."}), 404

        # 2. No cancelada
        if reserva["estado"] == "CANCELADA":
            cur.close(); conn.close()
            return jsonify({"error": "No se puede pagar una reserva cancelada."}), 409

        # 3. Sin pago previo
        cur.execute("SELECT id FROM pagos_pago WHERE reserva_id = %s", (reserva_id,))
        if cur.fetchone():
            cur.close(); conn.close()
            return jsonify({"error": "Esta reserva ya tiene un pago registrado."}), 409

        # 4. Pasarela
        resultado = _pasarela_simulada(monto_dec, metodo_pago, f"RESERVA-{reserva_id}")
        estado_pago = "APROBADO" if resultado["aprobado"] else "RECHAZADO"

        # 5. Persistir pago
        cur.execute(
            """
            INSERT INTO pagos_pago
                (reserva_id, monto, estado_pago, metodo_pago, fecha_pago, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING id, reserva_id, monto, estado_pago, metodo_pago, fecha_pago, fecha_creacion
            """,
            (reserva_id, str(monto_dec), estado_pago, metodo_pago, fecha_pago)
        )
        pago = cur.fetchone()

        # 6. Confirmar reserva si fue aprobado
        if resultado["aprobado"]:
            cur.execute(
                "UPDATE reservas_reserva SET estado = 'CONFIRMADA' WHERE id = %s",
                (reserva_id,)
            )

        conn.commit()
        cur.close(); conn.close()

        return jsonify({
            "id":                 pago["id"],
            "reserva_id":         pago["reserva_id"],
            "monto":              str(pago["monto"]),
            "estado_pago":        pago["estado_pago"],
            "metodo_pago":        pago["metodo_pago"],
            "fecha_pago":         str(pago["fecha_pago"]),
            "fecha_creacion":     str(pago["fecha_creacion"]),
            "codigo_transaccion": resultado["codigo_transaccion"],
        }), 201

    except Exception as exc:
        return jsonify({"error": f"Error interno: {str(exc)}"}), 500


@app.route("/api/v2/pagos/<int:pago_id>/", methods=["GET"])
def obtener_pago(pago_id: int):
    """GET /api/v2/pagos/<id>/"""
    try:
        conn = get_db()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            "SELECT id, reserva_id, monto, estado_pago, metodo_pago, fecha_pago, fecha_creacion "
            "FROM pagos_pago WHERE id = %s",
            (pago_id,)
        )
        pago = cur.fetchone()
        cur.close(); conn.close()

        if not pago:
            return jsonify({"error": f"Pago #{pago_id} no encontrado."}), 404

        return jsonify({
            "id":             pago["id"],
            "reserva_id":     pago["reserva_id"],
            "monto":          str(pago["monto"]),
            "estado_pago":    pago["estado_pago"],
            "metodo_pago":    pago["metodo_pago"],
            "fecha_pago":     str(pago["fecha_pago"]),
            "fecha_creacion": str(pago["fecha_creacion"]),
        }), 200

    except Exception as exc:
        return jsonify({"error": f"Error interno: {str(exc)}"}), 500


@app.route("/api/v2/pagos/", methods=["GET"])
def listar_pagos():
    """GET /api/v2/pagos/"""
    try:
        conn = get_db()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            "SELECT id, reserva_id, monto, estado_pago, metodo_pago, fecha_pago "
            "FROM pagos_pago ORDER BY id DESC"
        )
        pagos = cur.fetchall()
        cur.close(); conn.close()

        return jsonify([
            {
                "id":          p["id"],
                "reserva_id":  p["reserva_id"],
                "monto":       str(p["monto"]),
                "estado_pago": p["estado_pago"],
                "metodo_pago": p["metodo_pago"],
                "fecha_pago":  str(p["fecha_pago"]),
            }
            for p in pagos
        ]), 200

    except Exception as exc:
        return jsonify({"error": f"Error interno: {str(exc)}"}), 500


@app.route("/api/v2/health/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "flask-pagos", "version": "v2"}), 200


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
