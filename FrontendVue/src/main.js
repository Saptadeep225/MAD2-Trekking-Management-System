import { createApp } from 'vue';
import { createRouter, createWebHashHistory } from 'vue-router';
import App from './App.vue';
import './assets/style.css';
import { store } from './store';
import { showAlert } from './utils/api';

// Views
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import Register from './views/Register.vue';

// Admin Views
import AdminDashboard from './views/admin/AdminDashboard.vue';
import AdminTreks from './views/admin/AdminTreks.vue';
import AdminTrekForm from './views/admin/AdminTrekForm.vue';
import AdminAssignStaff from './views/admin/AdminAssignStaff.vue';
import AdminStaff from './views/admin/AdminStaff.vue';
import AdminUsers from './views/admin/AdminUsers.vue';
import AdminBookings from './views/admin/AdminBookings.vue';

// Staff Views
import StaffDashboard from './views/staff/StaffDashboard.vue';
import StaffTreks from './views/staff/StaffTreks.vue';
import StaffTrekEdit from './views/staff/StaffTrekEdit.vue';
import StaffParticipants from './views/staff/StaffParticipants.vue';

// User Views
import UserDashboard from './views/user/UserDashboard.vue';
import UserTreks from './views/user/UserTreks.vue';
import UserBookings from './views/user/UserBookings.vue';
import UserProfile from './views/user/UserProfile.vue';

const routes = [
    { path: "/", component: Home },
    { path: "/login", component: Login, meta: { guestOnly: true } },
    { path: "/register", component: Register, meta: { guestOnly: true } },
    
    // User Routes
    { path: "/user/dashboard", component: UserDashboard, meta: { requiresRole: "user" } },
    { path: "/user/treks", component: UserTreks, meta: { requiresRole: "user" } },
    { path: "/user/bookings", component: UserBookings, meta: { requiresRole: "user" } },
    { path: "/user/profile", component: UserProfile, meta: { requiresRole: "user" } },
    
    // Staff Routes
    { path: "/staff/dashboard", component: StaffDashboard, meta: { requiresRole: "staff" } },
    { path: "/staff/treks", component: StaffTreks, meta: { requiresRole: "staff" } },
    { path: "/staff/treks/update/:id", component: StaffTrekEdit, meta: { requiresRole: "staff" } },
    { path: "/staff/treks/participants/:id", component: StaffParticipants, meta: { requiresRole: "staff" } },
    
    // Admin Routes
    { path: "/admin/dashboard", component: AdminDashboard, meta: { requiresRole: "admin" } },
    { path: "/admin/treks", component: AdminTreks, meta: { requiresRole: "admin" } },
    { path: "/admin/treks/add", component: AdminTrekForm, meta: { requiresRole: "admin" } },
    { path: "/admin/treks/edit/:id", component: AdminTrekForm, meta: { requiresRole: "admin" } },
    { path: "/admin/treks/assign/:id", component: AdminAssignStaff, meta: { requiresRole: "admin" } },
    { path: "/admin/staff", component: AdminStaff, meta: { requiresRole: "admin" } },
    { path: "/admin/users", component: AdminUsers, meta: { requiresRole: "admin" } },
    { path: "/admin/bookings", component: AdminBookings, meta: { requiresRole: "admin" } }
];

const router = createRouter({
    history: createWebHashHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const isLoggedIn = !!store.token;
    const role = store.role;

    if (to.matched.some(record => record.meta.requiresRole)) {
        if (!isLoggedIn) {
            next("/login");
        } else {
            const requiredRole = to.meta.requiresRole;
            if (role !== requiredRole) {
                // Access Denied
                showAlert("Access Denied", "You do not have credentials for this console.", "warning");
                if (role === "admin") next("/admin/dashboard");
                else if (role === "staff") next("/staff/dashboard");
                else next("/user/dashboard");
            } else {
                next();
            }
        }
    } else if (to.matched.some(record => record.meta.guestOnly)) {
        if (isLoggedIn) {
            if (role === "admin") next("/admin/dashboard");
            else if (role === "staff") next("/staff/dashboard");
            else next("/user/dashboard");
        } else {
            next();
        }
    } else {
        next();
    }
});

const appInstance = createApp(App);
appInstance.use(router);
appInstance.mount("#app");
