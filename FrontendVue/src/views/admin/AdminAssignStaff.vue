<template>
  <div class="row justify-content-center py-4">
      <div class="col-md-6">
          <div class="card border-0 shadow p-3">
              <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center mb-4">
                      <h4 class="fw-bold mb-0">Assign Guide Staff</h4>
                      <router-link to="/admin/treks" class="btn btn-outline-secondary btn-sm rounded-pill px-3 text-decoration-none">Back</router-link>
                  </div>
                  <h6 class="text-muted">Itinerary Name:</h6>
                  <h4 class="fw-bold text-primary mb-4">{{ trekName }}</h4>
                  <form @submit.prevent="assignStaff">
                      <div class="mb-4">
                          <label class="form-label fw-medium">Available Guides list</label>
                          <select v-model="selectedStaffId" class="form-select bg-light">
                              <option :value="null">Unassign Guide / Free Route</option>
                              <option v-for="member in staff" :key="member.id" :value="member.id">{{ member.name }} (Username: {{ member.username }})</option>
                          </select>
                      </div>
                      <button type="submit" class="btn btn-primary w-100 py-2 rounded-pill fw-semibold shadow-sm">
                          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                          Confirm Guide Assignment
                      </button>
                  </form>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import { fetchAPI, showAlert } from '../../utils/api';

export default {
    name: 'AdminAssignStaff',
    data() {
        return {
            trekName: "",
            selectedStaffId: null,
            staff: [],
            loading: false
        };
    },
    mounted() {
        this.fetchTrekDetails();
        this.fetchGuides();
    },
    methods: {
        async fetchTrekDetails() {
            const id = this.$route.params.id;
            try {
                const res = await fetchAPI(`/api/treks/${id}`);
                if (res) {
                    this.trekName = res.name;
                    this.selectedStaffId = res.assigned_staff;
                }
            } catch (err) {
                showAlert("Error", "Could not fetch trek details.", "error");
            }
        },
        async fetchGuides() {
            try {
                const res = await fetchAPI("/admin/staff");
                if (res) {
                    this.staff = res.filter(s => s.status === "approved");
                }
            } catch (err) {
                console.error(err);
            }
        },
        async assignStaff() {
            const id = this.$route.params.id;
            this.loading = true;
            try {
                await fetchAPI(`/admin/treks/assign/${id}`, {
                    method: "POST",
                    body: JSON.stringify({ staff_id: this.selectedStaffId })
                });
                showAlert("Success", "Coordinating guide assigned successfully.", "success");
                this.$router.push("/admin/treks");
            } catch (err) {
                showAlert("Assignment Failed", err.message, "error");
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>
