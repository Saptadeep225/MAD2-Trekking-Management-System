<template>
  <nav class="navbar navbar-expand-lg navbar-dark shadow-sm">
      <div class="container">
          <router-link to="/" class="navbar-brand d-flex align-items-center">
              <i class="bi bi-compass me-2"></i>
              <span class="fw-bold tracking-tight">TrekTour</span>
          </router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav ms-auto align-items-lg-center">
                  <!-- Guest Links -->
                  <li class="nav-item" v-if="!isLoggedIn">
                      <router-link to="/login" class="nav-link">Login</router-link>
                  </li>
                  <li class="nav-item" v-if="!isLoggedIn">
                      <router-link to="/register" class="btn btn-light btn-sm px-3 ms-lg-2 rounded-pill fw-semibold">Register</router-link>
                  </li>

                  <!-- User Links -->
                  <li class="nav-item" v-if="isLoggedIn && role === 'user'">
                      <router-link to="/user/dashboard" class="nav-link">Dashboard</router-link>
                  </li>
                  <li class="nav-item" v-if="isLoggedIn && role === 'user'">
                      <router-link to="/user/treks" class="nav-link">Explore Treks</router-link>
                  </li>
                  <li class="nav-item" v-if="isLoggedIn && role === 'user'">
                      <router-link to="/user/bookings" class="nav-link">My Bookings</router-link>
                  </li>
                  <li class="nav-item" v-if="isLoggedIn && role === 'user'">
                      <router-link to="/user/profile" class="nav-link">Profile</router-link>
                  </li>

                  <!-- Staff Links -->
                  <li class="nav-item" v-if="isLoggedIn && role === 'staff'">
                      <router-link to="/staff/dashboard" class="nav-link">Dashboard</router-link>
                  </li>
                  <li class="nav-item" v-if="isLoggedIn && role === 'staff'">
                      <router-link to="/staff/treks" class="nav-link">My Treks</router-link>
                  </li>

                  <!-- Admin Links -->
                  <li class="nav-item" v-if="isLoggedIn && role === 'admin'">
                      <router-link to="/admin/dashboard" class="nav-link">Dashboard</router-link>
                  </li>
                  <li class="nav-item" v-if="isLoggedIn && role === 'admin'">
                      <router-link to="/admin/treks" class="nav-link">Treks</router-link>
                  </li>
                  <li class="nav-item" v-if="isLoggedIn && role === 'admin'">
                      <router-link to="/admin/staff" class="nav-link">Staff</router-link>
                  </li>
                  <li class="nav-item" v-if="isLoggedIn && role === 'admin'">
                      <router-link to="/admin/users" class="nav-link">Users</router-link>
                  </li>
                  <li class="nav-item" v-if="isLoggedIn && role === 'admin'">
                      <router-link to="/admin/bookings" class="nav-link">Bookings</router-link>
                  </li>

                  <!-- Logout Button -->
                  <li class="nav-item ms-lg-3" v-if="isLoggedIn">
                      <button @click="logout" class="btn btn-outline-light btn-sm px-3 rounded-pill">Logout</button>
                  </li>
              </ul>
          </div>
      </div>
  </nav>
</template>

<script>
import { store } from '../store';
import { fetchAPI, showAlert } from '../utils/api';

export default {
    name: 'Navbar',
    computed: {
        isLoggedIn() {
            return !!store.token;
        },
        role() {
            return store.role;
        }
    },
    methods: {
        async logout() {
            try {
                await fetchAPI("/auth/logout", { method: "POST" });
            } catch (err) {
                console.error("Logout error", err);
            } finally {
                store.clear();
                showAlert("Logged Out", "You have been logged out successfully.", "info");
                this.$router.push("/login");
            }
        }
    }
}
</script>
