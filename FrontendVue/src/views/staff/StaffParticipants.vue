<template>
  <div>
      <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold mb-0">Registered Trekkers List</h2>
          <router-link to="/staff/treks" class="btn btn-outline-secondary btn-sm rounded-pill px-3 text-decoration-none">Back</router-link>
      </div>
      <h5 class="text-muted mb-4">Route Name: <span class="fw-bold text-primary">{{ trekName }}</span></h5>

      <div class="card border-0 shadow-sm overflow-hidden">
          <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                  <thead class="table-light text-muted uppercase small">
                      <tr>
                          <th class="px-4">Reservation ID</th>
                          <th>Name</th>
                          <th>Email</th>
                          <th>Phone</th>
                          <th>Booking Date</th>
                          <th>Reservation Status</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-if="participants.length === 0">
                          <td colspan="6" class="text-center py-4 text-muted">No hikers registered on this trek yet.</td>
                      </tr>
                      <tr v-for="p in participants" :key="p.id">
                          <td class="px-4 text-muted">#{{ p.id }}</td>
                          <td><span class="fw-semibold">{{ p.user ? p.user.name : 'Unknown User' }}</span></td>
                          <td>{{ p.user ? p.user.email : '' }}</td>
                          <td>{{ p.user ? p.user.phone : '' }}</td>
                          <td>{{ formatDateTime(p.booking_date) }}</td>
                          <td>
                              <span class="badge" :class="{
                                  'bg-success': p.status === 'Booked',
                                  'bg-danger': p.status === 'Cancelled',
                                  'bg-secondary': p.status === 'Completed'
                              }">{{ p.status }}</span>
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
    name: 'StaffParticipants',
    data() {
        return {
            trekName: "",
            participants: []
        };
    },
    mounted() {
        this.fetchTrekDetails();
        this.fetchParticipants();
    },
    methods: {
        async fetchTrekDetails() {
            const id = this.$route.params.id;
            try {
                const res = await fetchAPI(`/api/treks/${id}`);
                if (res) {
                    this.trekName = res.name;
                }
            } catch (err) {
                console.error(err);
            }
        },
        async fetchParticipants() {
            const id = this.$route.params.id;
            try {
                const res = await fetchAPI(`/staff/participants/${id}`);
                if (res) {
                    this.participants = res;
                }
            } catch (err) {
                showAlert("Error", "Could not fetch participants directory.", "error");
            }
        },
        formatDateTime(dtStr) {
            return formatDateTimeString(dtStr);
        }
    }
}
</script>
