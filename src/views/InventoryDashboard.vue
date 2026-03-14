<template>
  <DefaultLayout>
    <div class="dashboard-wrapper">
      <button class="btn-back" @click="$router.push('/')">
        <ArrowLeft class="icon-sm" /> Về Bảng Điều Khiển
      </button>
      <div class="page-header">
        <div class="title-group">
          <!-- <BarChart3 class="title-icon" /> -->
          <h2>Bảng Thống Kê Tồn Kho</h2>
        </div>
        <p class="text-muted">
          Theo dõi số lượng hàng hóa hiện đang lưu trữ tại kho theo thời gian
          thực.
        </p>
      </div>

      <div v-if="canSwitchMode" class="admin-view-selector mb-4">
        <span class="label">Báo cáo của:</span>
        <button
          v-if="hasRegularAccess"
          :class="['btn-tab', { active: currentMode === 'THUONG' }]"
          @click="currentMode = 'THUONG'"
        >
          Khách Thường
        </button>
        <button
          v-if="hasRetailAccess"
          :class="['btn-tab', { active: currentMode === 'LE' }]"
          @click="currentMode = 'LE'"
        >
          Khách Lẻ
        </button>
      </div>

      <div
        v-if="!hasRegularAccess && !hasRetailAccess"
        class="empty-state text-center card p-5"
      >
        <ShieldAlert
          class="empty-icon mb-3"
          style="width: 48px; height: 48px; color: #f59e0b"
        />
        <h3>Tài khoản VIP không sử dụng chức năng này</h3>
        <p class="text-muted">
          Hàng hóa VIP được quản lý định danh theo từng Số Serial. Vui lòng tra
          cứu tại màn hình Lịch Sử Giao Dịch.
        </p>
        <button
          class="btn btn-primary mt-3"
          @click="$router.push('/inventory/history')"
        >
          Sang trang Lịch Sử
        </button>
      </div>

      <template v-else>
        <div class="summary-grid mb-4">
          <div class="summary-card">
            <div class="card-icon bg-blue"><Box class="icon-md" /></div>
            <div class="card-info">
              <p class="card-label">Tổng Mã Hàng Đang Tồn</p>
              <h3 class="card-value">
                {{ inventoryData.length }} <small>SKU</small>
              </h3>
            </div>
          </div>
          <div class="summary-card">
            <div class="card-icon bg-green">
              <ArrowDownToLine class="icon-md" />
            </div>
            <div class="card-info">
              <p class="card-label">Tổng Lượng Đã Nhập</p>
              <h3 class="card-value">{{ totalImport.toLocaleString() }}</h3>
            </div>
          </div>
          <div class="summary-card">
            <div class="card-icon bg-orange">
              <ArrowUpFromLine class="icon-md" />
            </div>
            <div class="card-info">
              <p class="card-label">Tổng Lượng Đã Xuất</p>
              <h3 class="card-value">{{ totalExport.toLocaleString() }}</h3>
            </div>
          </div>
          <div class="summary-card">
            <div class="card-icon bg-purple"><Layers class="icon-md" /></div>
            <div class="card-info">
              <p class="card-label">TỔNG TỒN HIỆN TẠI</p>
              <h3 class="card-value text-primary">
                {{ totalStock.toLocaleString() }}
              </h3>
            </div>
          </div>
        </div>

        <div
          class="card p-4 mb-4"
          v-if="currentMode === 'THUONG' || currentMode === 'LE'"
        >
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h3 class="m-0" style="font-size: 1.1rem; color: #1e293b">
              Biểu đồ Lưu chuyển Hàng hóa
            </h3>
            <select
              v-model="chartTimeRange"
              class="form-select form-select-sm"
              style="
                width: auto;
                padding: 6px 12px;
                border-radius: 6px;
                border: 1px solid #cbd5e1;
              "
            >
              <option value="7_days">7 Ngày qua</option>
              <option value="30_days">30 Ngày qua</option>
            </select>
          </div>

          <div style="min-height: 350px">
            <VueApexCharts
              v-if="chartSeries.length > 0"
              type="bar"
              height="350"
              :options="chartOptions"
              :series="chartSeries"
            />
            <div v-else class="text-center text-muted p-5">
              Đang tải biểu đồ...
            </div>
          </div>
        </div>

        <div class="card p-0">
          <div class="history-toolbar">
            <h3 class="m-0" style="font-size: 1.1rem">
              Chi Tiết Từng Sản Phẩm
            </h3>
            <button class="btn btn-secondary btn-sm" @click="fetchData">
              <RefreshCw class="icon-sm" :class="{ spin: isLoading }" /> Cập
              nhật
            </button>
          </div>

          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th width="80">ID Nhóm</th>
                  <th v-if="currentMode === 'THUONG'">Mã Sản Phẩm</th>
                  <th>Tên Sản Phẩm</th>
                  <th class="text-right">Tổng Nhập</th>
                  <th class="text-right">Tổng Xuất</th>
                  <th class="text-right">Tồn Kho</th>
                  <th width="200">Mức Độ Tồn</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in inventoryData" :key="item.id">
                  <td>#{{ item.id }}</td>
                  <td v-if="currentMode === 'THUONG'">
                    <strong>{{ item.ma_san_pham }}</strong>
                  </td>
                  <td>{{ item.ten_san_pham }}</td>
                  <td class="text-right text-success">
                    +{{ item.tong_nhap.toLocaleString() }}
                  </td>
                  <td class="text-right text-danger">
                    -{{ item.tong_xuat.toLocaleString() }}
                  </td>
                  <td class="text-right">
                    <span
                      class="badge"
                      style="
                        font-size: 1rem;
                        padding: 6px 12px;
                        background: #0f3d26;
                        color: white;
                      "
                    >
                      {{ item.ton_kho.toLocaleString() }}
                    </span>
                  </td>
                  <td>
                    <div
                      class="stock-bar-container"
                      :title="`Còn lại ${Math.round(
                        (item.ton_kho / item.tong_nhap) * 100
                      )}%`"
                    >
                      <div
                        class="stock-bar-fill"
                        :style="{
                          width: `${(item.ton_kho / item.tong_nhap) * 100}%`,
                        }"
                      ></div>
                    </div>
                  </td>
                </tr>
                <tr v-if="inventoryData.length === 0 && !isLoading">
                  <td colspan="7" class="text-center p-5 text-muted">
                    Kho hiện tại đang trống. Không có sản phẩm nào tồn kho.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useToast } from '../composables/useToast';
import { inventoryService } from '../services/inventory';
import DefaultLayout from '../layouts/DefaultLayout.vue';
import VueApexCharts from 'vue3-apexcharts';
import {
  BarChart3,
  Box,
  ArrowDownToLine,
  ArrowUpFromLine,
  Layers,
  RefreshCw,
  ShieldAlert,
  ArrowLeft,
} from 'lucide-vue-next';

// ==========================================
// 1. KHAI BÁO TOÀN BỘ BIẾN (STATE) LÊN TRÊN CÙNG
// ==========================================
const authStore = useAuthStore();
const toast = useToast();

const currentMode = ref(''); // CHUYỂN LÊN ĐÂY ĐỂ TRÁNH LỖI REFERENCE
const inventoryData = ref([]);
const isLoading = ref(false);

const chartTimeRange = ref('7_days');
const chartSeries = ref([]);
const chartOptions = ref({
  chart: { type: 'bar', height: 350, toolbar: { show: false } },
  colors: ['#10b981', '#ef4444'],
  plotOptions: {
    bar: { horizontal: false, columnWidth: '55%', borderRadius: 4 },
  },
  dataLabels: { enabled: false },
  stroke: { show: true, width: 2, colors: ['transparent'] },
  xaxis: { categories: [] },
  yaxis: { title: { text: 'Số lượng (Sản phẩm)' } },
  fill: { opacity: 1 },
  tooltip: {
    y: {
      formatter: function (val) {
        return val + ' sản phẩm';
      },
    },
  },
});

// Quyền hạn
const isAdmin = computed(() => authStore.hasPermission('FUNC_ADMIN_ALL'));
const hasRegularAccess = computed(
  () =>
    isAdmin.value ||
    authStore.hasPermission('FUNC_THUONG_NHAP') ||
    authStore.hasPermission('FUNC_THUONG_XUAT')
);
const hasRetailAccess = computed(
  () =>
    isAdmin.value ||
    authStore.hasPermission('FUNC_LE_NHAP') ||
    authStore.hasPermission('FUNC_LE_XUAT')
);
const canSwitchMode = computed(
  () => hasRegularAccess.value && hasRetailAccess.value
);

// Tính tổng
const totalImport = computed(() =>
  inventoryData.value.reduce((sum, item) => sum + item.tong_nhap, 0)
);
const totalExport = computed(() =>
  inventoryData.value.reduce((sum, item) => sum + item.tong_xuat, 0)
);
const totalStock = computed(() =>
  inventoryData.value.reduce((sum, item) => sum + item.ton_kho, 0)
);

// ==========================================
// 2. KHAI BÁO CÁC HÀM XỬ LÝ (FUNCTIONS)
// ==========================================
const fetchChartData = async () => {
  if (!currentMode.value) return;

  try {
    let response;

    // Tùy theo đang ở Tab nào mà gọi API đó
    if (currentMode.value === 'THUONG') {
      response = await inventoryService.getChartDataRegular(
        chartTimeRange.value
      );
    } else if (currentMode.value === 'LE') {
      response = await inventoryService.getChartDataRetail(
        chartTimeRange.value
      );
    }

    if (response) {
      const data = response.data;

      chartOptions.value = {
        ...chartOptions.value,
        xaxis: { categories: data.labels },
      };
      chartSeries.value = [
        { name: 'Tổng Nhập', data: data.datasets.nhap },
        { name: 'Tổng Xuất', data: data.datasets.xuat },
      ];
    }
  } catch (error) {
    // console.error('Lỗi khi tải biểu đồ:', error);
  }
};

const fetchData = async () => {
  if (!currentMode.value) return;
  isLoading.value = true;
  inventoryData.value = [];

  try {
    let response;
    if (currentMode.value === 'THUONG')
      response = await inventoryService.getInventoryRegular();
    else if (currentMode.value === 'LE')
      response = await inventoryService.getInventoryRetail();

    if (response) inventoryData.value = response.data.data;
  } catch (error) {
    // console.error('Lỗi tải tồn kho:', error);
    toast.error('Không thể tải dữ liệu tồn kho!');
  } finally {
    isLoading.value = false;
  }
};

// ==========================================
// 3. THEO DÕI VÀ VÒNG ĐỜI (WATCHERS & LIFECYCLE)
// ==========================================
watch(chartTimeRange, () => {
  fetchChartData();
});

watch(currentMode, () => {
  fetchData();
  fetchChartData();
});

onMounted(() => {
  if (hasRegularAccess.value) currentMode.value = 'THUONG';
  else if (hasRetailAccess.value) currentMode.value = 'LE';

  if (currentMode.value) {
    fetchData();
    fetchChartData();
  }
});
</script>

<style scoped>
/* Toàn bộ CSS giữ nguyên */
.dashboard-wrapper {
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
.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
.summary-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
.bg-blue {
  background-color: #3b82f6;
}
.bg-green {
  background-color: #10b981;
}
.bg-orange {
  background-color: #f59e0b;
}
.bg-purple {
  background-color: #8b5cf6;
}
.card-label {
  margin: 0;
  font-size: 0.85rem;
  color: #64748b;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}
.card-value {
  margin: 5px 0 0 0;
  font-size: 1.5rem;
  color: #1e293b;
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
.spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}
.stock-bar-container {
  width: 100%;
  height: 8px;
  background-color: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 5px;
}
.stock-bar-fill {
  height: 100%;
  background-color: #10b981;
  border-radius: 4px;
  transition: width 0.5s ease-in-out;
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
