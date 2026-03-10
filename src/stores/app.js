import { defineStore } from 'pinia';

export const useAppStore = defineStore('app', {
    state: () => ({
        isLoading: false,
        requestCount: 0, // Đếm số lượng API đang được gọi
    }),

    actions: {
        startLoading() {
            this.requestCount++;
            this.isLoading = true;
        },
        stopLoading() {
            if (this.requestCount > 0) {
                this.requestCount--;
            }
            // Chỉ tắt vòng xoay khi TẤT CẢ các API đều đã trả về kết quả
            if (this.requestCount === 0) {
                this.isLoading = false;
            }
        }
    }
});