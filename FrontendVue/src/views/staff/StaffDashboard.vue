<template>
  <div>
      <h2 class="fw-bold mb-4">Guide Dashboard</h2>
      
      <div class="row g-4 mb-4">
          <div class="col-md-6">
              <div class="card border-0 shadow-sm bg-primary text-white p-4">
                  <div class="d-flex justify-content-between align-items-center">
                      <div>
                          <h6 class="card-subtitle mb-1 text-white-50">Assigned Itineraries</h6>
                          <h3 class="card-title mb-0 fw-bold">{{ stats.assigned_treks }}</h3>
                      </div>
                      <i class="bi bi-map fs-1 opacity-50"></i>
                  </div>
              </div>
          </div>
          <div class="col-md-6">
              <div class="card border-0 shadow-sm bg-success text-white p-4">
                  <div class="d-flex justify-content-between align-items-center">
                      <div>
                          <h6 class="card-subtitle mb-1 text-white-50">Total Registered Trekkers</h6>
                          <h3 class="card-title mb-0 fw-bold">{{ stats.total_participants }}</h3>
                      </div>
                      <i class="bi bi-people fs-1 opacity-50"></i>
                  </div>
              </div>
          </div>
      </div>

      <div class="card border-0 shadow-sm mt-4">
          <div class="card-header bg-transparent border-0 pt-4 px-4">
              <h5 class="fw-bold mb-0">Guide Instructions</h5>
          </div>
          <div class="card-body px-4 pb-4">
              <p class="text-muted">You are assigned by the System Administrator to manage expedition details, update remaining slot capacity dynamically, log route statuses, and view the list of verified registrants. Ensure to update slot counts appropriately to prevent overbookings.</p>
              <router-link to="/staff/treks" class="btn btn-primary rounded-pill px-4 text-decoration-none">View My Assigned Treks</router-link>
          </div>
      </div>
  </div>
</template>

<script>
import { fetchAPI, showAlert } from '../../utils/api';

export default {
    name: 'StaffDashboard',
    data() {
        return {
            stats: {
                assigned_treks: 0,
                total_participants: 0
            }
        };
    },
    mounted() {
        this.fetchDashboardData();
    },
    methods: {
        async fetchDashboardData() {
            try {
                const res = await fetchAPI("/staff/dashboard");
                if (res) {
                    this.stats = res;
                }
            } catch (err) {
                showAlert("Error", "Could not load dashboard data.", "error");
            }
        }
    }
}
</script>
