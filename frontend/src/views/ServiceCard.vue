<template>
  <div class="services-page">
    <MiMenu />
    <main class="services-content">
      <HeroSection
        title="Todos tus Trámites de Salud, Aquí."
        subtitle="Nos dedicamos a cuidar tu salud y la de los tuyos. Aquí puedes gestionar tu plan, agendar citas y acceder a toda nuestra red de servicios."
        image-placeholder="Imagen de Equipo Profesional"
      />

      <h3 class="section-title">Servicios Destacados</h3>

      <section class="featured-cards">
        <FeaturedServiceCard v-for="service in services" :key="service.id" :service="service" />
      </section>
      
      </main>
  </div>
</template>

<script>
import MiMenu from '@/components/MiMenu.vue'
import HeroSection from '@/components/HeroSection.vue'
import FeaturedServiceCard from '@/components/FeaturedServiceCard.vue'

export default {
  name: 'ServiceCard',
  components: {
    MiMenu,
    HeroSection,
    FeaturedServiceCard
  },
  data() {
    return {
      services: [
        {
          id: 1,
          title: 'Agendamiento en línea',
          description: 'Programa tus citas médicas de forma fácil y rápida desde tu casa.',
          image: 'src/assets/agendamiento_Enlinea.jpg'
        },
        {
          id: 2,
          title: 'Especialistas disponibles',
          description: 'Acceso a médicos generales y especialistas en diferentes áreas de la salud.',
          image: 'src/assets/especialistas.jpg' // placeholder
        },
        {
          id: 3,
          title: 'Historial médico',
          description: 'Consulta tu historial clínico y resultados de laboratorio en línea.',
          image: 'src/assets/historial.jpg' // placeholder
        },
        {
          id: 4,
          title: 'Atención a tu familia',
          description: 'Agrega a tus familiares y gestiona sus citas desde tu perfil.',
          image: 'src/assets/familia.jpg' // placeholder
        }
      ]
    }
  }
}
</script>

<style scoped>

.services-content {
    padding-top: 20px;
}


.section-title {
    text-align: center;
    color: #007bff;
    font-size: 1.8em;
    margin: 60px 0 30px 0;
    padding-bottom: 5px;
    border-bottom: 2px solid #a4cc16; 
    display: inline-block;
    width: auto;
    max-width: 90%;
    margin-left: 50%;
    transform: translateX(-50%);
}

.featured-cards {
  max-width: 1200px;
  margin: 0 auto 60px;
  display: flex;
  justify-content: space-around;
  gap: 30px;
}

</style>