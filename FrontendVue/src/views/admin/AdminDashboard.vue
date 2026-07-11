<template>
  <div>
      <h2 class="fw-bold mb-4">Admin Console</h2>
      
      <!-- Stats Counters -->
      <div class="row g-4 mb-4">
          <div class="col-md-3">
              <div class="card border-0 shadow-sm bg-primary text-white">
                  <div class="card-body p-4 d-flex justify-content-between align-items-center">
                      <div>
                          <h6 class="card-subtitle mb-1 text-white-50">Active Trekkers</h6>
                          <h3 class="card-title mb-0 fw-bold">{{ stats.total_users }}</h3>
                      </div>
                      <i class="bi bi-people fs-1 opacity-50"></i>
                  </div>
              </div>
          </div>
          <div class="col-md-3">
              <div class="card border-0 shadow-sm bg-success text-white">
                  <div class="card-body p-4 d-flex justify-content-between align-items-center">
                      <div>
                          <h6 class="card-subtitle mb-1 text-white-50">Staff Accounts</h6>
                          <h3 class="card-title mb-0 fw-bold">{{ stats.total_staff }}</h3>
                      </div>
                      <i class="bi bi-person-badge fs-1 opacity-50"></i>
                  </div>
              </div>
          </div>
          <div class="col-md-3">
              <div class="card border-0 shadow-sm bg-info text-white">
                  <div class="card-body p-4 d-flex justify-content-between align-items-center">
                      <div>
                          <h6 class="card-subtitle mb-1 text-white-50">Trekking Routes</h6>
                          <h3 class="card-title mb-0 fw-bold">{{ stats.total_treks }}</h3>
                      </div>
                      <i class="bi bi-map fs-1 opacity-50"></i>
                  </div>
              </div>
          </div>
          <div class="col-md-3">
              <div class="card border-0 shadow-sm bg-warning text-white">
                  <div class="card-body p-4 d-flex justify-content-between align-items-center">
                      <div>
                          <h6 class="card-subtitle mb-1 text-white-50">Bookings Count</h6>
                          <h3 class="card-title mb-0 fw-bold">{{ stats.total_bookings }}</h3>
                      </div>
                      <i class="bi bi-journal-check fs-1 opacity-50"></i>
                  </div>
              </div>
          </div>
      </div>

      <!-- Charts & Quick Actions -->
      <div class="row g-4 mb-4">
          <div class="col-lg-8">
              <div class="card border-0 shadow-sm mb-4">
                  <div class="card-header bg-transparent border-0 pt-4 px-4">
                      <h5 class="fw-bold mb-0">Popular Treks Analytics</h5>
                  </div>
                  <div class="card-body px-4 pb-4">
                      <div class="chart-container position-relative" style="height:300px;">
                          <canvas id="popularTreksChart"></canvas>
                      </div>
                  </div>
              </div>
          </div>
          <div class="col-lg-4">
              <div class="card border-0 shadow-sm h-100">
                  <div class="card-header bg-transparent border-0 pt-4 px-4">
                      <h5 class="fw-bold mb-0">Quick Operations</h5>
                  </div>
                  <div class="card-body px-4 pb-4 d-flex flex-column justify-content-around">
                      <router-link to="/admin/treks/add" class="btn btn-outline-primary py-3 w-100 rounded-3 mb-3 d-flex align-items-center justify-content-center text-decoration-none">
                          <i class="bi bi-plus-circle me-2 fs-5"></i> Create New Trek
                      </router-link>
                      <router-link to="/admin/staff" class="btn btn-outline-success py-3 w-100 rounded-3 mb-3 d-flex align-items-center justify-content-center text-decoration-none">
                          <i class="bi bi-person-plus me-2 fs-5"></i> Manage Guides / Staff
                      </router-link>
                      <router-link to="/admin/bookings" class="btn btn-outline-warning py-3 w-100 rounded-3 d-flex align-items-center justify-content-center text-decoration-none">
                          <i class="bi bi-journal-text me-2 fs-5"></i> View Reservations
                      </router-link>
                  </div>
              </div>
          </div>
      </div>

      <div class="row g-4">
          <div class="col-md-6">
              <div class="card border-0 shadow-sm">
                  <div class="card-header bg-transparent border-0 pt-4 px-4 d-flex justify-content-between align-items-center">
                      <h5 class="fw-bold mb-0">Pending Staff Requests</h5>
                      <span class="badge bg-danger rounded-pill">{{ stats.pending_staff }} Requests</span>
                  </div>
                  <div class="card-body px-4 pb-4">
                      <div v-if="pendingGuides.length === 0" class="text-center py-4 text-muted">
                          <i class="bi bi-check2-circle fs-2 text-success"></i>
                          <p class="mb-0 mt-2 small">All staff applications approved.</p>
                      </div>
                      <div v-else class="list-group list-group-flush">
                          <div v-for="guide in pendingGuides" :key="guide.id" class="list-group-item px-0 py-3 d-flex justify-content-between align-items-center">
                              <div>
                                  <h6 class="fw-semibold mb-1">{{ guide.name }}</h6>
                                  <p class="mb-0 text-muted small">Username: {{ guide.username }} | Email: {{ guide.email }}</p>
                              </div>
                              <button @click="approveGuide(guide.id)" class="btn btn-success btn-sm rounded-pill px-3">Approve</button>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
          <div class="col-md-6">
              <div class="card border-0 shadow-sm">
                  <div class="card-header bg-transparent border-0 pt-4 px-4">
                      <h5 class="fw-bold mb-0">Reservations Breakdown</h5>
                  </div>
                  <div class="card-body px-4 pb-4">
                      <div class="chart-container position-relative" style="height:250px;">
                          <canvas id="participationChart"></canvas>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import { fetchAPI, showAlert } from '../../utils/api';

export default {
    name: 'AdminDashboard',
    data() {
        return {
            stats: {
                total_users: 0,
                total_staff: 0,
                total_treks: 0,
                total_bookings: 0,
                pending_staff: 0,
                popular_treks: [],
                participation: {}
            },
            pendingGuides: [],
            charts: {
                popular: null,
                participation: null
            }
        };
    },
    mounted() {
        this.fetchDashboardData();
        this.fetchPendingGuides();
    },
    beforeUnmount() {
        if (this.charts.popular) this.charts.popular.destroy();
        if (this.charts.participation) this.charts.participation.destroy();
    },
    methods: {
        async fetchDashboardData() {
            try {
                const res = await fetchAPI("/admin/dashboard");
                if (res) {
                    this.stats = res;
                    this.$nextTick(() => {
                        this.renderCharts();
                    });
                }
            } catch (err) {
                showAlert("Error", "Could not fetch dashboard metrics.", "error");
            }
        },
        async fetchPendingGuides() {
            try {
                const res = await fetchAPI("/admin/staff");
                if (res) {
                    this.pendingGuides = res.filter(g => g.status === "pending");
                }
            } catch (err) {
                console.error(err);
            }
        },
        async approveGuide(id) {
            try {
                await fetchAPI(`/admin/staff/approve/${id}`, { method: "POST" });
                showAlert("Success", "Staff approved successfully.", "success");
                this.fetchPendingGuides();
                this.fetchDashboardData();
            } catch (err) {
                showAlert("Error", err.message, "error");
            }
        },
        renderCharts() {
            if (this.charts.popular) this.charts.popular.destroy();
            if (this.charts.participation) this.charts.participation.destroy();

            const ChartClass = window.Chart;
            if (!ChartClass) {
                console.error("Chart.js not loaded.");
                return;
            }

            // Popular Treks Chart
            const ptCtx = document.getElementById("popularTreksChart");
            if (ptCtx) {
                const trekNames = this.stats.popular_treks.map(t => t.name);
                const trekBookings = this.stats.popular_treks.map(t => t.bookings);
                
                this.charts.popular = new ChartClass(ptCtx, {
                    type: "bar",
                    data: {
                        labels: trekNames,
                        datasets: [{
                            label: "Total Reservations",
                            data: trekBookings,
                            backgroundColor: "#3b7597",
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            y: { beginAtZero: true, ticks: { precision: 0 } }
                        }
                    }
                });
            }

            // Booking Participation Chart
            const partCtx = document.getElementById("participationChart");
            if (partCtx) {
                const statuses = Object.keys(this.stats.participation);
                const counts = Object.values(this.stats.participation);
                
                this.charts.participation = new ChartClass(partCtx, {
                    type: "doughnut",
                    data: {
                        labels: statuses,
                        datasets: [{
                            data: counts,
                            backgroundColor: ["#198754", "#dc3545", "#6c757d"]
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: "right" }
                        }
                    }
                });
            }
        }
    }
}
</script>
