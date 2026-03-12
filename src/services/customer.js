// src/services/customer.js
import apiClient from '../utils/axios';

const API_CUSTOMERS = '/api/customers';

export const customerService = {
    getCustomers: (skip = 0, limit = 100) =>
        apiClient.get(`${API_CUSTOMERS}?skip=${skip}&limit=${limit}`),
    createCustomer: (data) =>
        apiClient.post(API_CUSTOMERS, data),
    updateCustomer: (id, data) =>
        apiClient.put(`${API_CUSTOMERS}/${id}`, data),
    deleteCustomer: (id) =>
        apiClient.delete(`${API_CUSTOMERS}/${id}`)
};