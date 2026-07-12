<template>
  <div>
      <section class="hero text-white rounded-4 overflow-hidden mb-5">
          <div class="hero-overlay d-flex flex-column justify-content-center align-items-center p-5 text-center">
              <h1 class="display-3 fw-bold mb-3 tracking-tight">Climb Mountains, Discover Life</h1>
              <p class="lead mb-4 max-w-600">Track slots, register bookings, and coordinate guides for top routes across the country.</p>
              <div v-if="!isLoggedIn">
                  <router-link to="/register" class="btn btn-light btn-lg px-4 me-3 rounded-pill fw-semibold shadow-sm">Get Started</router-link>
                  <router-link to="/login" class="btn btn-outline-light btn-lg px-4 rounded-pill shadow-sm">Login</router-link>
              </div>
              <div v-else>
                  <router-link :to="dashboardRoute" class="btn btn-light btn-lg px-4 rounded-pill fw-semibold shadow-sm">Go to Dashboard</router-link>
              </div>
          </div>
      </section>

      <div class="row align-items-center mb-5 py-3">
          <div class="col-lg-6 mb-4 mb-lg-0">
              <h2 class="fw-bold mb-3">Professional Trekking Infrastructure</h2>
              <p class="text-muted mb-4">We bridge the gap between adventure organizations, assigned field staff, and eager trekkers. Our application coordinates trek routing, real-time participant capacity metrics, and route completion logs.</p>
              <div class="row g-3">
                  <div class="col-md-6 d-flex align-items-start">
                      <div class="feature-icon bg-light text-primary rounded p-2 me-3">
                          <i class="bi bi-calendar-event fs-4"></i>
                      </div>
                      <div>
                          <h5 class="fw-semibold mb-1">Easy Bookings</h5>
                          <p class="text-muted small">Reserve slots instantly with strict duplicate preventions.</p>
                      </div>
                  </div>
                  <div class="col-md-6 d-flex align-items-start">
                      <div class="feature-icon bg-light text-primary rounded p-2 me-3">
                          <i class="bi bi-people fs-4"></i>
                      </div>
                      <div>
                          <h5 class="fw-semibold mb-1">Assigned Guides</h5>
                          <p class="text-muted small">Every group is accompanied by verified trek coordinators.</p>
                      </div>
                  </div>
              </div>
          </div>
          <div class="col-lg-6">
              <div class="card bg-dark text-white rounded-4 border-0 shadow overflow-hidden">
                  <img src="/images/hero.jpg" alt="Mountain Peak" class="card-img opacity-50">
                  <div class="card-img-overlay d-flex flex-column justify-content-end p-4">
                      <h4 class="fw-bold">Ready for the Summit?</h4>
                      <p class="card-text small text-light opacity-75">Sign up today and browse moderate to extreme itineraries led by certified experts.</p>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import { store } from '../store';

export default {
    name: 'Home',
    computed: {
        isLoggedIn() {
            return !!store.token;
        },
        dashboardRoute() {
            const role = store.role;
            if (role === "admin") return "/admin/dashboard";
            if (role === "staff") return "/staff/dashboard";
            return "/user/dashboard";
        }
    }
}
</script>
