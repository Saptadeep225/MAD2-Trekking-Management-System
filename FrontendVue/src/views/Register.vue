<template>
  <div class="row justify-content-center py-4">
      <div class="col-md-6">
          <div class="card border-0 shadow-lg p-3">
              <div class="card-body">
                  <div class="text-center mb-4">
                      <i class="bi bi-person-plus text-primary display-4"></i>
                      <h3 class="fw-bold mt-2">Create Account</h3>
                      <p class="text-muted small">Join as a Trekker or apply to become a Staff member</p>
                  </div>
                  <form @submit.prevent="handleSubmit">
                      <div class="row g-3 mb-3">
                          <div class="col-md-6">
                              <label class="form-label fw-medium">Full Name</label>
                              <input type="text" v-model="form.name" class="form-control bg-light" required placeholder="e.g. John Doe">
                          </div>
                          <div class="col-md-6">
                              <label class="form-label fw-medium">Username</label>
                              <input type="text" v-model="form.username" class="form-control bg-light" required placeholder="e.g. johndoe">
                          </div>
                      </div>
                      <div class="row g-3 mb-3">
                          <div class="col-md-6">
                              <label class="form-label fw-medium">Email Address</label>
                              <input type="email" v-model="form.email" class="form-control bg-light" required placeholder="e.g. john@example.com">
                          </div>
                          <div class="col-md-6">
                              <label class="form-label fw-medium">Phone Number</label>
                              <input type="tel" v-model="form.phone" class="form-control bg-light" placeholder="e.g. 9876543210">
                          </div>
                      </div>
                      <div class="row g-3 mb-3">
                          <div class="col-md-6">
                              <label class="form-label fw-medium">Password</label>
                              <input type="password" v-model="form.password" class="form-control bg-light" required minlength="6" placeholder="Min 6 characters">
                          </div>
                          <div class="col-md-6">
                              <label class="form-label fw-medium">Confirm Password</label>
                              <input type="password" v-model="form.confirm_password" class="form-control bg-light" required placeholder="Re-type password">
                          </div>
                      </div>

                      <button type="submit" class="btn btn-primary w-100 py-2 rounded-pill fw-semibold shadow-sm mb-3">
                          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                          Register
                      </button>
                  </form>
              </div>
              <div class="card-footer bg-transparent border-0 text-center text-muted py-3">
                  Already have an account? <router-link to="/login" class="fw-semibold text-primary text-decoration-none">Login here</router-link>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import { fetchAPI, showAlert } from '../utils/api';

export default {
    name: 'Register',
    data() {
        return {
            form: {
                name: "",
                username: "",
                email: "",
                phone: "",
                password: "",
                confirm_password: "",
                role: "user"
            },
            loading: false
        };
    },
    methods: {
        async handleSubmit() {
            if (this.form.password !== this.form.confirm_password) {
                showAlert("Validation Error", "Passwords do not match.", "warning");
                return;
            }
            this.loading = true;
            try {
                await fetchAPI("/auth/register", {
                    method: "POST",
                    body: JSON.stringify(this.form)
                });
                showAlert("Registered", "Account created successfully. Please login.", "success");
                this.$router.push("/login");
            } catch (err) {
                showAlert("Registration Failed", err.message, "error");
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>
