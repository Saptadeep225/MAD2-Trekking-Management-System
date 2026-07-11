<template>
  <div class="row justify-content-center py-4">
      <div class="col-md-8">
          <div class="card border-0 shadow p-3">
              <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center mb-4">
                      <h3 class="fw-bold mb-0">{{ isEdit ? 'Edit Trek Route' : 'Add New Itinerary' }}</h3>
                      <router-link to="/admin/treks" class="btn btn-outline-secondary btn-sm rounded-pill px-3 text-decoration-none">Back to List</router-link>
                  </div>
                  <form @submit.prevent="saveTrek">
                      <div class="row g-3 mb-3">
                          <div class="col-md-8">
                              <label class="form-label fw-medium">Trek Itinerary Name</label>
                              <input type="text" v-model="form.name" class="form-control" required placeholder="e.g. Kedarkantha Base Camp">
                          </div>
                          <div class="col-md-4">
                              <label class="form-label fw-medium">Difficulty Profile</label>
                              <select v-model="form.difficulty" class="form-select">
                                  <option value="Easy">Easy</option>
                                  <option value="Moderate">Moderate</option>
                                  <option value="Hard">Hard</option>
                              </select>
                          </div>
                      </div>
                      <div class="row g-3 mb-3">
                          <div class="col-md-6">
                              <label class="form-label fw-medium">Location State/Region</label>
                              <input type="text" v-model="form.location" class="form-control" required placeholder="e.g. Uttarakhand">
                          </div>
                          <div class="col-md-6">
                              <label class="form-label fw-medium">Route Itinerary Duration (Days)</label>
                              <input type="number" v-model="form.duration" class="form-control" required min="1">
                          </div>
                      </div>
                      <div class="row g-3 mb-3">
                          <div class="col-md-6">
                              <label class="form-label fw-medium">Total Maximum Capacity Slots</label>
                              <input type="number" v-model="form.total_slots" class="form-control" required min="1" @input="updateSlots">
                          </div>
                          <div class="col-md-6">
                              <label class="form-label fw-medium">Available Remaining Slots</label>
                              <input type="number" v-model="form.available_slots" class="form-control" required :max="form.total_slots" min="0">
                          </div>
                      </div>
                      <div class="row g-3 mb-4">
                          <div class="col-md-6">
                              <label class="form-label fw-medium">Start Date of Expedition</label>
                              <input type="date" v-model="form.start_date" class="form-control" required>
                          </div>
                          <div class="col-md-6">
                              <label class="form-label fw-medium">End Date of Expedition</label>
                              <input type="date" v-model="form.end_date" class="form-control" required>
                          </div>
                      </div>
                      <div class="mb-4">
                          <label class="form-label fw-medium">Description and Instructions</label>
                          <textarea v-model="form.description" class="form-control" rows="4" placeholder="Itinerary details, gear checklist, emergency contact details..."></textarea>
                      </div>
                      <button type="submit" class="btn btn-primary w-100 py-2 rounded-pill fw-semibold shadow-sm">
                          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                          Save Route Details
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
    name: 'AdminTrekForm',
    data() {
        return {
            form: {
                name: "",
                difficulty: "Easy",
                location: "",
                duration: 1,
                total_slots: 10,
                available_slots: 10,
                start_date: "",
                end_date: "",
                description: ""
            },
            isEdit: false,
            loading: false
        };
    },
    mounted() {
        const id = this.$route.params.id;
        if (id) {
            this.isEdit = true;
            this.fetchTrekDetails(id);
        }
    },
    methods: {
        async fetchTrekDetails(id) {
            try {
                const res = await fetchAPI(`/api/treks/${id}`);
                if (res) {
                    this.form = {
                        ...res,
                        start_date: res.start_date || "",
                        end_date: res.end_date || ""
                    };
                }
            } catch (err) {
                showAlert("Error", "Could not fetch trek details.", "error");
            }
        },
        updateSlots() {
            if (!this.isEdit) {
                this.form.available_slots = this.form.total_slots;
            }
        },
        async saveTrek() {
            this.loading = true;
            try {
                const url = this.isEdit ? `/admin/treks/edit/${this.form.id}` : "/admin/treks/add";
                const method = this.isEdit ? "PUT" : "POST";
                await fetchAPI(url, {
                    method,
                    body: JSON.stringify(this.form)
                });
                showAlert("Success", this.isEdit ? "Trek updated successfully." : "Trek itinerary added successfully.", "success");
                this.$router.push("/admin/treks");
            } catch (err) {
                showAlert("Saving Failed", err.message, "error");
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>
