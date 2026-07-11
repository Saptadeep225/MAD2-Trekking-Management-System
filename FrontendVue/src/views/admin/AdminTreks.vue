<template>
  <div>
      <div class="d-flex flex-column flex-sm-row justify-content-between align-items-start align-items-sm-center mb-4 g-3">
          <h2 class="fw-bold mb-0">Trekking Itineraries</h2>
          <router-link to="/admin/treks/add" class="btn btn-primary rounded-pill px-3 shadow-sm text-decoration-none">
              <i class="bi bi-plus-lg me-1"></i> Add Itinerary
          </router-link>
      </div>

      <div class="card border-0 shadow-sm mb-4">
          <div class="card-body p-3">
              <form @submit.prevent="fetchTreks" class="row g-2">
                  <div class="col-md-8">
                      <div class="input-group">
                          <span class="input-group-text bg-light border-0"><i class="bi bi-search text-muted"></i></span>
                          <input type="text" v-model="searchQuery" class="form-control bg-light border-0" placeholder="Search by route name or location...">
                      </div>
                  </div>
                  <div class="col-md-4">
                      <button type="submit" class="btn btn-outline-primary w-100 rounded">Filter Treks</button>
                  </div>
              </form>
          </div>
      </div>

      <div class="card border-0 shadow-sm overflow-hidden">
          <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                  <thead class="table-light text-muted uppercase small">
                      <tr>
                          <th class="px-4">Route ID</th>
                          <th>Trek Name</th>
                          <th>Location</th>
                          <th>Difficulty</th>
                          <th>Duration</th>
                          <th>Slots Available</th>
                          <th>Assigned Staff</th>
                          <th>Status</th>
                          <th class="text-end px-4">Actions</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-if="treks.length === 0">
                          <td colspan="9" class="text-center py-5 text-muted">No trekking itineraries match selection.</td>
                      </tr>
                      <tr v-for="trek in treks" :key="trek.id" :class="{'table-light opacity-75 text-decoration-line-through': trek.is_deleted}">
                          <td class="px-4 text-muted">#{{ trek.id }}</td>
                          <td><span class="fw-semibold">{{ trek.name }}</span></td>
                          <td>{{ trek.location }}</td>
                          <td>
                              <span class="badge" :class="{
                                  'bg-success-subtle text-success': trek.difficulty === 'Easy',
                                  'bg-warning-subtle text-warning-emphasis': trek.difficulty === 'Moderate',
                                  'bg-danger-subtle text-danger': trek.difficulty === 'Hard'
                              }">{{ trek.difficulty }}</span>
                          </td>
                          <td>{{ trek.duration }} Days</td>
                          <td>
                              <span class="fw-bold">{{ trek.available_slots }}</span> / {{ trek.total_slots }}
                          </td>
                          <td>
                              <span v-if="trek.assigned_staff" class="badge bg-secondary-subtle text-secondary-emphasis">Coordinated</span>
                              <span v-else class="badge bg-danger-subtle text-danger">Unassigned</span>
                          </td>
                          <td>
                              <span class="badge" :class="{
                                  'bg-info': trek.status === 'Open',
                                  'bg-secondary': trek.status === 'Closed' || trek.status === 'Completed',
                                  'bg-warning': trek.status === 'Pending' || trek.status === 'Approved'
                              }">{{ trek.status }}</span>
                          </td>
                          <td class="text-end px-4">
                              <div class="btn-group" role="group">
                                  <router-link :to="'/admin/treks/edit/' + trek.id" class="btn btn-outline-secondary btn-sm" title="Edit route"><i class="bi bi-pencil"></i></router-link>
                                  <router-link :to="'/admin/treks/assign/' + trek.id" class="btn btn-outline-success btn-sm" title="Assign Guide"><i class="bi bi-person-badge"></i></router-link>
                                  <button v-if="trek.is_deleted" @click="restoreTrek(trek.id)" class="btn btn-outline-warning btn-sm" title="Restore route"><i class="bi bi-arrow-counterclockwise"></i></button>
                                  <button v-else @click="deleteTrek(trek.id)" class="btn btn-outline-danger btn-sm" title="Remove route"><i class="bi bi-trash"></i></button>
                              </div>
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
    name: 'AdminTreks',
    data() {
        return {
            treks: [],
            searchQuery: ""
        };
    },
    mounted() {
        this.fetchTreks();
    },
    methods: {
        async fetchTreks() {
            try {
                const url = this.searchQuery ? `/admin/treks?search=${encodeURIComponent(this.searchQuery)}` : "/admin/treks";
                const res = await fetchAPI(url);
                if (res) {
                    this.treks = res;
                }
            } catch (err) {
                showAlert("Error", "Could not fetch itineraries.", "error");
            }
        },
        async deleteTrek(id) {
            if (!window.Swal) return;
            window.Swal.fire({
                title: "Are you sure?",
                text: "This will soft-delete the trek itinerary.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#dc3545",
                cancelButtonColor: "#6c757d",
                confirmButtonText: "Yes, delete it"
            }).then(async (result) => {
                if (result.isConfirmed) {
                    try {
                        await fetchAPI(`/admin/treks/delete/${id}`, { method: "DELETE" });
                        showAlert("Deleted", "Trek itinerary removed successfully.", "success");
                        this.fetchTreks();
                    } catch (err) {
                        showAlert("Error", err.message, "error");
                    }
                }
            });
        },
        async restoreTrek(id) {
            try {
                await fetchAPI(`/admin/treks/restore/${id}`, { method: "POST" });
                showAlert("Restored", "Trek itinerary restored successfully.", "success");
                this.fetchTreks();
            } catch (err) {
                showAlert("Error", err.message, "error");
            }
        }
    }
}
</script>
