<template>
  <div>
      <h2 class="fw-bold mb-4">Welcome back, {{ currentUserName }}</h2>
      
      <!-- Quick Notification Alerts -->
      <div v-if="notifications.length > 0" class="card border-0 shadow-sm bg-info-subtle border-start border-info border-3 mb-4 p-2">
          <div class="card-body d-flex justify-content-between align-items-center py-2">
              <div class="d-flex align-items-center">
                  <i class="bi bi-bell-fill text-info fs-4 me-3"></i>
                  <div>
                      <span class="fw-semibold">Export Notification: </span>
                      <span>{{ notifications[notifications.length - 1].message }}</span>
                      <a v-if="notifications[notifications.length - 1].download_url" :href="notifications[notifications.length - 1].download_url" class="btn btn-link btn-sm text-info fw-bold p-0 ms-2 text-decoration-none" download>Download CSV</a>
                  </div>
              </div>
              <button @click="clearNotifications" class="btn-close" aria-label="Close"></button>
          </div>
      </div>

      <div class="row g-4 mb-4">
          <div class="col-md-4">
              <div class="card border-0 shadow-sm p-4 text-center">
                  <h6 class="text-muted mb-1">Total Adventures Booked</h6>
                  <h2 class="fw-bold text-primary">{{ stats.total_bookings }}</h2>
              </div>
          </div>
          <div class="col-md-4">
              <div class="card border-0 shadow-sm p-4 text-center">
                  <h6 class="text-muted mb-1">Upcoming Expeditions</h6>
                  <h2 class="fw-bold text-success">{{ stats.upcoming }}</h2>
              </div>
          </div>
          <div class="col-md-4">
              <div class="card border-0 shadow-sm p-4 text-center">
                  <h6 class="text-muted mb-1">Completed Summits</h6>
                  <h2 class="fw-bold text-secondary">{{ stats.completed }}</h2>
              </div>
          </div>
      </div>

      <div class="row g-4">
          <div class="col-md-8">
              <div class="card border-0 shadow-sm">
                  <div class="card-header bg-transparent border-0 pt-4 px-4">
                      <h5 class="fw-bold mb-0">Ready for your next journey?</h5>
                  </div>
                  <div class="card-body px-4 pb-4">
                      <p class="text-muted">Browse and explore verified routes with guide coordination and slot safety constraints. Select an open itinerary matching your difficulty and location preferences.</p>
                      <router-link to="/user/treks" class="btn btn-primary rounded-pill px-4 me-2 text-decoration-none">Explore Open Treks</router-link>
                      <router-link to="/user/bookings" class="btn btn-outline-secondary rounded-pill px-4 text-decoration-none">View Reservation History</router-link>
                  </div>
              </div>
          </div>
          <div class="col-md-4">
              <div class="card border-0 shadow-sm h-100">
                  <div class="card-body p-4 d-flex flex-column justify-content-center text-center">
                      <i class="bi bi-person-circle fs-1 text-muted mb-2"></i>
                      <h5 class="fw-bold">My profile details</h5>
                      <p class="text-muted small">Update your email, contact details and password credentials.</p>
                      <router-link to="/user/profile" class="btn btn-sm btn-outline-primary rounded-pill mt-2 text-decoration-none">Edit Profile</router-link>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import { store } from '../../store';
import { fetchAPI } from '../../utils/api';

export default {
    name: 'UserDashboard',
    data() {
        return {
            stats: {
                total_bookings: 0,
                upcoming: 0,
                completed: 0
            },
            notifications: [],
            pollInterval: null
        };
    },
    computed: {
        currentUserName() {
            return store.user ? store.user.name : "Explorer";
        }
    },
    mounted() {
        this.fetchDashboardData();
        this.fetchNotifications();
        
        // Polling notifications for CSV export completes
        this.pollInterval = setInterval(() => {
            this.fetchNotifications();
        }, 5000);
    },
    beforeUnmount() {
        if (this.pollInterval) clearInterval(this.pollInterval);
    },
    methods: {
        async fetchDashboardData() {
            try {
                const res = await fetchAPI("/user/dashboard");
                if (res) {
                    this.stats = res;
                }
            } catch (err) {
                console.error(err);
            }
        },
        async fetchNotifications() {
            try {
                const res = await fetchAPI("/user/notifications");
                if (res) {
                    this.notifications = res;
                }
            } catch (err) {
                console.error(err);
            }
        },
        async clearNotifications() {
            try {
                await fetchAPI("/user/notifications/clear", { method: "POST" });
                this.notifications = [];
            } catch (err) {
                console.error(err);
            }
        }
    }
}
</script>
