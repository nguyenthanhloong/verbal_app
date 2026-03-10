<template>
  <DefaultLayout>
    <div class="history-wrapper">
      <button class="btn-back" @click="$router.push('/')">
        <ArrowLeft class="icon-sm" /> Về Bảng Điều Khiển
      </button>
      <div class="page-header">
        <div class="title-group">
          <!-- <History class="title-icon" /> -->
          <h2>Lịch Sử Giao Dịch</h2>
        </div>
        <p class="text-muted">
          Tra cứu lịch sử nhập, xuất và trả hàng chi tiết.
        </p>
      </div>

      <!-- <div v-if="isAdmin" class="admin-view-selector mb-4">
        <span class="label">Góc nhìn:</span>
        <button
          :class="['btn-tab', { active: currentMode === 'VIP' }]"
          @click="currentMode = 'VIP'"
        >
          Khách VIP
        </button>
        <button
          :class="['btn-tab', { active: currentMode === 'THUONG' }]"
          @click="currentMode = 'THUONG'"
        >
          Khách Thường
        </button>
        <button
          :class="['btn-tab', { active: currentMode === 'LE' }]"
          @click="currentMode = 'LE'"
        >
          Khách Lẻ
        </button>
      </div> -->

      <div v-if="showTabSelector" class="admin-view-selector mb-4">
        <span class="label">Góc nhìn:</span>
        <button
          v-if="canViewVip"
          :class="['btn-tab', { active: currentMode === 'VIP' }]"
          @click="currentMode = 'VIP'"
        >
          Khách VIP
        </button>
        <button
          v-if="canViewThuong"
          :class="['btn-tab', { active: currentMode === 'THUONG' }]"
          @click="currentMode = 'THUONG'"
        >
          Khách Thường
        </button>
        <button
          v-if="canViewLe"
          :class="['btn-tab', { active: currentMode === 'LE' }]"
          @click="currentMode = 'LE'"
        >
          Khách Lẻ
        </button>
      </div>

      <div class="card p-0">
        <div class="history-toolbar">
          <div class="action-filters">
            <template v-if="currentMode === 'VIP'">
              <button
                class="filter-btn"
                :class="{ active: actionType === 'IMPORT_NEW' }"
                @click="actionType = 'IMPORT_NEW'"
              >
                Nhập Hàng Mới
              </button>
              <button
                class="filter-btn"
                :class="{ active: actionType === 'EXPORT_NEW' }"
                @click="actionType = 'EXPORT_NEW'"
              >
                Xuất Giao Hàng
              </button>
              <button
                class="filter-btn"
                :class="{ active: actionType === 'IMPORT_OLD' }"
                @click="actionType = 'IMPORT_OLD'"
              >
                Khách Trả Cũ
              </button>
              <button
                class="filter-btn"
                :class="{ active: actionType === 'EXPORT_OLD' }"
                @click="actionType = 'EXPORT_OLD'"
              >
                Xuất Trả NCC
              </button>
            </template>
            <template v-else>
              <button
                class="filter-btn"
                :class="{ active: actionType === 'IMPORT' }"
                @click="actionType = 'IMPORT'"
              >
                Lịch Sử Nhập Kho
              </button>
              <button
                class="filter-btn"
                :class="{ active: actionType === 'EXPORT' }"
                @click="actionType = 'EXPORT'"
              >
                Lịch Sử Xuất Kho
              </button>
            </template>
          </div>

          <button class="btn btn-secondary btn-sm" @click="fetchData">
            <RefreshCw class="icon-sm" :class="{ spin: isLoading }" /> Làm mới
          </button>
        </div>

        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th width="120">Ngày GD</th>
                <th v-if="actionType !== 'IMPORT'">Mã Vận Đơn</th>
                <th>Mã Kho (SPL)</th>

                <th v-if="currentMode !== 'VIP'">ID</th>
                <th v-if="currentMode === 'VIP'">Số Serial</th>
                <th
                  v-if="
                    currentMode === 'VIP' &&
                    (actionType === 'IMPORT_NEW' || actionType === 'EXPORT_NEW')
                  "
                >
                  Mã Máy / SP
                </th>

                <th v-if="currentMode !== 'VIP'">Tên Sản Phẩm</th>
                <th v-if="currentMode !== 'VIP'" class="text-right">
                  Số Lượng
                </th>

                <th v-if="isExportAction">Người Giao / Biển Số</th>
                <th v-if="actionType === 'EXPORT_OLD'">
                  Kho Nhận / Người Nhận
                </th>

                <th>Ghi Chú</th>
                <th v-if="isExportAction" width="100" class="text-center">
                  Thao Tác
                </th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="item in tableData" :key="item.id || item.record_id">
                <td>
                  <span class="date-badge">{{ formatDate(item.ngay) }}</span>
                </td>

                <td v-if="actionType !== 'IMPORT'">
                  <strong>{{ item.ma_bill }}</strong>
                </td>

                <td>
                  <span class="badge">{{ item.ma_kho_spl }}</span>
                </td>

                <td v-if="currentMode !== 'VIP'">
                  {{ item.id }}
                </td>

                <td
                  v-if="currentMode === 'VIP'"
                  class="text-primary font-weight-bold"
                >
                  {{ item.serial_moi || item.serial_cu }}
                </td>

                <td
                  v-if="
                    currentMode === 'VIP' &&
                    (actionType === 'IMPORT_NEW' || actionType === 'EXPORT_NEW')
                  "
                >
                  {{ item.ma_may || item.ma_san_pham || 'N/A' }}
                </td>

                <td v-if="currentMode !== 'VIP'">
                  {{ item.ten_san_pham }} <br />
                  <small class="text-muted" v-if="item.ma_san_pham">{{
                    item.ma_san_pham
                  }}</small>
                </td>

                <td v-if="currentMode !== 'VIP'" class="text-right">
                  <span
                    class="badge qty-badge"
                    :class="isExportAction ? 'bg-danger' : 'bg-success'"
                  >
                    {{ isExportAction ? '-' : '+' }}{{ item.so_luong }}
                  </span>
                </td>

                <td v-if="isExportAction" style="white-space: nowrap">
                  {{ item.nv_giao_hang }}
                  <small class="text-muted" v-if="item.bien_so_xe">
                    ({{ item.bien_so_xe }})
                  </small>
                </td>

                <td
                  v-if="actionType === 'EXPORT_OLD'"
                  style="white-space: nowrap"
                >
                  {{ item.kho_tra_hang }}
                  <small class="text-muted" v-if="item.nguoi_nhan">
                    - {{ item.nguoi_nhan }}
                  </small>
                </td>

                <td>{{ item.ghi_chu || '-' }}</td>

                <td v-if="isExportAction" class="text-center">
                  <button
                    @click="downloadExcel(item.ma_bill)"
                    class="btn btn-sm btn-outline-success action-btn"
                    title="Tải Excel"
                  >
                    Tải File
                  </button>
                </td>
              </tr>

              <tr v-if="tableData.length === 0 && !isLoading">
                <td colspan="12" class="text-center text-muted empty-row">
                  Không tìm thấy dữ liệu giao dịch nào.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="pagination-container" v-if="totalItems > 0">
          <div class="pagination-info">
            Hiển thị {{ (currentPage - 1) * limit + 1 }} đến
            {{ Math.min(currentPage * limit, totalItems) }} trong tổng số
            <strong>{{ totalItems }}</strong> giao dịch
          </div>
          <div class="pagination-actions">
            <button
              class="btn-page"
              :disabled="currentPage === 1"
              @click="changePage(currentPage - 1)"
            >
              Trước
            </button>
            <button
              v-for="page in totalPages"
              :key="page"
              class="btn-page"
              :class="{ active: page === currentPage }"
              @click="changePage(page)"
            >
              {{ page }}
            </button>
            <button
              class="btn-page"
              :disabled="currentPage === totalPages"
              @click="changePage(currentPage + 1)"
            >
              Sau
            </button>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useToast } from '../composables/useToast';
import { inventoryService } from '../services/inventory';
import DefaultLayout from '../layouts/DefaultLayout.vue';
import { History, RefreshCw, ArrowLeft } from 'lucide-vue-next';

const authStore = useAuthStore();
const toast = useToast();
const isAdmin = computed(() => authStore.hasPermission('FUNC_ADMIN_ALL'));

// Kiểm tra quyền Lịch sử (Dựa vào các quyền Nhập/Xuất)
const canViewVip = computed(
  () =>
    isAdmin.value ||
    authStore.hasPermission('FUNC_VIP_NHAP_MOI') ||
    authStore.hasPermission('FUNC_VIP_XUAT_MOI') ||
    authStore.hasPermission('FUNC_VIP_NHAP_CU') ||
    authStore.hasPermission('FUNC_VIP_XUAT_CU')
);
const canViewThuong = computed(
  () =>
    isAdmin.value ||
    authStore.hasPermission('FUNC_THUONG_NHAP') ||
    authStore.hasPermission('FUNC_THUONG_XUAT')
);
const canViewLe = computed(
  () =>
    isAdmin.value ||
    authStore.hasPermission('FUNC_LE_NHAP') ||
    authStore.hasPermission('FUNC_LE_XUAT')
);

const showTabSelector = computed(() => {
  return (
    [canViewVip.value, canViewThuong.value, canViewLe.value].filter(Boolean)
      .length > 1
  );
});

const currentMode = ref('VIP');
const actionType = ref('IMPORT_NEW');
const tableData = ref([]);
const isLoading = ref(false);

const currentPage = ref(1);
const limit = ref(10);
const totalItems = ref(0);

const totalPages = computed(() => Math.ceil(totalItems.value / limit.value));
const isExportAction = computed(() => actionType.value.includes('EXPORT'));

let currentRequestId = 0; // Biến đếm ID của mỗi lần gọi API

// onMounted(() => {
//   if (!isAdmin.value) {
//     if (authStore.hasPermission('FUNC_VIP_NHAP_MOI')) currentMode.value = 'VIP';
//     else if (authStore.hasPermission('FUNC_THUONG_NHAP'))
//       currentMode.value = 'THUONG';
//     else if (authStore.hasPermission('FUNC_LE_NHAP')) currentMode.value = 'LE';
//   }
//   fetchData();
// });

onMounted(() => {
  if (canViewVip.value) currentMode.value = 'VIP';
  else if (canViewThuong.value) currentMode.value = 'THUONG';
  else if (canViewLe.value) currentMode.value = 'LE';

  fetchData();
});

const fetchData = async () => {
  // Mỗi lần gọi hàm, tạo một ID duy nhất cho lượt gọi này
  currentRequestId += 1;
  const myRequestId = currentRequestId;

  isLoading.value = true;
  tableData.value = []; // Tạm xóa trắng bảng ngay khi bấm để tránh giật hình

  const skip = (currentPage.value - 1) * limit.value;
  let response = null;

  try {
    if (currentMode.value === 'VIP') {
      if (actionType.value === 'IMPORT_NEW')
        response = await inventoryService.getHistoryVipImportNew(
          skip,
          limit.value
        );
      else if (actionType.value === 'EXPORT_NEW')
        response = await inventoryService.getHistoryVipExportNew(
          skip,
          limit.value
        );
      else if (actionType.value === 'IMPORT_OLD')
        response = await inventoryService.getHistoryVipImportOld(
          skip,
          limit.value
        );
      else if (actionType.value === 'EXPORT_OLD')
        response = await inventoryService.getHistoryVipExportOld(
          skip,
          limit.value
        );
    } else if (currentMode.value === 'THUONG') {
      if (actionType.value === 'IMPORT')
        response = await inventoryService.getHistoryRegularImport(
          skip,
          limit.value
        );
      else if (actionType.value === 'EXPORT')
        response = await inventoryService.getHistoryRegularExport(
          skip,
          limit.value
        );
    } else if (currentMode.value === 'LE') {
      if (actionType.value === 'IMPORT')
        response = await inventoryService.getHistoryRetailImport(
          skip,
          limit.value
        );
      else if (actionType.value === 'EXPORT')
        response = await inventoryService.getHistoryRetailExport(
          skip,
          limit.value
        );
    }

    // CHỐT CHẶN RACE CONDITION:
    // Kiểm tra xem trong lúc API đang chạy, người dùng có bấm Tab khác không?
    // Nếu myRequestId không còn bằng currentRequestId (tức là đã có lượt bấm mới),
    // thì vứt bỏ kết quả cũ này đi, không in ra bảng nữa.
    if (myRequestId !== currentRequestId) {
      return;
    }

    if (response && response.data) {
      tableData.value = response.data.data;
      totalItems.value = response.data.total;
    }
  } catch (error) {
    if (myRequestId === currentRequestId) {
      console.error('Chi tiết lỗi khi tải dữ liệu:', error);
      toast.error('Không thể tải dữ liệu lịch sử. Vui lòng thử lại!');
    }
  } finally {
    if (myRequestId === currentRequestId) {
      isLoading.value = false;
    }
  }
};

watch(currentMode, (newMode) => {
  if (newMode === 'VIP') actionType.value = 'IMPORT_NEW';
  else actionType.value = 'IMPORT';
});

watch([currentMode, actionType], () => {
  currentPage.value = 1;
  fetchData();
});

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    fetchData();
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).format(date);
};

const downloadExcel = async (maBill) => {
  try {
    let response;
    let fileName = '';

    if (currentMode.value === 'VIP') {
      if (actionType.value === 'EXPORT_OLD') {
        response = await inventoryService.exportExcelVipOld(maBill);
        fileName = `Phieu_Xuat_Tra_${maBill}.xlsx`;
      } else if (actionType.value === 'EXPORT_NEW') {
        response = await inventoryService.exportExcelVipNew(maBill);
        fileName = `Phieu_Xuat_Giao_Hang_${maBill}.xlsx`;
      }
    } else if (currentMode.value === 'THUONG') {
      response = await inventoryService.exportExcelRegular(maBill);
      fileName = `Phieu_Xuat_Kho_Thuong_${maBill}.xlsx`;
    } else if (currentMode.value === 'LE') {
      response = await inventoryService.exportExcelRetail(maBill);
      fileName = `Phieu_Xuat_Kho_Le_${maBill}.xlsx`;
    }

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Chi tiết lỗi xuất Excel:', error);
    toast.error('Có lỗi xảy ra khi xuất file Excel! Hãy xem Console (F12).');
  }
};
</script>

<style scoped>
/* Giữ nguyên toàn bộ phần CSS mà không thay đổi gì cả */
.history-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}
.admin-view-selector {
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  padding: 12px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
.admin-view-selector .label {
  font-weight: bold;
  color: #ef4444;
  margin-right: 10px;
}
.btn-tab {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  color: #64748b;
  font-weight: 500;
  transition: all 0.2s;
}
.btn-tab:hover {
  background: #f8fafc;
}
.btn-tab.active {
  background: #0f3d26;
  color: white;
  border-color: #0f3d26;
}
.history-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
  background: #fafafa;
  border-radius: 12px 12px 0 0;
}
.action-filters {
  display: flex;
  gap: 8px;
}
.filter-btn {
  padding: 8px 16px;
  border: none;
  background: transparent;
  color: #64748b;
  font-weight: 600;
  font-size: 0.95rem;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s;
}
.filter-btn:hover {
  background: #e2e8f0;
  color: #0f3d26;
}
.filter-btn.active {
  background: #e0f2fe;
  color: #0369a1;
}
.date-badge {
  background: #f1f5f9;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #475569;
  font-weight: 500;
}
.qty-badge {
  font-size: 1rem;
  padding: 6px 12px;
}
.bg-success {
  background-color: #22c55e;
  color: white;
}
.bg-danger {
  background-color: #ef4444;
  color: white;
}
.spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}
.empty-row {
  padding: 40px !important;
}
.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.5rem;
  border-top: 1px solid #e0e0e0;
  background-color: #fafafa;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}
.pagination-info {
  font-size: 0.9rem;
  color: #64748b;
}
.pagination-info strong {
  color: #0f3d26;
}
.pagination-actions {
  display: flex;
  gap: 0.25rem;
}
.btn-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 32px;
  height: 32px;
  border: 1px solid #e2e8f0;
  background-color: #ffffff;
  color: #475569;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-page:hover:not(:disabled) {
  background-color: #f1f5f9;
  border-color: #cbd5e1;
}
.btn-page.active {
  background-color: #2e7d32;
  color: #ffffff;
  border-color: #2e7d32;
}
.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #f8fafc;
}
.action-btn {
  padding: 4px 10px;
  font-size: 0.85rem;
  border-radius: 4px;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  border: 1px solid #22c55e;
  color: #22c55e;
  background: white;
  transition: all 0.2s;
}
.action-btn:hover {
  background-color: #22c55e;
  color: white;
}
.data-table th {
  white-space: nowrap;
}
/* NÚT QUAY LẠI */
.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  background: transparent;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  color: #64748b;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.btn-back:hover {
  background: #f8fafc;
  color: #0f3d26;
  border-color: #cbd5e1;
}

.icon-sm {
  width: 18px;
  height: 18px;
}
</style>
