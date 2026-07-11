<template>
  <div>
      <h2 class="fw-bold mb-4">Guides Directory</h2>
      
      <div class="row g-4 mb-5">
          <div class="col-lg-8">
              <div class="card border-0 shadow-sm overflow-hidden">
                  <div class="card-header bg-transparent border-0 pt-4 px-4 d-flex justify-content-between align-items-center">
                      <h5 class="fw-bold mb-0">Coordinating Guides</h5>
                  </div>
                  <div class="card-body px-0 py-0">
                      <div class="table-responsive">
                          <table class="table table-hover align-middle mb-0">
                              <thead class="table-light text-muted uppercase small">
                                  <tr>
                                      <th class="px-4">Guide ID</th>
                                      <th>Name</th>
                                      <th>Username</th>
                                      <th>Email</th>
                                      <th>Phone</th>
                                      <th>Status</th>
                                      <th class="text-end px-4">Actions</th>
                                  </tr>
                              </thead>
                              <tbody>
                                  <tr v-if="staff.length === 0">
                                      <td colspan="7" class="text-center py-4 text-muted">No staff accounts registered.</td>
                                  </tr>
                                  <tr v-for="member in staff" :key="member.id">
                                      <td class="px-4 text-muted">#{{ member.id }}</td>
                                      <td><span class="fw-semibold">{{ member.name }}</span></td>
                                      <td>{{ member.username }}</td>
                                      <td>{{ member.email }}</td>
                                      <td>{{ member.phone }}</td>
                                      <td>
                                          <span class="badge" :class="{
                                              'bg-success-subtle text-success': member.status === 'approved',
                                              'bg-warning-subtle text-warning-emphasis': member.status === 'pending',
                                              'bg-danger-subtle text-danger': member.status === 'blacklisted'
                                          }">{{ member.status }}</span>
                                      </td>
                                      <td class="text-end px-4">
                                          <button v-if="member.status === 'pending'" @click="approveStaff(member.id)" class="btn btn-success btn-sm rounded-pill px-3 me-2">Approve</button>
                                          <button v-if="member.status === 'blacklisted'" @click="unblacklistStaff(member.id)" class="btn btn-outline-warning btn-sm rounded-pill px-3 me-2">Restore</button>
                                          <button v-if="member.status === 'approved'" @click="blacklistStaff(member.id)" class="btn btn-outline-danger btn-sm rounded-pill px-3">Deactivate</button>
                                      </td>
                                  </tr>
                              </tbody>
                          </table>
                      </div>
                  </div>
              </div>
          </div>
          <div class="col-lg-4">
              <div class="card border-0 shadow-sm p-2">
                  <div class="card-body">
                      <h5 class="fw-bold mb-3">Add Guide Account</h5>
                      <form @submit.prevent="addStaff">
                          <div class="mb-3">
                              <label class="form-label fw-medium">Full Name</label>
                              <input type="text" v-model="newStaff.name" class="form-control form-control-sm" required placeholder="e.g. Rahul Sharma">
                          </div>
                          <div class="mb-3">
                              <label class="form-label fw-medium">Username</label>
                              <input type="text" v-model="newStaff.username" class="form-control form-control-sm" required placeholder="e.g. rahul_guide">
                          </div>
                          <div class="mb-3">
                              <label class="form-label fw-medium">Email Address</label>
                              <input type="email" v-model="newStaff.email" class="form-control form-control-sm" required placeholder="e.g. guide@trek.com">
                          </div>
                          <div class="mb-3">
                              <label class="form-label fw-medium">Phone</label>
                              <input type="text" v-model="newStaff.phone" class="form-control form-control-sm" placeholder="e.g. 9876543210">
                          </div>
                          <div class="mb-4">
                              <label class="form-label fw-medium">Temporary Password</label>
                              <input type="password" v-model="newStaff.password" class="form-control form-control-sm" required minlength="6" placeholder="Min 6 characters">
                          </div>
                          <button type="submit" class="btn btn-primary w-100 rounded-pill btn-sm fw-semibold shadow-sm">
                              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                              Create Staff User
                          </button>
                      </form>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import { fetchAPI, showAlert } from '../../utils/api';

export default {
    name: 'AdminStaff',
    data() {
        return {
            staff: [],
            newStaff: {
                name: "",
                username: "",
                email: "",
                phone: "",
                password: ""
            },
            loading: false
        };
    },
    mounted() {
        this.fetchStaff();
    },
    methods: {
        async fetchStaff() {
            try {
                const res = await fetchAPI("/admin/staff");
                if (res) {
                    this.staff = res;
                }
            } catch (err) {
                showAlert("Error", "Could not load guides directory.", "error");
            }
        },
        async addStaff() {
            this.loading = true;
            try {
                await fetchAPI("/admin/staff/add", {
                    method: "POST",
                    body: JSON.stringify(this.newStaff)
                });
                showAlert("Success", "New staff account added successfully.", "success");
                this.newStaff = { name: "", username: "", email: "", phone: "", password: "" };
                this.fetchStaff();
            } catch (err) {
                showAlert("Failed to Add Staff", err.message, "error");
            } finally {
                this.loading = false;
            }
        },
        async approveStaff(id) {
            try {
                await fetchAPI(`/admin/staff/approve/${id}`, { method: "POST" });
                showAlert("Approved", "Staff account approved successfully.", "success");
                this.fetchStaff();
            } catch (err) {
                showAlert("Error", err.message, "error");
            }
        },
        async blacklistStaff(id) {
            try {
                await fetchAPI(`/admin/staff/blacklist/${id}`, { method: "POST" });
                showAlert("Deactivated", "Staff account deactivated.", "success");
                this.fetchStaff();
            } catch (err) {
                showAlert("Error", err.message, "error");
            }
        },
        async unblacklistStaff(id) {
            try {
                await fetchAPI(`/admin/staff/unblacklist/${id}`, { method: "POST" });
                showAlert("Restored", "Staff account restored successfully.", "success");
                this.fetchStaff();
            } catch (err) {
                showAlert("Error", err.message, "error");
            }
        }
    }
}
</script>
