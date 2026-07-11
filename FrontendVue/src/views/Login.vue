<template>
  <div class="row justify-content-center py-5">
      <div class="col-md-5">
          <div class="card border-0 shadow-lg p-3">
              <div class="card-body">
                  <div class="text-center mb-4">
                      <i class="bi bi-shield-lock text-primary display-4"></i>
                      <h3 class="fw-bold mt-2">Welcome Back</h3>
                      <p class="text-muted small">Access your account dashboard</p>
                  </div>
                  <form @submit.prevent="handleSubmit">
                      <div class="mb-3">
                          <label class="form-label fw-medium">Username</label>
                          <div class="input-group">
                              <span class="input-group-text bg-light border-0"><i class="bi bi-person text-muted"></i></span>
                              <input type="text" v-model="username" class="form-control border-light-subtle bg-light-subtle" required placeholder="Enter username">
                          </div>
                      </div>
                      <div class="mb-4">
                          <label class="form-label fw-medium">Password</label>
                          <div class="input-group">
                              <span class="input-group-text bg-light border-0"><i class="bi bi-key text-muted"></i></span>
                              <input type="password" v-model="password" class="form-control border-light-subtle bg-light-subtle" required placeholder="Enter password">
                          </div>
                      </div>
                      <button type="submit" class="btn btn-primary w-100 py-2 rounded-pill fw-semibold shadow-sm mb-3">
                          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                          Login
                      </button>
                  </form>
              </div>
              <div class="card-footer bg-transparent border-0 text-center text-muted py-3">
                  Don't have an account? <router-link to="/register" class="fw-semibold text-primary text-decoration-none">Register here</router-link>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import { store } from '../store';
import { fetchAPI, showAlert } from '../utils/api';

export default {
    name: 'Login',
    data() {
        return {
            username: "",
            password: "",
            loading: false
        };
    },
    methods: {
        async handleSubmit() {
            this.loading = true;
            try {
                const res = await fetchAPI("/auth/login", {
                    method: "POST",
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password
                    })
                });
                
                if (res && res.access_token) {
                    store.setToken(res.access_token);
                    store.setRole(res.role);
                    store.setUser(res.user);
                    
                    showAlert("Welcome", res.message, "success");
                    
                    if (res.role === "admin") {
                        this.$router.push("/admin/dashboard");
                    } else if (res.role === "staff") {
                        this.$router.push("/staff/dashboard");
                    } else {
                        this.$router.push("/user/dashboard");
                    }
                }
            } catch (err) {
                showAlert("Authentication Failed", err.message, "error");
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>
