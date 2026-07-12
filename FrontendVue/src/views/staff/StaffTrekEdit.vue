<template>
  <div class="row justify-content-center py-4">
      <div class="col-md-6">
          <div class="card border-0 shadow p-3">
              <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center mb-4">
                      <h4 class="fw-bold mb-0">Update Details</h4>
                      <router-link to="/staff/treks" class="btn btn-outline-secondary btn-sm rounded-pill px-3 text-decoration-none">Back</router-link>
                  </div>
                  <h6 class="text-muted">Expedition Name:</h6>
                  <h4 class="fw-bold text-primary mb-4">{{ trekName }}</h4>
                  <form @submit.prevent="updateTrek">
                      <div class="mb-3">
                          <label class="form-label fw-medium">Remaining Available Slots</label>
                          <input type="number" v-model="availableSlots" class="form-control bg-light" required :max="totalSlots" min="0">
                          <div class="form-text">Maximum route capacity is {{ totalSlots }}.</div>
                      </div>
                      <div class="mb-4">
                          <label class="form-label fw-medium">Expedition status</label>
                          <select v-model="status" class="form-select bg-light">
                              <option value="Open">Open (Accepting Bookings)</option>
                              <option value="Closed">Closed (Full / Postponed)</option>
                              <option value="Completed">Completed (Expedition finished)</option>
                          </select>
                      </div>
                      <button type="submit" class="btn btn-primary w-100 py-2 rounded-pill fw-semibold shadow-sm">
                          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                          Save Updates
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
    name: 'StaffTrekEdit',
    data() {
        return {
            trekName: "",
            totalSlots: 0,
            availableSlots: 0,
            status: "",
            loading: false
        };
    },
    mounted() {
        this.fetchTrekDetails();
    },
    methods: {
        async fetchTrekDetails() {
            const id = this.$route.params.id;
            try {
                const res = await fetchAPI(`/staff/treks/update/${id}`);
                if (res) {
                    this.trekName = res.name;
                    this.totalSlots = res.total_slots;
                    this.availableSlots = res.available_slots;
                    this.status = res.status;
                }
            } catch (err) {
                showAlert("Error", "Could not fetch route information.", "error");
            }
        },
        async updateTrek() {
            const id = this.$route.params.id;
            this.loading = true;
            try {
                await fetchAPI(`/staff/treks/update/${id}`, {
                    method: "PUT",
                    body: JSON.stringify({
                        available_slots: this.availableSlots,
                        status: this.status
                    })
                });
                showAlert("Success", "Route information updated successfully.", "success");
                this.$router.push("/staff/treks");
            } catch (err) {
                showAlert("Update Failed", err.message, "error");
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>
