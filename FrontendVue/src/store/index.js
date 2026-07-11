import { reactive } from 'vue';

export const store = reactive({
    token: localStorage.getItem("access_token"),
    role: localStorage.getItem("role"),
    user: JSON.parse(localStorage.getItem("user") || "null"),
    setToken(token) {
        this.token = token;
        if (token) localStorage.setItem("access_token", token);
        else localStorage.removeItem("access_token");
    },
    setRole(role) {
        this.role = role;
        if (role) localStorage.setItem("role", role);
        else localStorage.removeItem("role");
    },
    setUser(user) {
        this.user = user;
        if (user) localStorage.setItem("user", JSON.stringify(user));
        else localStorage.removeItem("user");
    },
    clear() {
        this.token = null;
        this.role = null;
        this.user = null;
        localStorage.clear();
    }
});
