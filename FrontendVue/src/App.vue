<template>
  <div class="d-flex flex-column min-vh-100">
    <app-navbar></app-navbar>
    <div class="container py-4 main-content">
        <router-view></router-view>
    </div>
    <footer class="footer py-3 text-center text-muted border-top mt-auto bg-white">
        <div class="container">
            <span>TrekTour</span>
        </div>
    </footer>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  name: 'App',
  components: {
    'app-navbar': Navbar
  }
}
</script>
