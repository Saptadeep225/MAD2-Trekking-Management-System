import { store } from '../store';

export async function fetchAPI(url, options = {}) {
    const token = store.token;
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers
    };

    const response = await fetch(url, config);
    
    // Auto logout on unauthorized response
    if (response.status === 401) {
        store.clear();
        window.location.hash = "/login";
        return null;
    }

    if (response.status === 204) {
        return null;
    }

    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.message || "Something went wrong.");
    }
    return data;
}

export function showAlert(title, text, icon = "success") {
    if (window.Swal) {
        window.Swal.fire({
            title,
            text,
            icon,
            confirmButtonColor: "#093c5d"
        });
    } else {
        alert(`${title}: ${text}`);
    }
}

export function formatDateString(dateStr) {
    if (!dateStr) return "";
    const date = new Date(dateStr);
    return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
}

export function formatDateTimeString(dateTimeStr) {
    if (!dateTimeStr) return "";
    const date = new Date(dateTimeStr);
    return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' }) + " " + date.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
}
