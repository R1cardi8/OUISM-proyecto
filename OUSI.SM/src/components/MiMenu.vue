<template>
  <nav :class="['navbar', { scrolled }]">

    <div class="light-border">
      <span class="lb-top"></span>
      <span class="lb-right"></span>
      <span class="lb-bottom"></span>
      <span class="lb-left"></span>
    </div>

    <router-link to="/" class="logo">
      <div class="logo-icon">
        <img src="@/assets/basura.png" alt="Logo" />
        <div class="logo-ring"></div>
      </div>
      <div class="logo-text">
        <span class="logo-name">OUI<em>.SM</em></span>
        <span class="logo-sub" :class="{ hidden: scrolled }">Tu ciudad en tiempo real</span>
      </div>
    </router-link>

    <ul class="nav-links">
      <li>
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
          <svg viewBox="0 0 20 20" fill="currentColor" width="14"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7A1 1 0 003 11h1v6a1 1 0 001 1h4v-4h2v4h4a1 1 0 001-1v-6h1a1 1 0 00.707-1.707l-7-7z"/></svg>
          Inicio
        </router-link>
      </li>
      <li v-if="usuario">
        <router-link to="/reportar-incidentes" class="nav-cta">
          <span class="cta-dot"></span>
          <svg viewBox="0 0 20 20" fill="currentColor" width="14"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
          Reportar
        </router-link>
      </li>
    </ul>

    <div class="nav-auth">

      <template v-if="!usuario">
        <router-link to="/login" class="btn-ghost">Iniciar sesión</router-link>
        <router-link to="/registro" class="btn-outline">
          Registrarse
          <svg viewBox="0 0 20 20" fill="currentColor" width="12"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
        </router-link>
      </template>

      <template v-else>
        <div class="user-chip" @click="dropOpen = !dropOpen" ref="chipRef">
          <div class="chip-avatar">{{ usuario.charAt(0).toUpperCase() }}</div>
          <span class="chip-name" :class="{ hidden: scrolled }">{{ usuario }}</span>
          <svg class="chip-chevron" :class="{ flipped: dropOpen }" viewBox="0 0 20 20" fill="currentColor" width="13">
            <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd"/>
          </svg>

          <transition name="drop">
            <div class="user-drop" v-if="dropOpen">
              <div class="drop-head">
                <div class="drop-avatar">{{ usuario.charAt(0).toUpperCase() }}</div>
                <div class="drop-info">
                  <strong>{{ usuario }}</strong>
                  <span>Ciudadano activo</span>
                </div>
              </div>
              <div class="drop-sep"></div>
              <router-link to="/" class="drop-item" @click="dropOpen = false">
                <svg viewBox="0 0 20 20" fill="currentColor" width="15"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7A1 1 0 003 11h1v6a1 1 0 001 1h4v-4h2v4h4a1 1 0 001-1v-6h1a1 1 0 00.707-1.707l-7-7z"/></svg>
                Inicio
              </router-link>
              <router-link to="/reportar-incidentes" class="drop-item" @click="dropOpen = false">
                <svg viewBox="0 0 20 20" fill="currentColor" width="15"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92z" clip-rule="evenodd"/></svg>
                Mis reportes
              </router-link>
              <div class="drop-sep"></div>
              <button class="drop-item danger" @click="cerrarSesion">
                <svg viewBox="0 0 20 20" fill="currentColor" width="15"><path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 001 1h8a1 1 0 100-2H4V5h7a1 1 0 100-2H3zm11.707 4.293a1 1 0 00-1.414 1.414L14.586 10l-1.293 1.293a1 1 0 101.414 1.414l2-2a1 1 0 000-1.414l-2-2z" clip-rule="evenodd"/></svg>
                Cerrar sesión
              </button>
            </div>
          </transition>
        </div>
      </template>

    </div>
  </nav>
</template>

<script>
export default {
  name: "MiMenu",
  data() {
    return {
      usuario: localStorage.getItem("usuario") || null,
      scrolled: false,
      dropOpen: false,
    };
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
    document.addEventListener("click", this.handleOutside);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
    document.removeEventListener("click", this.handleOutside);
  },
  methods: {
    handleScroll() {
      this.scrolled = window.scrollY > 30;
    },
    handleOutside(e) {
      if (this.$refs.chipRef && !this.$refs.chipRef.contains(e.target)) {
        this.dropOpen = false;
      }
    },
    cerrarSesion() {
      localStorage.removeItem("usuario");
      this.usuario = null;
      this.dropOpen = false;
      this.$router.push("/");
    },
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

.navbar {
  font-family: 'Outfit', sans-serif;
  position: sticky;
  top: 12px;
  margin: 12px 20px 0;
  height: 66px;
  padding: 0 1.6rem;
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  background: rgba(22, 30, 46, 0.92);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 18px;
  color: #e2e8f0;
  box-shadow: 0 2px 20px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.06);
  transition: height 0.4s cubic-bezier(.34,1.2,.64,1), margin 0.4s cubic-bezier(.34,1.2,.64,1), border-radius 0.4s ease, box-shadow 0.4s ease;
}

.navbar.scrolled {
  height: 50px;
  margin: 8px 56px 0;
  border-radius: 99px;
  background: rgba(10, 15, 28, 0.96);
  box-shadow: 0 8px 36px rgba(0,0,0,0.5), 0 0 0 1px rgba(56,189,248,0.12), 0 0 28px rgba(56,189,248,0.06), inset 0 1px 0 rgba(255,255,255,0.05);
}

.light-border { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; opacity: 0; transition: opacity 0.5s ease; }
.navbar.scrolled .light-border { opacity: 1; }
.light-border span { position: absolute; display: block; }
.lb-top    { top: 0; left: -100%; width: 100%; height: 1px; background: linear-gradient(90deg, transparent, #38bdf8 40%, #4ade80 60%, transparent); animation: run-h 2.8s linear infinite; }
.lb-bottom { bottom: 0; right: -100%; width: 100%; height: 1px; background: linear-gradient(90deg, transparent, #a78bfa 40%, #38bdf8 60%, transparent); animation: run-h 2.8s linear infinite reverse; animation-delay: -1.4s; }
.lb-right  { right: 0; top: -100%; width: 1px; height: 100%; background: linear-gradient(180deg, transparent, #4ade80, transparent); animation: run-v 2.8s linear infinite; animation-delay: -0.7s; }
.lb-left   { left: 0; bottom: -100%; width: 1px; height: 100%; background: linear-gradient(180deg, transparent, #a78bfa, transparent); animation: run-v 2.8s linear infinite reverse; animation-delay: -2.1s; }

@keyframes run-h { from { left: -100%; } to { left: 100%; } }
@keyframes run-v { from { top: -100%; } to { top: 100%; } }

.logo { display: flex; align-items: center; gap: 10px; text-decoration: none; flex-shrink: 0; }
.logo-icon { position: relative; width: 38px; height: 38px; flex-shrink: 0; transition: transform 0.35s cubic-bezier(.34,1.4,.64,1); }
.logo:hover .logo-icon { transform: rotate(-8deg) scale(1.08); }
.logo-icon img { width: 100%; object-fit: contain; border-radius: 10px; display: block; filter: drop-shadow(0 0 6px rgba(74,222,128,0.35)); }
.navbar.scrolled .logo-icon { width: 30px; height: 30px; }
.logo-ring { position: absolute; inset: -3px; border-radius: 50%; border: 1.5px dashed rgba(74,222,128,0.3); animation: spin 8s linear infinite; opacity: 0; transition: opacity 0.3s; }
.logo:hover .logo-ring { opacity: 1; }

@keyframes spin { to { transform: rotate(360deg); } }

.logo-text { display: flex; flex-direction: column; line-height: 1.1; overflow: hidden; }
.logo-name { font-size: 1.2rem; font-weight: 800; color: #fff; letter-spacing: -0.3px; transition: font-size 0.35s ease; }
.logo-name em { font-style: normal; color: #4ade80; }
.navbar.scrolled .logo-name { font-size: 1rem; }
.logo-sub { font-size: 0.62rem; color: rgba(255,255,255,0.45); max-height: 20px; overflow: hidden; transition: max-height 0.35s ease, opacity 0.25s ease; }
.logo-sub.hidden { max-height: 0; opacity: 0; }

.nav-links { display: flex; align-items: center; gap: 4px; list-style: none; margin: 0; padding: 0; }
.nav-link { position: relative; display: inline-flex; align-items: center; gap: 6px; padding: 7px 13px; border-radius: 10px; text-decoration: none; color: rgba(255,255,255,0.5); font-size: 0.875rem; font-weight: 500; transition: color 0.2s, background 0.2s, border 0.2s; border: 1px solid transparent; }
.nav-link::after { content: ''; position: absolute; bottom: 5px; left: 50%; transform: translateX(-50%) scaleX(0); width: 16px; height: 2px; background: #4ade80; border-radius: 2px; transition: transform 0.25s cubic-bezier(.34,1.4,.64,1); }
.nav-link:hover { color: #fff; background: rgba(255,255,255,0.06); }
.nav-link:hover::after { transform: translateX(-50%) scaleX(1); }
.nav-link.active { color: #4ade80; background: rgba(74,222,128,0.08); border-color: rgba(74,222,128,0.15); }
.nav-link.active::after { transform: translateX(-50%) scaleX(1); }

.nav-cta { position: relative; display: inline-flex; align-items: center; gap: 7px; padding: 8px 18px; border-radius: 10px; text-decoration: none; color: #fff; font-size: 0.875rem; font-weight: 700; background: linear-gradient(135deg, #1d4ed8, #3b82f6); box-shadow: 0 4px 18px rgba(37,99,235,0.4); overflow: hidden; transition: transform 0.22s cubic-bezier(.34,1.4,.64,1), box-shadow 0.22s, border-radius 0.35s; }
.nav-cta::before { content: ''; position: absolute; inset: 0; background: linear-gradient(135deg, rgba(255,255,255,0.12), transparent); opacity: 0; transition: opacity 0.2s; }
.nav-cta:hover::before { opacity: 1; }
.nav-cta:hover { transform: translateY(-2px) scale(1.03); box-shadow: 0 8px 28px rgba(37,99,235,0.55); }
.nav-cta:active { transform: translateY(0) scale(0.98); }
.navbar.scrolled .nav-cta { border-radius: 99px; padding: 5px 15px; }
.cta-dot { width: 7px; height: 7px; background: #93c5fd; border-radius: 50%; flex-shrink: 0; animation: cta-pulse 1.6s ease-in-out infinite; }

@keyframes cta-pulse { 0%,100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.7); opacity: 0.5; } }

.nav-auth { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.btn-ghost { text-decoration: none; color: rgba(255,255,255,0.5); font-size: 0.85rem; font-weight: 500; padding: 7px 12px; border-radius: 9px; transition: color 0.2s, background 0.2s; }
.btn-ghost:hover { color: #fff; background: rgba(255,255,255,0.07); }
.btn-outline { display: inline-flex; align-items: center; gap: 6px; text-decoration: none; color: #e2e8f0; font-size: 0.85rem; font-weight: 600; padding: 7px 14px; border-radius: 9px; border: 1px solid rgba(255,255,255,0.18); background: rgba(255,255,255,0.04); transition: all 0.22s; }
.btn-outline:hover { color: #fff; border-color: rgba(255,255,255,0.4); background: rgba(255,255,255,0.09); transform: translateY(-1px); }

.user-chip { position: relative; display: flex; align-items: center; gap: 8px; padding: 5px 10px 5px 5px; border-radius: 99px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); cursor: pointer; transition: background 0.2s, border-color 0.2s, box-shadow 0.2s; user-select: none; }
.user-chip:hover { background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.22); box-shadow: 0 4px 16px rgba(0,0,0,0.3); }
.chip-avatar { width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, #16a34a, #4ade80); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.78rem; color: #022c22; flex-shrink: 0; box-shadow: 0 0 10px rgba(74,222,128,0.3); }
.chip-name { font-size: 0.85rem; font-weight: 600; color: #e2e8f0; max-width: 120px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; transition: max-width 0.3s ease, opacity 0.25s ease; }
.chip-name.hidden { max-width: 0; opacity: 0; }
.chip-chevron { color: rgba(255,255,255,0.4); flex-shrink: 0; transition: transform 0.25s cubic-bezier(.34,1.4,.64,1), color 0.2s; }
.chip-chevron.flipped { transform: rotate(180deg); color: #e2e8f0; }

.user-drop { position: absolute; top: calc(100% + 12px); right: 0; width: 230px; background: #141b2d; border: 1px solid rgba(255,255,255,0.09); border-radius: 16px; padding: 8px; box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 0 1px rgba(56,189,248,0.06); transform-origin: top right; z-index: 300; }
.drop-head { display: flex; align-items: center; gap: 10px; padding: 10px 8px 12px; }
.drop-avatar { width: 40px; height: 40px; border-radius: 12px; background: linear-gradient(135deg, #16a34a, #4ade80); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1rem; color: #022c22; flex-shrink: 0; box-shadow: 0 0 14px rgba(74,222,128,0.25); }
.drop-info strong { display: block; font-size: 0.88rem; color: #fff; font-weight: 700; }
.drop-info span { display: block; font-size: 0.7rem; color: #4ade80; margin-top: 2px; }
.drop-sep { height: 1px; background: rgba(255,255,255,0.06); margin: 4px 0; }
.drop-item { display: flex; align-items: center; gap: 10px; width: 100%; padding: 9px 12px; border-radius: 9px; font-size: 0.85rem; font-weight: 500; color: rgba(255,255,255,0.7); text-decoration: none; background: none; border: none; cursor: pointer; font-family: 'Outfit', sans-serif; text-align: left; transition: background 0.18s, color 0.18s, transform 0.15s; }
.drop-item svg { flex-shrink: 0; opacity: 0.7; }
.drop-item:hover { background: rgba(255,255,255,0.07); color: #fff; transform: translateX(2px); }
.drop-item:hover svg { opacity: 1; }
.drop-item.danger { color: rgba(248,113,113,0.75); }
.drop-item.danger:hover { background: rgba(239,68,68,0.12); color: #f87171; }

.drop-enter-active { animation: drop-in 0.22s cubic-bezier(.34,1.4,.64,1); }
.drop-leave-active { animation: drop-in 0.14s ease-in reverse; }

@keyframes drop-in { from { opacity: 0; transform: scale(0.93) translateY(-8px); } to { opacity: 1; transform: scale(1) translateY(0); } }
</style>