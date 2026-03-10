// src/services/admin.js
import apiClient from '../utils/axios';

const API_RBAC = '/api/admin/rbac';

export const adminService = {
    // --- QUẢN LÝ QUYỀN (PERMISSIONS) ---
    getPermissions: () => apiClient.get(`${API_RBAC}/permissions`),
    createPermission: (data) => apiClient.post(`${API_RBAC}/permissions`, data),
    updatePermission: (id, data) => apiClient.put(`${API_RBAC}/permissions/${id}`, data),

    // --- QUẢN LÝ VAI TRÒ (ROLES) ---
    getRoles: () => apiClient.get(`${API_RBAC}/roles`),
    createRole: (data) => apiClient.post(`${API_RBAC}/roles`, data),
    updateRole: (id, data) => apiClient.put(`${API_RBAC}/roles/${id}`, data),
    syncRolePermissions: (roleId, permissionIds) =>
        apiClient.put(`${API_RBAC}/roles/${roleId}/permissions`, { ids: permissionIds }),

    // --- QUẢN LÝ NGƯỜI DÙNG (USERS) ---
    getUsers: (skip = 0, limit = 100) => apiClient.get(`${API_RBAC}/users?skip=${skip}&limit=${limit}`),
    createUser: (data) => apiClient.post(`${API_RBAC}/users`, data),
    updateUser: (id, data) => apiClient.put(`${API_RBAC}/users/${id}`, data),
    syncUserRoles: (userId, roleIds) =>
        apiClient.put(`${API_RBAC}/users/${userId}/roles`, { ids: roleIds }),
};