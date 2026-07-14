<template>
  <div>
      <h2 class="fw-bold mb-4">Expedition Bookings Console</h2>

      <div class="card border-0 shadow-sm mb-4">
          <div class="card-body p-3">
              <form @submit.prevent="fetchBookings" class="row g-2">
                  <div class="col-md-9">
                      <div class="input-group">
                          <span class="input-group-text bg-light border-0"><i class="bi bi-search text-muted"></i></span>
                          <input type="text" v-model="searchQuery" class="form-control bg-light border-0" placeholder="Search by participant name or trek title...">
                      </div>
                  </div>
                  <div class="col-md-3">
                      <button type="submit" class="btn btn-outline-primary w-100">Filter Reservation</button>
                  </div>
              </form>
          </div>
      </div>

      <div class="card border-0 shadow-sm overflow-hidden">
          <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                  <thead class="table-light text-muted uppercase small">
                      <tr>
                          <th class="px-4">Booking ID</th>
                          <th>Trekker Name</th>
                          <th>Trek Title</th>
                          <th>Location</th>
                          <th>Reserved Date</th>
                          <th>Expedition status</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-if="bookings.length === 0">
                          <td colspan="6" class="text-center py-4 text-muted">No reservations booked on system.</td>
                      </tr>
                      <tr v-for="b in bookings" :key="b.id">
                          <td class="px-4 text-muted">#{{ b.id }}</td>
                          <td>
                              <div class="fw-semibold">{{ b.user ? b.user.name : 'Unknown User' }}</div>
                              <div class="text-muted small">{{ b.user ? b.user.email : '' }}</div>
                          </td>
                          <td><span class="fw-semibold text-primary">{{ b.trek ? b.trek.name : 'Deleted Trek' }}</span></td>
                          <td>{{ b.trek ? b.trek.location : '' }}</td>
                          <td>{{ formatDateTime(b.booking_date) }}</td>
                          <td>
                              <span class="badge" :class="{
                                  'bg-success': b.status === 'Booked',
                                  'bg-danger': b.status === 'Cancelled',
                                  'bg-secondary': b.status === 'Completed'
                              }">{{ b.status }}</span>
                          </td>
                      </tr>
                  </tbody>
              </table>
          </div>
      </div>
  </div>
</template>

<script>
import { fetchAPI, showAlert, formatDateTimeString } from '../../utils/api';

export default {
    name: 'AdminBookings',
    data() {
        return {
            bookings: [],
            searchQuery: ""
        };
    },
    mounted() {
        this.fetchBookings();
    },
    methods: {
        async fetchBookings() {
            try {
                const url = this.searchQuery ? `/admin/bookings?search=${encodeURIComponent(this.searchQuery)}` : "/admin/bookings";
                const res = await fetchAPI(url);
                if (res) {
                    this.bookings = res;
                }
            } catch (err) {
                showAlert("Error", "Could not fetch bookings log.", "error");
            }
        },
        formatDateTime(dtStr) {
            return formatDateTimeString(dtStr);
        }
    }
}
</script>