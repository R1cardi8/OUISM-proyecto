<template>
  <div class="page">
    <MiMenu />

    <div class="registro-wrapper">
      <div class="registro-card">

        <div class="brand-header">
          <div>
            <h1 class="brand-name">OUI<span class="brand-dot">.SM</span></h1>
            <p class="brand-tagline">Tu ciudad en tiempo real, tu voz en acción.</p>
          </div>
        </div>

        <div class="divider" />

        <h2 class="form-title">Crear cuenta</h2>
        <p class="form-subtitle">Únete a miles de ciudadanos activos</p>

        <form @submit.prevent="registrarUsuario" class="form" novalidate>

          <div class="input-group" :class="{ focused: focusedField === 'nombre', filled: nuevoUsuario.nombre }">
            <label>Nombre completo</label>
            <div class="input-wrapper">
              <input
                v-model="nuevoUsuario.nombre"
                placeholder="Ej: Sergio García"
                required
                @focus="focusedField = 'nombre'"
                @blur="focusedField = null"
              />
            </div>
          </div>

          <div class="input-group" :class="{ focused: focusedField === 'email', filled: nuevoUsuario.email }">
            <label>Correo electrónico</label>
            <div class="input-wrapper">
              <input
                type="email"
                v-model="nuevoUsuario.email"
                placeholder="correo@email.com"
                required
                @focus="focusedField = 'email'"
                @blur="focusedField = null"
              />
            </div>
          </div>

          <div class="input-group" :class="{ focused: focusedField === 'contrasena', filled: nuevoUsuario.contrasena }">
            <label>Contraseña</label>
            <div class="input-wrapper">
              <input
                :type="mostrarContrasena ? 'text' : 'password'"
                v-model="nuevoUsuario.contrasena"
                placeholder="••••••••"
                required
                @focus="focusedField = 'contrasena'"
                @blur="focusedField = null"
              />
              <button type="button" class="toggle-pass" @click="mostrarContrasena = !mostrarContrasena">
                {{ mostrarContrasena ? 'Ocultar' : 'Ver' }}
              </button>
            </div>
            <div class="password-strength" v-if="nuevoUsuario.contrasena">
              <div
                class="strength-bar"
                :class="passwordStrengthClass"
                :style="{ width: passwordStrengthWidth }"
              ></div>
              <span class="strength-label">{{ passwordStrengthLabel }}</span>
            </div>
          </div>

          <transition name="slide-up">
            <div v-if="error" class="error-pill">{{ error }}</div>
          </transition>

          <button type="submit" class="btn-primary" :disabled="cargando">
            <span v-if="!cargando">Registrarse →</span>
            <span v-else class="spinner"></span>
          </button>

        </form>

        <p class="login-link">
          ¿Ya tienes cuenta?
          <router-link to="/login">Inicia sesión</router-link>
        </p>

        <transition name="toast">
          <div v-if="mostrarToast" class="toast">
            ✅ Usuario registrado correctamente
          </div>
        </transition>

      </div>
    </div>
  </div>
</template>

<script>
import MiMenu           from '@/components/MiMenu.vue'
import incidenteService from '@/services/incidenteService'

export default {
  name: 'RegistroUsuario',
  components: { MiMenu },
  data() {
    return {
      nuevoUsuario: {
        nombre:     '',
        email:      '',
        contrasena: ''
      },
      focusedField:      null,
      mostrarContrasena: false,
      cargando:          false,
      mostrarToast:      false,
      error:             ''
    }
  },
  computed: {
    passwordStrength() {
      const p = this.nuevoUsuario.contrasena
      if (p.length < 4) return 1
      if (p.length < 8) return 2
      if (/[A-Z]/.test(p) && /[0-9]/.test(p)) return 4
      return 3
    },
    passwordStrengthWidth() {
      return ['0%', '25%', '50%', '75%', '100%'][this.passwordStrength]
    },
    passwordStrengthClass() {
      return ['', 'weak', 'fair', 'good', 'strong'][this.passwordStrength]
    },
    passwordStrengthLabel() {
      return ['', 'Débil', 'Regular', 'Buena', 'Fuerte'][this.passwordStrength]
    }
  },
  methods: {
    async registrarUsuario() {
      this.error    = ''
      this.cargando = true
      try {
        await incidenteService.registro({
          nombre:   this.nuevoUsuario.nombre,
          email:    this.nuevoUsuario.email,
          password: this.nuevoUsuario.contrasena
        })
        this.mostrarToast = true
        setTimeout(() => {
          this.mostrarToast = false
          this.$router.push('/login')
        }, 1800)
      } catch (err) {
        this.error = err.response?.data?.error || 'Error al registrar usuario'
      } finally {
        this.cargando = false
      }
    }
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f1f5f9;
  display: flex;
  flex-direction: column;
}

.registro-wrapper {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
}

.registro-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  border: 1px solid #e2e8f0;
  position: relative;
  animation: slideUp 0.4s ease;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.brand-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 1.5rem;
}

.brand-name {
  font-size: 1.4rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  letter-spacing: -0.5px;
}

.brand-dot {
  color: #3b82f6;
}

.brand-tagline {
  font-size: 0.78rem;
  color: #64748b;
  margin: 2px 0 0;
}

.divider {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin-bottom: 1.5rem;
}

.form-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 4px;
}

.form-subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0 0 1.5rem;
}

.input-group {
  margin-bottom: 1rem;
}

.input-group label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
  transition: color 0.2s;
}

.input-group.focused label {
  color: #3b82f6;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  padding: 0 12px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-group.focused .input-wrapper {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.12);
  background: #fff;
}

.input-wrapper input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 11px 0;
  font-size: 0.9rem;
  color: #0f172a;
  outline: none;
}

.input-wrapper input::placeholder {
  color: #94a3b8;
}

.toggle-pass {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.78rem;
  font-weight: 700;
  color: #8890b0;
  padding: 0;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.toggle-pass:hover {
  opacity: 1;
}

.password-strength {
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.strength-bar {
  height: 4px;
  border-radius: 99px;
  transition: width 0.3s, background 0.3s;
}

.strength-bar.weak   { background: #ef4444; }
.strength-bar.fair   { background: #f59e0b; }
.strength-bar.good   { background: #3b82f6; }
.strength-bar.strong { background: #10b981; }

.strength-label {
  font-size: 0.75rem;
  color: #64748b;
}

.error-pill {
  background: #ffe8e8;
  border: 1.5px solid #ffb0b0;
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 0.83rem;
  font-weight: 600;
  color: #cc2c2c;
  text-align: center;
  margin-bottom: 0.5rem;
}

.slide-up-enter-active {
  animation: slide-up-in 0.35s cubic-bezier(.34,1.56,.64,1);
}

@keyframes slide-up-in {
  from { transform: translateY(10px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}

button.btn-primary {
  width: 100%;
  margin-top: 1.25rem;
  padding: 13px;
  border: none;
  border-radius: 10px;
  background: #3b82f6;
  color: white;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

button.btn-primary:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(59,130,246,0.35);
}

button.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2.5px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.login-link {
  text-align: center;
  font-size: 0.85rem;
  color: #64748b;
  margin-top: 1.25rem;
  margin-bottom: 0;
}

.login-link a {
  color: #3b82f6;
  font-weight: 600;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

.toast {
  position: absolute;
  bottom: -60px;
  left: 50%;
  transform: translateX(-50%);
  background: #0f172a;
  color: white;
  padding: 10px 20px;
  border-radius: 99px;
  font-size: 0.85rem;
  font-weight: 500;
  white-space: nowrap;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(10px);
}
</style>