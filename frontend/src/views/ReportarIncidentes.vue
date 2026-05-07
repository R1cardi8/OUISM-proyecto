<template>
  <div class="page">
    <MiMenu />

    <main class="content">

      <!-- HERO -->
      <div class="hero">
        <div class="hero-top">
          <div class="hero-emoji">🚨</div>
          <div class="hero-text">
            <h1>Reportar Incidente</h1>
            <p>Ayuda a mejorar tu ciudad en segundos</p>
          </div>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progreso + '%' }"></div>
        </div>
        <span class="progress-label">{{ camposCompletos }}/6 campos</span>
      </div>

      <!-- FORMULARIO -->
      <form @submit.prevent="reportarIncidente" class="form-card">

        <!-- 1. TÍTULO -->
        <div class="field-block" :class="{ done: incidente.titulo }">
          <div class="field-header">
            <span class="step-num">1</span>
            <label for="titulo">¿Cuál es el problema?</label>
            <transition name="pop">
              <span v-if="incidente.titulo" class="check">✓</span>
            </transition>
          </div>
          <input
            v-model="incidente.titulo"
            id="titulo"
            type="text"
            class="big-input"
            placeholder="Ej: Basura acumulada en la esquina"
            required
            autocomplete="off"
          />
        </div>

        <!-- 2. TIPO -->
        <div class="field-block" :class="{ done: incidente.tipo }">
          <div class="field-header">
            <span class="step-num">2</span>
            <label>¿Qué tipo de incidente?</label>
            <transition name="pop">
              <span v-if="incidente.tipo" class="check">✓</span>
            </transition>
          </div>
          <div class="tipo-grid">
            <button
              v-for="t in tipos"
              :key="t.value"
              type="button"
              :class="['tipo-card', { active: incidente.tipo === t.value }]"
              @click="incidente.tipo = t.value"
            >
              <span class="t-emoji">{{ t.emoji }}</span>
              <span class="t-label">{{ t.label }}</span>
            </button>
          </div>
        </div>

        <!-- 3. DESCRIPCIÓN -->
        <div class="field-block" :class="{ done: incidente.descripcion }">
          <div class="field-header">
            <span class="step-num">3</span>
            <label for="desc">Cuéntanos más detalles</label>
            <transition name="pop">
              <span v-if="incidente.descripcion" class="check">✓</span>
            </transition>
          </div>
          <div class="textarea-wrap">
            <textarea
              v-model="incidente.descripcion"
              id="desc"
              class="big-input big-textarea"
              placeholder="Describe el incidente con todos los detalles que puedas..."
              required
              maxlength="500"
              rows="3"
            ></textarea>
            <span class="char-pill">{{ incidente.descripcion.length }}/500</span>
          </div>
        </div>

        <!-- 4. UBICACIÓN -->
        <div class="field-block" :class="{ done: incidente.ubicacion }">
          <div class="field-header">
            <span class="step-num">4</span>
            <label for="ubicacion">¿Dónde ocurrió?</label>
            <transition name="pop">
              <span v-if="incidente.ubicacion" class="check">✓</span>
            </transition>
          </div>
          <div class="icon-input-wrap">
            <span class="i-icon">📍</span>
            <input
              v-model="incidente.ubicacion"
              id="ubicacion"
              type="text"
              class="big-input with-icon"
              placeholder="Ej: Calle 10 #23-45, Barrio Centro"
              autocomplete="off"
            />
          </div>
        </div>

        <!-- 5. FOTO -->
        <div class="field-block" :class="{ done: fotoPreview }">
          <div class="field-header">
            <span class="step-num">5</span>
            <label>Adjunta una foto <span class="opcional">(opcional)</span></label>
            <transition name="pop">
              <span v-if="fotoPreview" class="check">✓</span>
            </transition>
          </div>
          <div
            class="foto-upload-area"
            :class="{ 'has-foto': fotoPreview }"
            @click="$refs.fotoInput.click()"
          >
            <input
              ref="fotoInput"
              id="foto"
              type="file"
              accept="image/*"
              style="display:none"
              @change="onFotoChange"
            />
            <div v-if="!fotoPreview" class="foto-placeholder">
              <span style="font-size:36px">📷</span>
              <p>Toca para subir una foto</p>
              <span class="foto-hint">Aumenta un 60% la velocidad de respuesta</span>
            </div>
            <div v-else class="foto-preview-wrap">
              <img :src="fotoPreview" class="foto-preview-img" alt="preview" />
              <button type="button" class="foto-remove" @click.stop="quitarFoto">
                ✕ Quitar
              </button>
            </div>
          </div>
        </div>

        <!-- 6. PRIORIDAD -->
        <div class="field-block" :class="{ done: incidente.prioridad }">
          <div class="field-header">
            <span class="step-num">6</span>
            <label>¿Qué tan urgente es?</label>
            <transition name="pop">
              <span v-if="incidente.prioridad" class="check">✓</span>
            </transition>
          </div>
          <div class="prioridad-grid">
            <button
              v-for="p in prioridades"
              :key="p.value"
              type="button"
              :class="['p-card', `p-${p.value}`, { active: incidente.prioridad === p.value }]"
              @click="incidente.prioridad = p.value"
            >
              <span class="p-emoji">{{ p.emoji }}</span>
              <span class="p-label">{{ p.label }}</span>
              <span class="p-desc">{{ p.desc }}</span>
            </button>
          </div>
        </div>

        <!-- SUBMIT -->
        <button
          type="submit"
          class="submit-btn"
          :class="{ ready: formValido }"
          :disabled="!formValido"
        >
          <span v-if="!enviando">📤 &nbsp;Reportar Incidente</span>
          <span v-else class="dots">
            <span></span><span></span><span></span>
          </span>
        </button>

      </form>

      <!-- TOAST -->
      <transition name="slide-up">
        <div v-if="mostrarToast" class="toast">
          🎉 &nbsp;<strong>¡Reporte enviado!</strong> &nbsp;Gracias por ayudar a mejorar tu ciudad.
        </div>
      </transition>

      <!-- LISTA DE REPORTES -->
      <div v-if="incidentes.length > 0" class="list-section">
        <div class="list-header">
          <h2>Reportes recientes</h2>
          <span class="count-badge">{{ incidentes.length }}</span>
        </div>

        <!-- LISTA VERTICAL -->
        <div class="inc-list">
          <div v-for="inc in incidentes" :key="inc.id" class="inc-card">
            <div class="inc-top">
              <span class="inc-emoji">{{ tipoEmoji(inc.tipo) }}</span>
              <span :class="['inc-badge', inc.prioridad]">{{ inc.prioridad }}</span>
            </div>
            <h3 class="inc-titulo">{{ inc.titulo }}</h3>
            <p class="inc-desc">{{ inc.descripcion }}</p>
            <img v-if="inc.foto" :src="inc.foto" class="inc-foto" alt="foto del reporte" />
            <div class="inc-footer">
              <span v-if="inc.ubicacion" class="inc-loc">📍 {{ inc.ubicacion }}</span>
              <span class="inc-fecha">{{ inc.fecha }}</span>
            </div>
          </div>
        </div>

      </div>

    </main>
  </div>
</template>

<script>
import MiMenu from '@/components/MiMenu.vue'
import incidenteService from '@/services/incidenteService'

export default {
  name: 'ReportarIncidentes',
  components: { MiMenu },
  data() {
    return {
      incidente: {
        titulo: '',
        descripcion: '',
        tipo: '',
        ubicacion: '',
        prioridad: ''
      },
      fotoPreview: null,
      incidentes: [],
      enviando: false,
      mostrarToast: false,
      tipos: [
        { value: 'técnico',        emoji: '🚧', label: 'Técnico'        },
        { value: 'médico',         emoji: '🏥', label: 'Médico'         },
        { value: 'administrativo', emoji: '📋', label: 'Administrativo' },
        { value: 'seguridad',      emoji: '🚔', label: 'Seguridad'      },
        { value: 'ambiental',      emoji: '🌿', label: 'Ambiental'      },
        { value: 'otro',           emoji: '❓', label: 'Otro'           },
      ],
      prioridades: [
        { value: 'baja',    emoji: '🟢', label: 'Baja',    desc: 'No es urgente'   },
        { value: 'media',   emoji: '🟡', label: 'Media',   desc: 'Atención pronto' },
        { value: 'alta',    emoji: '🟠', label: 'Alta',    desc: 'Requiere acción' },
        { value: 'urgente', emoji: '🔴', label: 'Urgente', desc: '¡Atención ya!'   },
      ]
    }
  },
  computed: {
    camposCompletos() {
      const i = this.incidente
      return [i.titulo, i.tipo, i.descripcion, i.ubicacion, i.prioridad, this.fotoPreview]
        .filter(v => v && String(v).trim()).length
    },
    progreso() {
      return (this.camposCompletos / 6) * 100
    },
    formValido() {
      const i = this.incidente
      return !!(i.titulo && i.tipo && i.descripcion && i.prioridad)
    }
  },
  mounted() {
    this.cargarIncidentes()
    const hint = this.$route.query.hint
    if (hint === 'urgente') {
      this.incidente.prioridad = 'urgente'
    }
    this.$nextTick(() => {
      if (hint === 'ubicacion') {
        const el = document.getElementById('ubicacion')
        if (el) { el.focus(); el.scrollIntoView({ behavior: 'smooth', block: 'center' }) }
      }
      if (hint === 'foto') {
        this.$refs.fotoInput?.click()
        this.$refs.fotoInput?.scrollIntoView?.({ behavior: 'smooth', block: 'center' })
      }
    })
  },
  methods: {
    tipoEmoji(tipo) {
      const t = this.tipos.find(x => x.value === tipo)
      return t ? t.emoji : '📌'
    },
    onFotoChange(e) {
      const file = e.target.files[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = (ev) => { this.fotoPreview = ev.target.result }
      reader.readAsDataURL(file)
    },
    quitarFoto() {
      this.fotoPreview = null
      this.$refs.fotoInput.value = ''
    },
    async reportarIncidente() {
      if (!this.formValido) return
      this.enviando = true
      try {
        const payload = {
          usuario_id:  parseInt(localStorage.getItem('usuarioId')),
          titulo:      this.incidente.titulo,
          descripcion: this.incidente.descripcion,
          tipo:        this.incidente.tipo,
          ubicacion:   this.incidente.ubicacion,
          prioridad:   this.incidente.prioridad,
          foto:        this.fotoPreview || null
        }
        const { data } = await incidenteService.createIncidente(payload)
        this.incidentes.unshift({
          id:          data.id,
          titulo:      payload.titulo,
          descripcion: payload.descripcion,
          tipo:        payload.tipo,
          ubicacion:   payload.ubicacion,
          prioridad:   payload.prioridad,
          foto:        payload.foto,
          fecha:       new Date().toLocaleString()
        })
        this.incidente   = { titulo: '', descripcion: '', tipo: '', ubicacion: '', prioridad: '' }
        this.fotoPreview = null
        this.mostrarToast = true
        setTimeout(() => { this.mostrarToast = false }, 3500)
      } catch (err) {
        alert('Error al enviar el reporte: ' + (err.response?.data?.error || err.message))
      } finally {
        this.enviando = false
      }
    },
    cargarIncidentes() {
      incidenteService.getIncidentes()
        .then(({ data }) => { this.incidentes = data })
        .catch(() => {})
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

* {
  box-sizing: border-box;
}

/* ── PAGE ── */
.page {
  min-height: 100vh;
  background: #f0f4ff;
  font-family: 'Nunito', sans-serif;
}

.content {
  max-width: 700px;
  margin: 0 auto;
  padding: 32px 20px 80px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ── HERO ── */
.hero {
  background: #fff;
  border-radius: 24px;
  padding: 24px 28px;
  box-shadow: 0 4px 0 #d4d9f0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hero-top {
  display: flex;
  align-items: center;
  gap: 16px;
}

.hero-emoji {
  font-size: 42px;
  line-height: 1;
}

.hero-text h1 {
  font-size: 22px;
  font-weight: 900;
  color: #1a1a2e;
  margin: 0 0 2px;
}

.hero-text p {
  font-size: 13px;
  color: #8890b0;
  margin: 0;
  font-weight: 600;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background: #e8eaf6;
  border-radius: 99px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #58cc02, #89e219);
  border-radius: 99px;
  transition: width 0.5s cubic-bezier(.34,1.56,.64,1);
}

.progress-label {
  font-size: 11px;
  font-weight: 700;
  color: #58cc02;
  letter-spacing: .5px;
  text-align: right;
}

/* ── FORM CARD ── */
.form-card {
  background: #fff;
  border-radius: 24px;
  padding: 32px 28px;
  box-shadow: 0 4px 0 #d4d9f0;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

/* ── FIELD BLOCK ── */
.field-block {
  border: 2px solid #e8eaf6;
  border-radius: 18px;
  padding: 20px 20px 18px;
  transition: border-color 0.25s, box-shadow 0.25s;
}

.field-block:focus-within {
  border-color: #84b0ff;
  box-shadow: 0 0 0 4px rgba(132,176,255,0.15);
}

.field-block.done {
  border-color: #58cc02;
  background: #f8fff0;
}

.field-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.step-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e8eaf6;
  color: #6670a0;
  font-size: 13px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.2s, color 0.2s;
}

.field-block.done .step-num {
  background: #58cc02;
  color: #fff;
}

label {
  font-size: 15px;
  font-weight: 800;
  color: #1a1a2e;
  flex: 1;
}

.opcional {
  font-size: 12px;
  font-weight: 600;
  color: #b0b8d8;
}

.check {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #58cc02;
  color: #fff;
  font-size: 14px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.pop-enter-active {
  animation: pop-in 0.35s cubic-bezier(.34,1.56,.64,1);
}

@keyframes pop-in {
  from { transform: scale(0); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}

/* ── INPUTS ── */
.big-input {
  width: 100%;
  background: #f4f6ff;
  border: 2px solid #e0e4f5;
  border-radius: 14px;
  color: #1a1a2e;
  font-family: 'Nunito', sans-serif;
  font-size: 15px;
  font-weight: 600;
  padding: 14px 16px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  appearance: none;
}

.big-input::placeholder {
  color: #b0b8d8;
}

.big-input:focus {
  border-color: #84b0ff;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(132,176,255,0.2);
}

.big-textarea {
  resize: none;
  line-height: 1.6;
}

.textarea-wrap {
  position: relative;
}

.char-pill {
  position: absolute;
  bottom: 10px;
  right: 12px;
  font-size: 11px;
  font-weight: 700;
  color: #b0b8d8;
  background: #eef0fa;
  border-radius: 99px;
  padding: 2px 8px;
  pointer-events: none;
}

/* ── ICON INPUT ── */
.icon-input-wrap {
  position: relative;
}

.i-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  pointer-events: none;
  line-height: 1;
}

.with-icon {
  padding-left: 44px;
}

/* ── FOTO UPLOAD ── */
.foto-upload-area {
  border: 2px dashed #c8d0f0;
  border-radius: 16px;
  padding: 24px 16px;
  cursor: pointer;
  text-align: center;
  background: #f4f6ff;
  transition: border-color 0.2s, background 0.2s;
  user-select: none;
}

.foto-upload-area:hover {
  border-color: #84b0ff;
  background: #eef2ff;
}

.foto-upload-area.has-foto {
  border-color: #58cc02;
  background: #f8fff0;
  border-style: solid;
}

.foto-placeholder p {
  font-size: 14px;
  font-weight: 700;
  color: #6670a0;
  margin: 8px 0 4px;
}

.foto-hint {
  font-size: 11px;
  font-weight: 600;
  color: #b0b8d8;
}

.foto-preview-wrap {
  position: relative;
  display: inline-block;
}

.foto-preview-img {
  max-height: 200px;
  max-width: 100%;
  border-radius: 12px;
  object-fit: cover;
  display: block;
}

.foto-remove {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0,0,0,0.55);
  color: #fff;
  border: none;
  border-radius: 99px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  font-family: 'Nunito', sans-serif;
}

.foto-remove:hover {
  background: rgba(200,0,0,0.75);
}

/* ── TIPO GRID ── */
.tipo-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.tipo-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 14px 8px;
  border: 2px solid #e0e4f5;
  border-radius: 16px;
  background: #f4f6ff;
  cursor: pointer;
  transition: all 0.18s cubic-bezier(.34,1.56,.64,1);
  font-family: 'Nunito', sans-serif;
}

.tipo-card:hover {
  border-color: #84b0ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(132,176,255,0.2);
}

.tipo-card.active {
  border-color: #1cb0f6;
  background: #e8f7ff;
  transform: scale(1.05);
  box-shadow: 0 4px 0 #1a9fd4;
}

.t-emoji {
  font-size: 26px;
  line-height: 1;
}

.t-label {
  font-size: 12px;
  font-weight: 800;
  color: #4a5080;
}

.tipo-card.active .t-label {
  color: #1cb0f6;
}

/* ── PRIORIDAD GRID ── */
.prioridad-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.p-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 14px 6px;
  border: 2px solid #e0e4f5;
  border-radius: 16px;
  background: #f4f6ff;
  cursor: pointer;
  transition: all 0.18s cubic-bezier(.34,1.56,.64,1);
  font-family: 'Nunito', sans-serif;
}

.p-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.p-emoji {
  font-size: 22px;
  line-height: 1;
}

.p-label {
  font-size: 13px;
  font-weight: 800;
  color: #1a1a2e;
}

.p-desc {
  font-size: 10px;
  font-weight: 600;
  color: #8890b0;
  text-align: center;
}

.p-card.p-baja.active {
  border-color: #58cc02;
  background: #f0ffe8;
  box-shadow: 0 4px 0 #3da800;
}

.p-card.p-media.active {
  border-color: #ffc800;
  background: #fffbe8;
  box-shadow: 0 4px 0 #d4a600;
}

.p-card.p-alta.active {
  border-color: #ff9600;
  background: #fff4e8;
  box-shadow: 0 4px 0 #d47c00;
}

.p-card.p-urgente.active {
  border-color: #ff4b4b;
  background: #fff0f0;
  box-shadow: 0 4px 0 #cc2c2c;
}

.p-card.p-baja.active    .p-label { color: #3da800; }
.p-card.p-media.active   .p-label { color: #d4a600; }
.p-card.p-alta.active    .p-label { color: #d47c00; }
.p-card.p-urgente.active .p-label { color: #cc2c2c; }

/* ── SUBMIT ── */
.submit-btn {
  width: 100%;
  padding: 18px;
  border: none;
  border-radius: 16px;
  background: #e0e4f5;
  color: #a0a8c8;
  font-family: 'Nunito', sans-serif;
  font-size: 17px;
  font-weight: 900;
  cursor: not-allowed;
  transition: all 0.25s;
  letter-spacing: 0.3px;
  box-shadow: 0 4px 0 #c8ccdf;
}

.submit-btn.ready {
  background: linear-gradient(135deg, #58cc02, #89e219);
  color: #fff;
  cursor: pointer;
  box-shadow: 0 6px 0 #3da800;
}

.submit-btn.ready:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 0 #3da800;
}

.submit-btn.ready:active {
  transform: translateY(3px);
  box-shadow: 0 2px 0 #3da800;
}

.submit-btn:disabled {
  transform: none !important;
}

/* ── DOTS LOADER ── */
.dots {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #fff;
  animation: bounce-dot 0.8s infinite;
}

.dots span:nth-child(2) { animation-delay: 0.15s; }
.dots span:nth-child(3) { animation-delay: 0.30s; }

@keyframes bounce-dot {
  0%, 80%, 100% { transform: scale(0.7); opacity: .5; }
  40%           { transform: scale(1.1); opacity: 1;  }
}

/* ── TOAST ── */
.toast {
  position: fixed;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  background: #1a1a2e;
  color: #fff;
  font-family: 'Nunito', sans-serif;
  font-size: 14px;
  font-weight: 700;
  padding: 14px 28px;
  border-radius: 99px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.25);
  white-space: nowrap;
  z-index: 999;
}

.slide-up-enter-active {
  animation: slide-up-in 0.4s cubic-bezier(.34,1.56,.64,1);
}

.slide-up-leave-active {
  animation: slide-up-in 0.25s reverse ease-in;
}

@keyframes slide-up-in {
  from { transform: translateX(-50%) translateY(30px); opacity: 0; }
  to   { transform: translateX(-50%) translateY(0);    opacity: 1; }
}

/* ── LISTA REPORTES ── */
.list-section {
  margin-top: 16px;
}

.list-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
}

.list-header h2 {
  font-size: 20px;
  font-weight: 900;
  color: #1a1a2e;
  margin: 0;
}

.count-badge {
  background: #1cb0f6;
  color: #fff;
  font-size: 12px;
  font-weight: 800;
  border-radius: 99px;
  padding: 2px 10px;
}

/* ── LISTA VERTICAL ── */
.inc-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.inc-card {
  background: #fff;
  border: 2px solid #e8eaf6;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 0 #d4d9f0;
  transition: transform 0.2s, box-shadow 0.2s;
}

.inc-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 0 #d4d9f0;
}

.inc-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.inc-emoji {
  font-size: 28px;
  line-height: 1;
}

.inc-badge {
  font-size: 11px;
  font-weight: 800;
  border-radius: 99px;
  padding: 3px 12px;
  text-transform: uppercase;
  letter-spacing: .5px;
}

.inc-badge.baja    { background: #e8ffe0; color: #3da800; }
.inc-badge.media   { background: #fff8d6; color: #b08800; }
.inc-badge.alta    { background: #fff0e0; color: #c46000; }
.inc-badge.urgente { background: #ffe8e8; color: #cc2c2c; }

.inc-titulo {
  font-size: 15px;
  font-weight: 800;
  color: #1a1a2e;
  margin: 0 0 6px;
}

.inc-desc {
  font-size: 13px;
  color: #6670a0;
  font-weight: 600;
  line-height: 1.5;
  margin: 0 0 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.inc-foto {
  width: 100%;
  max-height: 180px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 12px;
}

.inc-footer {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.inc-loc {
  font-size: 12px;
  font-weight: 700;
  color: #8890b0;
}

.inc-fecha {
  font-size: 11px;
  font-weight: 600;
  color: #b0b8d8;
}

/* ── RESPONSIVE ── */
@media (max-width: 580px) {
  .form-card        { padding: 24px 16px; }
  .tipo-grid        { grid-template-columns: repeat(2, 1fr); }
  .prioridad-grid   { grid-template-columns: repeat(2, 1fr); }
  .hero             { padding: 20px; }
}
</style>