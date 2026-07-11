<template>
  <div>
      <h2 class="fw-bold mb-4">Trekkers Directory</h2>

      <div class="card border-0 shadow-sm mb-4">
          <div class="card-body p-3">
              <form @submit.prevent="fetchUsers" class="row g-2">
                  <div class="col-md-9">
                      <div class="input-group">
                          <span class="input-group-text bg-light border-0"><i class="bi bi-search text-muted"></i></span>
                          <input type="text" v-model="searchQuery" class="form-control bg-light border-0" placeholder="Search by name or username...">
                      </div>
                  </div>
                  <div class="col-md-3">
                      <button type="submit" class="btn btn-outline-primary w-100">Filter list</button>
                  </div>
              </form>
          </div>
      </div>

      <div class="card border-0 shadow-sm overflow-hidden">
          <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                  <thead class="table-light text-muted uppercase small">
                      <tr>
                          <th class="px-4">Trekker ID</th>
                          <th>Name</th>
                          <th>Username</th>
                          <th>Email</th>
                          <th>Phone</th>
                          <th>Status</th>
                          <th class="text-end px-4">Actions</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-if="users.length === 0">
                          <td colspan="7" class="text-center py-4 text-muted">No trekkers matching criteria.</td>
                      </tr>
                      <tr v-for="user in users" :key="user.id">
                          <td class="px-4 text-muted">#{{ user.id }}</td>
                          <td><span class="fw-semibold">{{ user.name }}</span></td>
                          <td>{{ user.username }}</td>
                          <td>{{ user.email }}</td>
                          <td>{{ user.phone }}</td>
                          <td>
                              <span class="badge" :class="{
                                  'bg-success-subtle text-success': user.status === 'approved',
                                  'bg-danger-subtle text-danger': user.status === 'blacklisted'
                              }">{{ user.status }}</span>
                          </td>
                          <td class="text-end px-4">
                              <button v-if="user.status === 'blacklisted'" @click="unblacklistUser(user.id)" class="btn btn-outline-warning btn-sm rounded-pill px-3">Restore</button>
                              <button v-else @click="blacklistUser(user.id)" class="btn btn-outline-danger btn-sm rounded-pill px-3">Deactivate</button>
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
    name: 'AdminUsers',
    data() {
        return {
            users: [],
            searchQuery: ""
        };
    },
    mounted() {
        this.fetchUsers();
    },
    methods: {
        async fetchUsers() {
            try {
                const url = this.searchQuery ? `/admin/users?search=${encodeURIComponent(this.searchQuery)}` : "/admin/users";
                const res = await fetchAPI(url);
                if (res) {
                    this.users = res;
                }
            } catch (err) {
                showAlert("Error", "Could not load trekkers directory.", "error");
            }
        },
        async blacklistUser(id) {
            try {
                await fetchAPI(`/admin/users/blacklist/${id}`, { method: "POST" });
                showAlert("Deactivated", "Trekker profile deactivated.", "success");
                this.fetchUsers();
            } catch (err) {
                showAlert("Error", err.message, "error");
            }
        },
        async unblacklistUser(id) {
            try {
                await fetchAPI(`/admin/users/unblacklist/${id}`, { method: "POST" });
                showAlert("Restored", "Trekker profile restored successfully.", "success");
                this.fetchUsers();
            } catch (err) {
                showAlert("Error", err.message, "error");
            }
        }
    }
}
</script>
