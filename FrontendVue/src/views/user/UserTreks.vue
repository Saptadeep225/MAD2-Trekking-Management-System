<template>
  <div>
      <h2 class="fw-bold mb-4">Open Expeditions</h2>

      <!-- Filtering Interface -->
      <div class="card border-0 shadow-sm mb-4">
          <div class="card-body p-3">
              <form @submit.prevent="fetchTreks" class="row g-2">
                  <div class="col-md-4">
                      <input type="text" v-model="filter.search" class="form-control form-control-sm border-0 bg-light" placeholder="Search by route name...">
                  </div>
                  <div class="col-md-3">
                      <input type="text" v-model="filter.location" class="form-control form-control-sm border-0 bg-light" placeholder="Search by location...">
                  </div>
                  <div class="col-md-3">
                      <select v-model="filter.difficulty" class="form-select form-select-sm border-0 bg-light">
                          <option value="">Any Difficulty</option>
                          <option value="Easy">Easy</option>
                          <option value="Moderate">Moderate</option>
                          <option value="Hard">Hard</option>
                      </select>
                  </div>
                  <div class="col-md-2">
                      <button type="submit" class="btn btn-primary btn-sm w-100 rounded-pill fw-semibold">Filter Routes</button>
                  </div>
              </form>
          </div>
      </div>

      <!-- Treks Grid -->
      <div class="row g-4">
          <div class="col-md-12 text-center py-5 text-muted" v-if="treks.length === 0">
              <i class="bi bi-binoculars fs-1"></i>
              <p class="mt-3">No active itineraries match selection criteria.</p>
          </div>
          <div class="col-md-4" v-for="trek in treks" :key="trek.id">
              <div class="card border-0 shadow-sm h-100 overflow-hidden hover-card">
                  <div class="p-3 bg-primary text-white d-flex justify-content-between align-items-center">
                      <span class="small uppercase tracking-wider fw-medium"><i class="bi bi-geo-alt-fill me-1"></i>{{ trek.location }}</span>
                      <span class="badge rounded-pill" :class="{
                          'bg-success': trek.difficulty === 'Easy',
                          'bg-warning text-dark': trek.difficulty === 'Moderate',
                          'bg-danger': trek.difficulty === 'Hard'
                      }">{{ trek.difficulty }}</span>
                  </div>
                  <div class="card-body p-4 d-flex flex-column">
                      <h4 class="fw-bold mb-2">{{ trek.name }}</h4>
                      <p class="text-muted small flex-grow-1">{{ trek.description }}</p>
                      <hr class="text-light-emphasis">
                      <div class="d-flex justify-content-between text-muted small mb-3">
                          <span><i class="bi bi-clock me-1"></i>{{ trek.duration }} Days</span>
                          <span><i class="bi bi-calendar2-range me-1"></i>{{ trek.start_date }}</span>
                      </div>
                      <div class="d-flex justify-content-between align-items-center">
                          <span class="small text-muted">
                              Capacity: <span class="fw-bold text-dark">{{ trek.available_slots }}</span> / {{ trek.total_slots }} slots left
                          </span>
                          <button v-if="trek.available_slots > 0" @click="bookTrek(trek.id)" class="btn btn-primary btn-sm px-3 rounded-pill fw-semibold">Book Now</button>
                          <button v-else disabled class="btn btn-secondary btn-sm px-3 rounded-pill">Sold Out</button>
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
    name: 'UserTreks',
    data() {
        return {
            treks: [],
            filter: {
                search: "",
                location: "",
                difficulty: ""
            }
        };
    },
    mounted() {
        this.fetchTreks();
    },
    methods: {
        async fetchTreks() {
            try {
                const params = new URLSearchParams();
                if (this.filter.search) params.append("search", this.filter.search);
                if (this.filter.location) params.append("location", this.filter.location);
                if (this.filter.difficulty) params.append("difficulty", this.filter.difficulty);
                
                const res = await fetchAPI(`/user/treks?${params.toString()}`);
                if (res) {
                    this.treks = res;
                }
            } catch (err) {
                showAlert("Error", "Could not fetch treks list.", "error");
            }
        },
        async bookTrek(id) {
            try {
                const res = await fetchAPI(`/user/book/${id}`, { method: "POST" });
                showAlert("Booking Confirmed", res.message, "success");
                this.fetchTreks();
            } catch (err) {
                showAlert("Booking Failed", err.message, "error");
            }
        }
    }
}
</script>
