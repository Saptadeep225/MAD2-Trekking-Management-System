<template>
  <div class="row justify-content-center py-4">
      <div class="col-md-6">
          <div class="card border-0 shadow p-3">
              <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center mb-4">
                      <h3 class="fw-bold mb-0">My Account Profile</h3>
                      <router-link to="/user/dashboard" class="btn btn-outline-secondary btn-sm rounded-pill px-3 text-decoration-none">Dashboard</router-link>
                  </div>
                  <form @submit.prevent="updateProfile">
                      <div class="mb-3">
                          <label class="form-label fw-medium">Full Name</label>
                          <input type="text" v-model="profile.name" class="form-control bg-light" required>
                      </div>
                      <div class="mb-3">
                          <label class="form-label fw-medium">Email Address</label>
                          <input type="email" v-model="profile.email" class="form-control bg-light" required>
                      </div>
                      <div class="mb-4">
                          <label class="form-label fw-medium">Phone Number</label>
                          <input type="text" v-model="profile.phone" class="form-control bg-light">
                      </div>
                      <button type="submit" class="btn btn-primary w-100 py-2 rounded-pill fw-semibold shadow-sm">
                          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                          Save Profile Changes
                      </button>
                  </form>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import { store } from '../../store';
import { fetchAPI, showAlert } from '../../utils/api';

export default {
    name: 'UserProfile',
    data() {
        return {
            profile: {
                name: "",
                email: "",
                phone: ""
            },
            loading: false
        };
    },
    mounted() {
        this.fetchProfile();
    },
    methods: {
        async fetchProfile() {
            try {
                const res = await fetchAPI("/user/profile");
                if (res) {
                    this.profile = res;
                }
            } catch (err) {
                showAlert("Error", "Could not fetch profile details.", "error");
            }
        },
        async updateProfile() {
            this.loading = true;
            try {
                const res = await fetchAPI("/user/profile", {
                    method: "PUT",
                    body: JSON.stringify(this.profile)
                });
                showAlert("Success", "Profile updated successfully.", "success");
                store.setUser(res.user);
            } catch (err) {
                showAlert("Update Failed", err.message, "error");
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>
