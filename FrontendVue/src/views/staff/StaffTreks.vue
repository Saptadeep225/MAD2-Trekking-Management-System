<template>
  <div>
      <h2 class="fw-bold mb-4">My Assigned Expeditions</h2>

      <div class="card border-0 shadow-sm overflow-hidden">
          <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                  <thead class="table-light text-muted uppercase small">
                      <tr>
                          <th class="px-4">Route ID</th>
                          <th>Trek Name</th>
                          <th>Location</th>
                          <th>Expedition Dates</th>
                          <th>Slots Remaining</th>
                          <th>Difficulty</th>
                          <th>Status</th>
                          <th class="text-end px-4">Actions</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-if="treks.length === 0">
                          <td colspan="8" class="text-center py-5 text-muted">You have no treks assigned by the Admin.</td>
                      </tr>
                      <tr v-for="trek in treks" :key="trek.id">
                          <td class="px-4 text-muted">#{{ trek.id }}</td>
                          <td><span class="fw-semibold">{{ trek.name }}</span></td>
                          <td>{{ trek.location }}</td>
                          <td>{{ trek.start_date }} to {{ trek.end_date }}</td>
                          <td><span class="fw-bold">{{ trek.available_slots }}</span> / {{ trek.total_slots }}</td>
                          <td>
                              <span class="badge" :class="{
                                  'bg-success-subtle text-success': trek.difficulty === 'Easy',
                                  'bg-warning-subtle text-warning-emphasis': trek.difficulty === 'Moderate',
                                  'bg-danger-subtle text-danger': trek.difficulty === 'Hard'
                              }">{{ trek.difficulty }}</span>
                          </td>
                          <td>
                              <span class="badge" :class="{
                                  'bg-info': trek.status === 'Open',
                                  'bg-secondary': trek.status === 'Closed' || trek.status === 'Completed',
                                  'bg-warning': trek.status === 'Pending' || trek.status === 'Approved'
                              }">{{ trek.status }}</span>
                          </td>
                          <td class="text-end px-4">
                              <router-link :to="'/staff/treks/update/' + trek.id" class="btn btn-sm btn-outline-primary rounded-pill px-3 me-2 text-decoration-none">Update Slots/Status</router-link>
                              <router-link :to="'/staff/treks/participants/' + trek.id" class="btn btn-sm btn-outline-secondary rounded-pill px-3 text-decoration-none">Participants</router-link>
                          </td>
                      </tr>
                  </tbody>
              </table>
          </div>
      </div>
  </div>
</template>

<script>
import { fetchAPI, showAlert } from '../../utils/api';

export default {
    name: 'StaffTreks',
    data() {
        return {
            treks: []
        };
    },
    mounted() {
        this.fetchAssignedTreks();
    },
    methods: {
        async fetchAssignedTreks() {
            try {
                const res = await fetchAPI("/staff/treks");
                if (res) {
                    this.treks = res;
                }
            } catch (err) {
                showAlert("Error", "Could not load assigned treks list.", "error");
            }
        }
    }
}
</script>
