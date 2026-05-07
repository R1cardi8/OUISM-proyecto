<template>
  <div class="page">
    <MiMenu />
    <main class="content">

      <div class="hero">
        <div class="hero-text">
          <h1>Bienvenido de nuevo</h1>
          <p>Inicia sesión para continuar</p>
        </div>
      </div>

      <div class="form-card">

        <div class="field-block" :class="{ done: email }">
          <div class="field-header">
            <span class="step-num">1</span>
            <label for="email">Email</label>
            <transition name="pop"><span v-if="email" class="check">✓</span></transition>
          </div>
          <div class="icon-input-wrap">
            <input
              v-model="email"
              id="email"
              type="email"
              class="big-input"
              placeholder="Ingresa tu email"
              required
              autocomplete="off"
            />
          </div>
        </div>

        <div class="field-block" :class="{ done: contrasena }">
          <div class="field-header">
            <span class="step-num">2</span>
            <label for="contrasena">Contraseña</label>
            <transition name="pop"><span v-if="contrasena" class="check">✓</span></transition>
          </div>
          <div class="icon-input-wrap">
            <input
              v-model="contrasena"
              id="contrasena"
              :type="verContrasena ? 'text' : 'password'"
              class="big-input with-icon-right"
              placeholder="••••••••"
              required
            />
            <button type="button" class="toggle-pass" @click="verContrasena = !verContrasena">
              {{ verContrasena ? 'Ocultar' : 'Ver' }}
            </button>
          </div>
        </div>

        <transition name="slide-up">
          <div v-if="error" class="error-pill">{{ error }}</div>
        </transition>

        <button
          class="submit-btn"
          :class="{ ready: email && contrasena }"
          :disabled="!email || !contrasena || cargando"
          @click="login"
        >
          <span v-if="!cargando">Ingresar</span>
          <span v-else class="dots"><span></span><span></span><span></span></span>
        </button>

        <div class="links">
          <router-link to="/" class="link-ghost">← Volver</router-link>
          <router-link to="/registro" class="link-main">Crear cuenta →</router-link>
        </div>

      </div>

    </main>
  </div>
</template>

<script>
import MiMenu           from '@/components/MiMenu.vue'
import incidenteService from '@/services/incidenteService'

export default {
  name: 'IniciodeSesion',
  components: { MiMenu },
  data() {
    return {
      email:         '',
      contrasena:    '',
      verContrasena: false,
      error:         '',
      cargando:      false
    }
  },
  methods: {
    async login() {
      this.error    = ''
      this.cargando = true
      try {
        const { data } = await incidenteService.login({
          email:    this.email,
          password: this.contrasena
        })
        localStorage.setItem('usuario', data.nombre)
        localStorage.setItem('usuarioId', data.id)
        this.$router.push('/')
      } catch (err) {
        this.error = err.response?.data?.error || 'Error al iniciar sesión'
      } finally {
        this.cargando = false
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

* {
  box-sizing: border-box;
}

.page {
  min-height: 100vh;
  background: #f0f4ff;
  font-family: 'Nunito', sans-serif;
}

.content {
  max-width: 480px;
  margin: 0 auto;
  padding: 32px 20px 80px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.hero {
  background: #fff;
  border-radius: 24px;
  padding: 24px 28px;
  box-shadow: 0 4px 0 #d4d9f0;
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

.form-card {
  background: #fff;
  border-radius: 24px;
  padding: 32px 28px;
  box-shadow: 0 4px 0 #d4d9f0;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

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

.icon-input-wrap {
  position: relative;
}

.toggle-pass {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 12px;
  font-weight: 700;
  color: #8890b0;
  font-family: 'Nunito', sans-serif;
  padding: 0;
}

.toggle-pass:hover {
  color: #1a1a2e;
}

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

.with-icon-right {
  padding-right: 64px;
}

.error-pill {
  background: #ffe8e8;
  border: 2px solid #ffb0b0;
  border-radius: 14px;
  padding: 12px 16px;
  font-size: 13px;
  font-weight: 700;
  color: #cc2c2c;
  text-align: center;
}

.slide-up-enter-active {
  animation: slide-up-in 0.35s cubic-bezier(.34,1.56,.64,1);
}

@keyframes slide-up-in {
  from { transform: translateY(10px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}

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
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: #fff;
  cursor: pointer;
  box-shadow: 0 6px 0 #1a3fb8;
}

.submit-btn.ready:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 0 #1a3fb8;
}

.submit-btn.ready:active {
  transform: translateY(3px);
  box-shadow: 0 2px 0 #1a3fb8;
}

.submit-btn:disabled {
  transform: none !important;
}

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

.links {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 4px;
}

.link-ghost {
  font-size: 13px;
  font-weight: 700;
  color: #8890b0;
  text-decoration: none;
}

.link-ghost:hover {
  color: #1a1a2e;
}

.link-main {
  font-size: 13px;
  font-weight: 900;
  color: #1cb0f6;
  text-decoration: none;
  border-bottom: 2px solid #1cb0f6;
  padding-bottom: 1px;
}

.link-main:hover {
  opacity: 0.7;
}

@media (max-width: 580px) {
  .form-card { padding: 24px 16px; }
  .hero      { padding: 20px; }
}
</style>