"""
Centro de Control Diario · Definición
Entrenamiento · Nutrición · Movilidad · Mantenimiento del espacio

Ejecutar local:  streamlit run app.py
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────
# CONFIGURACIÓN GENERAL
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Centro de Control · Definición",
    page_icon="🥊",
    layout="centered",
)

TZ = ZoneInfo("America/Santiago")
DATA_FILE = Path(__file__).parent / "progreso.json"

# Metas estrictas
KCAL_MIN, KCAL_MAX = 2150, 2200
PROT_MIN, PROT_MAX = 140, 150

EQUIPAMIENTO = ["Anillas", "Mancuernas", "Saco de boxeo", "Bandas elásticas"]
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

AHORA = datetime.now(TZ)
HOY = AHORA.date()
HOY_STR = HOY.isoformat()
DIA_HOY = DIAS[HOY.weekday()]
_iso = HOY.isocalendar()
SEMANA_STR = f"{_iso[0]}-S{_iso[1]:02d}"
ES_VIERNES = HOY.weekday() == 4

# ─────────────────────────────────────────────
# DATOS DEL PLAN
# ─────────────────────────────────────────────
ACTIVACION_BANDAS = [
    "Band pull-aparts · 2x15",
    "Dislocaciones de hombro con banda · 2x10",
    "Rotación externa de hombro con banda · 2x12 por lado",
    "Monster walk / caminata lateral con banda · 2x10 pasos por lado",
    "Glute bridge con banda en rodillas · 2x15",
]

PLAN_SEMANAL = {
    "Lunes": {
        "titulo": "💪 Fuerza tren superior (anillas + mancuernas)",
        "bloques": {
            "Activación con bandas (8-10 min)": ACTIVACION_BANDAS,
            "Anillas": [
                "Dominadas en anillas · 4x6-8",
                "Fondos en anillas · 4x6-8",
                "Remo invertido en anillas · 3x10-12",
                "Flexiones en anillas · 3x10-12",
            ],
            "Mancuernas": [
                "Press militar con mancuernas · 3x10",
                "Curl martillo · 3x12",
                "Elevaciones laterales · 3x15",
            ],
            "Core": ["Plancha 3x45 s", "Knee raises en anillas 3x12"],
        },
    },
    "Martes": {
        "titulo": "🥊 Técnica en saco + MMA",
        "bloques": {
            "Activación con bandas (8-10 min)": ACTIVACION_BANDAS,
            "Saco de boxeo (mañana/tarde, ritmo suave)": [
                "Sombra 2 rounds x 3 min",
                "Saco técnico: jab-cross-hook · 4 rounds x 3 min (descanso 1 min)",
                "Patadas bajas y medias al saco · 3 rounds x 2 min",
            ],
            "Clase": ["🥋 Clase de MMA · 20:00 hrs"],
            "Recuperación": ["Snack proteico pre-clase (~17:30-18:30)", "Estirar 5 min post-clase"],
        },
    },
    "Miércoles": {
        "titulo": "🦵 Tren inferior + core (mancuernas + bandas)",
        "bloques": {
            "Activación con bandas (8-10 min)": ACTIVACION_BANDAS,
            "Mancuernas": [
                "Sentadilla goblet · 4x10",
                "Peso muerto rumano · 4x10",
                "Zancada búlgara · 3x10 por pierna",
                "Step-ups / zancadas caminando · 3x12",
            ],
            "Bandas / Anillas": [
                "Hip thrust con banda · 3x15",
                "Pistol squat asistido con anillas · 3x6 por pierna",
            ],
            "Core": ["Rueda / body saw en anillas 3x10", "Russian twist con mancuerna 3x20"],
        },
    },
    "Jueves": {
        "titulo": "🧘 Movilidad + MMA",
        "bloques": {
            "Activación con bandas (8-10 min)": ACTIVACION_BANDAS,
            "Movilidad (ver pestaña Movilidad)": [
                "Rutina de movilidad para patadas completa",
                "Rutina de movilidad de brazos/hombros completa",
            ],
            "Clase": ["🥋 Clase de MMA · 20:00 hrs"],
            "Recuperación": ["Snack proteico pre-clase (~17:30-18:30)", "Estirar 5 min post-clase"],
        },
    },
    "Viernes": {
        "titulo": "🔥 HIIT en saco + full body anillas + mantenimiento",
        "bloques": {
            "Activación con bandas (8-10 min)": ACTIVACION_BANDAS,
            "Saco de boxeo HIIT": [
                "8 rounds: 30 s máxima intensidad / 30 s ritmo medio (x3 min) · 1 min descanso",
                "Finisher: 100 golpes rectos sin parar",
            ],
            "Anillas (volumen ligero)": [
                "Remo en anillas · 3x12",
                "Flexiones en anillas · 3x12",
                "Face pulls en anillas · 3x15",
            ],
            "Espacio": ["Checklist de mantenimiento completado (pestaña Mantenimiento)"],
        },
    },
    "Sábado": {
        "titulo": "⚡ Circuito metabólico full body",
        "bloques": {
            "Activación con bandas (8-10 min)": ACTIVACION_BANDAS,
            "Circuito x 4 vueltas (descanso 90 s entre vueltas)": [
                "Thrusters con mancuernas · 12",
                "Dominadas en anillas · 6-8",
                "Renegade row con mancuernas · 10",
                "Saco: 1 min de combinaciones continuas",
                "Burpees · 10",
            ],
            "Cardio suave": ["20-30 min caminata o trote suave"],
        },
    },
    "Domingo": {
        "titulo": "🌿 Descanso activo",
        "bloques": {
            "Recuperación": [
                "Caminata 30-45 min",
                "Movilidad suave 15 min",
                "Preparar comidas de la semana (meal prep)",
                "Revisar el plan de la próxima semana",
            ],
        },
    },
}

MOVILIDAD = {
    "🦵 Movilidad para patadas (kicks)": [
        ("Balanceos de pierna frontal y lateral", "2x15 por pierna", "Controlado, sin rebote brusco"),
        ("Estocada profunda (hip flexor)", "45 s por lado", "Glúteo apretado, pelvis neutra"),
        ("Postura 90/90 de cadera", "60 s por lado", "Pecho alto, rota desde la cadera"),
        ("Isquiotibiales con banda (acostado)", "45 s por pierna", "Rodilla estirada, tobillo en flexión"),
        ("Mariposa / aductores", "60 s", "Codos empujan rodillas suave"),
        ("Cossack squat", "2x8 por lado", "Talón apoyado, espalda larga"),
        ("Patada lenta controlada (frontal y lateral)", "2x8 por pierna", "Sube 3 s, mantén 2 s, baja 3 s"),
        ("Estiramiento de pantorrilla / tobillo", "30 s por lado", "Rodilla sobre la punta del pie"),
    ],
    "💪 Movilidad de brazos y hombros": [
        ("Círculos de brazos (adelante/atrás)", "20 cada dirección", "Amplitud progresiva"),
        ("Dislocaciones con banda", "2x12", "Codos estirados, agarre ancho"),
        ("Estiramiento de pecho en marco de puerta", "45 s por lado", "No fuerces el hombro"),
        ("Estiramiento de tríceps sobre la cabeza", "30 s por lado", "Codo apunta al techo"),
        ("Estiramiento cruzado de hombro posterior", "30 s por lado", "Hombro abajo, lejos de la oreja"),
        ("Muñecas y antebrazos (flexión/extensión)", "30 s cada una", "Clave para golpear y anillas"),
        ("Colgado pasivo en anillas", "3x30 s", "Descomprime columna y hombros"),
        ("Rotación torácica en cuadrupedia", "10 por lado", "Sigue la mano con la mirada"),
    ],
}

MANTENIMIENTO = [
    "Limpiar y desinfectar agarres de anillas y mancuernas",
    "Revisar correas, hebillas y punto de anclaje de las anillas",
    "Revisar saco: cadenas, gancho, costuras y relleno",
    "Revisar bandas elásticas (grietas, desgaste, estiramiento)",
    "Lavar vendas y airear/desinfectar guantes",
    "Limpiar piso / colchonetas",
    "Ordenar equipamiento en su lugar",
    "Ventilar el espacio",
    "Reponer botella de agua, toalla y tape/botiquín",
    "Anotar qué equipo hay que reparar o reemplazar",
]

COMIDAS_RAPIDAS = [
    # (nombre, kcal, proteína g) — valores aproximados
    ("Pechuga de pollo 150 g", 248, 46),
    ("3 huevos", 215, 19),
    ("Atún al agua (1 lata)", 120, 26),
    ("Scoop proteína whey", 120, 24),
    ("Yogur proteico", 110, 15),
    ("Avena 50 g", 190, 7),
    ("Arroz cocido 150 g", 195, 4),
    ("Plátano", 105, 1),
    ("Media palta", 120, 2),
    ("Marraqueta", 270, 8),
]

# ─────────────────────────────────────────────
# PERSISTENCIA (archivo JSON)
# ─────────────────────────────────────────────
def cargar_datos() -> dict:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"dias": {}, "semanas": {}}


def guardar_datos() -> None:
    try:
        DATA_FILE.write_text(
            json.dumps(st.session_state.db, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError:
        st.warning("No se pudo guardar el progreso en disco.")


if "db" not in st.session_state:
    st.session_state.db = cargar_datos()

db = st.session_state.db
db.setdefault("dias", {})
db.setdefault("semanas", {})


def datos_dia(fecha: str = HOY_STR) -> dict:
    d = db["dias"].setdefault(fecha, {})
    d.setdefault("comidas", [])
    d.setdefault("movilidad", {})
    d.setdefault("agua", 0)
    return d


def datos_semana() -> dict:
    s = db["semanas"].setdefault(SEMANA_STR, {})
    s.setdefault("entreno", {})
    s.setdefault("mantenimiento", {})
    return s


def casilla(label: str, contenedor: dict, item_id: str, prefijo: str) -> bool:
    """Checkbox que se guarda automáticamente al marcarlo."""
    wkey = f"{prefijo}__{item_id}"

    def _al_cambiar():
        contenedor[item_id] = st.session_state[wkey]
        guardar_datos()

    return st.checkbox(
        label,
        value=contenedor.get(item_id, False),
        key=wkey,
        on_change=_al_cambiar,
    )


def reiniciar(contenedor: dict, prefijo: str) -> None:
    contenedor.clear()
    for k in [k for k in st.session_state if str(k).startswith(prefijo + "__")]:
        del st.session_state[k]
    guardar_datos()


def totales(dia: dict) -> tuple[int, int]:
    kcal = sum(c["kcal"] for c in dia["comidas"])
    prot = sum(c["prot"] for c in dia["comidas"])
    return kcal, prot


# ─────────────────────────────────────────────
# ENCABEZADO + SIDEBAR
# ─────────────────────────────────────────────
dia = datos_dia()
semana = datos_semana()
kcal_hoy, prot_hoy = totales(dia)

st.title("🥊 Centro de Control · Definición")
st.caption(f"{DIA_HOY} {HOY.strftime('%d-%m-%Y')} · Semana {SEMANA_STR}")

with st.sidebar:
    st.header("📋 Resumen de hoy")
    st.write(f"**{DIA_HOY}** — {PLAN_SEMANAL[DIA_HOY]['titulo']}")
    st.metric("Calorías", f"{kcal_hoy} kcal", f"{KCAL_MAX - kcal_hoy} restantes", delta_color="off")
    st.metric("Proteína", f"{prot_hoy} g", f"{max(PROT_MIN - prot_hoy, 0)} g para la meta", delta_color="off")
    st.divider()
    st.subheader("🎯 Metas")
    st.write(f"• Calorías: **{KCAL_MIN:,}–{KCAL_MAX:,} kcal**".replace(",", "."))
    st.write(f"• Proteína: **{PROT_MIN}–{PROT_MAX} g**")
    st.subheader("🏋️ Equipamiento")
    st.write(" · ".join(EQUIPAMIENTO))
    if DIA_HOY in ("Martes", "Jueves"):
        st.info("🥋 Hoy tienes MMA a las 20:00 hrs")
    if ES_VIERNES:
        st.warning("🧹 Hoy toca mantenimiento del espacio")

tab_nutri, tab_entreno, tab_movi, tab_mant = st.tabs(
    ["🍽️ Nutrición", "🏋️ Entrenamiento", "🧘 Movilidad", "🧹 Mantenimiento"]
)

# ─────────────────────────────────────────────
# 1. PANEL DE CALORÍAS Y PROTEÍNAS
# ─────────────────────────────────────────────
with tab_nutri:
    st.subheader("Panel de calorías y proteínas")

    c1, c2 = st.columns(2)
    c1.metric("🔥 Calorías", f"{kcal_hoy} / {KCAL_MAX}", f"{KCAL_MAX - kcal_hoy} kcal restantes", delta_color="off")
    c2.metric("🥩 Proteína", f"{prot_hoy} / {PROT_MAX} g", f"{PROT_MAX - prot_hoy} g restantes", delta_color="off")

    st.progress(min(kcal_hoy / KCAL_MAX, 1.0), text=f"Calorías: {kcal_hoy / KCAL_MAX:.0%}")
    st.progress(min(prot_hoy / PROT_MAX, 1.0), text=f"Proteína: {prot_hoy / PROT_MAX:.0%}")

    # Estado del día
    if kcal_hoy > KCAL_MAX:
        st.error(f"⚠️ Te pasaste por {kcal_hoy - KCAL_MAX} kcal del máximo.")
    elif kcal_hoy >= KCAL_MIN:
        st.success("✅ Calorías dentro del rango objetivo.")
    if PROT_MIN <= prot_hoy <= PROT_MAX:
        st.success("✅ Meta de proteína cumplida.")
    elif prot_hoy > PROT_MAX:
        st.info("💡 Superaste la meta de proteína (no es problema si calzan las calorías).")

    st.markdown("#### ⚡ Suma rápida")
    cols = st.columns(2)
    for i, (nombre, kc, pr) in enumerate(COMIDAS_RAPIDAS):
        if cols[i % 2].button(f"{nombre} · {kc} kcal · {pr} g", key=f"rapida_{i}", use_container_width=True):
            dia["comidas"].append(
                {"nombre": nombre, "kcal": kc, "prot": pr, "hora": datetime.now(TZ).strftime("%H:%M")}
            )
            guardar_datos()
            st.rerun()
    st.caption("Valores aproximados. Ajústalos con el formulario si tu porción es distinta.")

    st.markdown("#### ➕ Agregar comida personalizada")
    with st.form("form_comida", clear_on_submit=True):
        nombre = st.text_input("Comida", placeholder="Ej: Almuerzo pollo + arroz + ensalada")
        f1, f2 = st.columns(2)
        kcal_in = f1.number_input("Calorías (kcal)", min_value=0, max_value=3000, step=10)
        prot_in = f2.number_input("Proteína (g)", min_value=0, max_value=300, step=1)
        if st.form_submit_button("Agregar", use_container_width=True, type="primary"):
            if kcal_in == 0 and prot_in == 0:
                st.warning("Ingresa al menos calorías o proteína.")
            else:
                dia["comidas"].append(
                    {
                        "nombre": nombre.strip() or "Comida",
                        "kcal": int(kcal_in),
                        "prot": int(prot_in),
                        "hora": datetime.now(TZ).strftime("%H:%M"),
                    }
                )
                guardar_datos()
                st.rerun()

    st.markdown("#### 🧾 Registro de hoy")
    if not dia["comidas"]:
        st.info("Aún no registras comidas hoy.")
    else:
        for i, c in enumerate(dia["comidas"]):
            r1, r2 = st.columns([5, 1])
            r1.write(f"`{c['hora']}` **{c['nombre']}** — {c['kcal']} kcal · {c['prot']} g prot")
            if r2.button("🗑️", key=f"borrar_{i}", help="Eliminar"):
                dia["comidas"].pop(i)
                guardar_datos()
                st.rerun()

    st.markdown("#### 💧 Agua")
    a1, a2, a3 = st.columns([2, 1, 1])
    a1.write(f"**{dia['agua']} vasos** (meta: 10 · ~2,5 L)")
    if a2.button("➕ Vaso", use_container_width=True):
        dia["agua"] += 1
        guardar_datos()
        st.rerun()
    if a3.button("➖ Vaso", use_container_width=True) and dia["agua"] > 0:
        dia["agua"] -= 1
        guardar_datos()
        st.rerun()
    st.progress(min(dia["agua"] / 10, 1.0))

    st.markdown("#### 📈 Últimos 7 días")
    filas = []
    for n in range(6, -1, -1):
        f = (HOY - timedelta(days=n)).isoformat()
        d = db["dias"].get(f, {"comidas": []})
        k = sum(c["kcal"] for c in d.get("comidas", []))
        p = sum(c["prot"] for c in d.get("comidas", []))
        filas.append({"Fecha": f[5:], "Calorías": k, "Proteína (g)": p})
    hist = pd.DataFrame(filas).set_index("Fecha")
    st.bar_chart(hist["Calorías"])
    st.bar_chart(hist["Proteína (g)"])

    with st.expander("⚙️ Reiniciar día"):
        if st.button("Borrar todas las comidas de hoy", type="secondary"):
            dia["comidas"].clear()
            dia["agua"] = 0
            guardar_datos()
            st.rerun()

# ─────────────────────────────────────────────
# 2. CHECKLIST DE ENTRENAMIENTO SEMANAL
# ─────────────────────────────────────────────
with tab_entreno:
    st.subheader("Checklist de entrenamiento semanal")
    prefijo_ent = f"ent_{SEMANA_STR}"

    total_items = sum(len(items) for p in PLAN_SEMANAL.values() for items in p["bloques"].values())
    hechos = sum(1 for v in semana["entreno"].values() if v)
    st.progress(hechos / total_items, text=f"Progreso semanal: {hechos}/{total_items} ({hechos / total_items:.0%})")

    for nombre_dia, plan in PLAN_SEMANAL.items():
        es_hoy = nombre_dia == DIA_HOY
        items_dia = [
            f"{nombre_dia}|{bloque}|{item}"
            for bloque, items in plan["bloques"].items()
            for item in items
        ]
        hechos_dia = sum(1 for i in items_dia if semana["entreno"].get(i))
        estado = "✅" if hechos_dia == len(items_dia) else f"{hechos_dia}/{len(items_dia)}"
        etiqueta = f"{'📍 HOY · ' if es_hoy else ''}{nombre_dia} — {plan['titulo']}  [{estado}]"

        with st.expander(etiqueta, expanded=es_hoy):
            for bloque, items in plan["bloques"].items():
                st.markdown(f"**{bloque}**")
                for item in items:
                    casilla(item, semana["entreno"], f"{nombre_dia}|{bloque}|{item}", prefijo_ent)

    with st.expander("⚙️ Reiniciar semana"):
        if st.button("Desmarcar todo el entrenamiento de esta semana"):
            reiniciar(semana["entreno"], prefijo_ent)
            st.rerun()

# ─────────────────────────────────────────────
# 3. MÓDULO DE ELONGACIÓN Y MOVILIDAD
# ─────────────────────────────────────────────
with tab_movi:
    st.subheader("Elongación y movilidad")
    st.caption("Se reinicia cada día. Ideal post-entreno o antes de dormir.")
    prefijo_mov = f"mov_{HOY_STR}"

    total_mov = sum(len(v) for v in MOVILIDAD.values())
    hechos_mov = sum(1 for v in dia["movilidad"].values() if v)
    st.progress(hechos_mov / total_mov, text=f"Movilidad de hoy: {hechos_mov}/{total_mov}")

    for rutina, pasos in MOVILIDAD.items():
        st.markdown(f"### {rutina}")
        for n, (ejercicio, dosis, tip) in enumerate(pasos, start=1):
            casilla(f"**Paso {n}: {ejercicio}** — {dosis}", dia["movilidad"], f"{rutina}|{ejercicio}", prefijo_mov)
            st.caption(f"↳ {tip}")

    if hechos_mov == total_mov:
        st.balloons()
        st.success("🔥 Movilidad completa. Tus patadas te lo van a agradecer.")

    if st.button("Reiniciar movilidad de hoy"):
        reiniciar(dia["movilidad"], prefijo_mov)
        st.rerun()

# ─────────────────────────────────────────────
# 4. CHECKLIST DE MANTENIMIENTO (VIERNES)
# ─────────────────────────────────────────────
with tab_mant:
    st.subheader("Mantenimiento del espacio · Viernes")
    prefijo_man = f"man_{SEMANA_STR}"

    if ES_VIERNES:
        st.warning("🧹 Hoy es viernes: toca mantenimiento.")
    else:
        dias_faltan = (4 - HOY.weekday()) % 7
        st.info(f"Próximo mantenimiento en {dias_faltan} día(s). Puedes adelantar tareas si quieres.")

    hechos_man = sum(1 for v in semana["mantenimiento"].values() if v)
    st.progress(hechos_man / len(MANTENIMIENTO), text=f"{hechos_man}/{len(MANTENIMIENTO)} tareas")

    for tarea in MANTENIMIENTO:
        casilla(tarea, semana["mantenimiento"], tarea, prefijo_man)

    if hechos_man == len(MANTENIMIENTO):
        st.success("✅ Espacio listo para la próxima semana.")

    if st.button("Reiniciar checklist de mantenimiento"):
        reiniciar(semana["mantenimiento"], prefijo_man)
        st.rerun()
