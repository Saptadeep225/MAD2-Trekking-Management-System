<template>
  <div>
      <div class="d-flex flex-column flex-sm-row justify-content-between align-items-start align-items-sm-center mb-4 g-2">
          <h2 class="fw-bold mb-0">My Adventures History</h2>
          <button @click="triggerExport" class="btn btn-outline-secondary rounded-pill px-3 shadow-sm">
              <span v-if="exporting" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-file-earmark-excel me-1"></i> Export Booking History
          </button>
      </div>

      <div class="card border-0 shadow-sm overflow-hidden">
          <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                  <thead class="table-light text-muted uppercase small">
                      <tr>
                          <th class="px-4">Booking ID</th>
                          <th>Trek Name</th>
                          <th>Location</th>
                          <th>Departure Date</th>
                          <th>Reservation Date</th>
                          <th>Status</th>
                          <th class="text-end px-4">Actions</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-if="bookings.length === 0">
                          <td colspan="7" class="text-center py-5 text-muted">You have no booking reservations logged on your account.</td>
                      </tr>
                      <tr v-for="b in bookings" :key="b.id">
                          <td class="px-4 text-muted">#{{ b.id }}</td>
                          <td><span class="fw-semibold">{{ b.trek ? b.trek.name : 'Deleted Itinerary' }}</span></td>
                          <td>{{ b.trek ? b.trek.location : '' }}</td>
                          <td>{{ b.trek ? b.trek.start_date : '' }}</td>
                          <td>{{ formatDate(b.booking_date) }}</td>
                          <td>
                              <span class="badge" :class="{
                                  'bg-success': b.status === 'Booked',
                                  'bg-danger': b.status === 'Cancelled',
                                  'bg-secondary': b.status === 'Completed'
                              }">{{ b.status }}</span>
                          </td>
                          <td class="text-end px-4">
                              <button v-if="b.status === 'Booked'" @click="cancelBooking(b.id)" class="btn btn-outline-danger btn-sm rounded-pill px-3">Cancel Reservation</button>
                              <span v-else class="text-muted small">-</span>
                          </td>
                      </tr>
                  </tbody>
              </table>
          </div>
      </div>
  </div>
</template>

<script>
import { fetchAPI, showAlert, formatDateString } from '../../utils/api';

export default {
    name: 'UserBookings',
    data() {
        return {
            bookings: [],
            exporting: false
        };
    },
    mounted() {
        this.fetchBookings();
    },
    methods: {
        async fetchBookings() {
            try {
                const res = await fetchAPI("/user/bookings");
                if (res) {
                    this.bookings = res;
                }
            } catch (err) {
                showAlert("Error", "Could not fetch bookings list.", "error");
            }
        },
        async cancelBooking(id) {
            if (!window.Swal) return;
            window.Swal.fire({
                title: "Cancel Reservation?",
                text: "This will release your slot back to the trek capacity.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#dc3545",
                cancelButtonColor: "#6c757d",
                confirmButtonText: "Confirm Cancellation"
            }).then(async (result) => {
                if (result.isConfirmed) {
                    try {
                        await fetchAPI(`/user/bookings/cancel/${id}`, { method: "POST" });
                        showAlert("Cancelled", "Reservation cancelled successfully.", "success");
                        this.fetchBookings();
                    } catch (err) {
                        showAlert("Cancellation Failed", err.message, "error");
                    }
                }
            });
        },
        async triggerExport() {
            this.exporting = true;
            try {
                const res = await fetchAPI("/user/export", { method: "POST" });
                showAlert("Export Started", res.message, "info");
            } catch (err) {
                showAlert("Export Failed", err.message, "error");
            } finally {
                this.exporting = false;
            }
        },
        formatDate(dtStr) {
            return formatDateString(dtStr);
        }
    }
}
</script>
