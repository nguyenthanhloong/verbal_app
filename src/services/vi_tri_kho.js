// src/services/vi_tri_kho.js
import apiClient from '../utils/axios';

const API_VITRIKHO = '/api/vi-tri-kho';

export const viTriKhoService = {
    getViTriKho: () =>
        apiClient.get(API_VITRIKHO),

    createViTriKho: (data) =>
        apiClient.post(API_VITRIKHO, data),

    updateViTriKho: (id, data) =>
        apiClient.put(`${API_VITRIKHO}/${id}`, data),

    deleteViTriKho: (id) =>
        apiClient.delete(`${API_VITRIKHO}/${id}`)
};