<template>
  <component :is="currentLayout">
    <div class="dashboard-wrapper">
      <div class="mb-4">
        <button class="btn-back" @click="$router.push('/')">
          <ArrowLeft class="icon-sm" /> Về Bảng Điều Khiển
        </button>
      </div>

      <div class="page-header">
        <div class="title-group">
          <MapPin class="title-icon" />
          <h2>Danh mục Vị trí Kho</h2>
        </div>
        <div class="header-actions">
          <button @click="openModal()" class="btn btn-primary">
            <Plus class="icon-sm" /> Thêm Kho Mới
          </button>
        </div>
      </div>

      <div class="card">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Mã Kho</th>
              <th>Tên Vị Trí Kho</th>
              <th>Người Tạo</th>
              <th>Ngày Tạo</th>
              <th class="text-center">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="kho in paginatedData" :key="kho.id">
              <td>{{ kho.id }}</td>
              <td>
                <span class="badge">{{ kho.ma_kho }}</span>
              </td>
              <td>
                <strong>{{ kho.ten_kho }}</strong>
              </td>
              <td>{{ kho.nguoi_tao || 'Hệ thống' }}</td>
              <td>{{ formatDate(kho.ngay_tao) }}</td>
              <td class="text-center">
                <button
                  @click="openModal(kho)"
                  class="btn btn-sm btn-secondary"
                  title="Sửa tên kho"
                >
                  <Edit class="icon-sm" /> Sửa
                </button>
              </td>
            </tr>
            <tr v-if="paginatedData.length === 0">
              <td
                colspan="6"
                class="text-center text-muted"
                style="padding: 2rem"
              >
                Chưa có dữ liệu kho hàng.
              </td>
            </tr>
          </tbody>
        </table>

        <div class="pagination-container" v-if="totalItems > 0">
          <div class="pagination-info">
            Hiển thị {{ (currentPage - 1) * limit + 1 }} đến
            {{ Math.min(currentPage * limit, totalItems) }} trong tổng số
            <strong>{{ totalItems }}</strong> kho hàng
          </div>
          <div class="pagination-actions">
            <button
              class="btn-page"
              :disabled="currentPage === 1"
              @click="changePage(currentPage - 1)"
            >
              <ChevronLeft class="icon-sm" />
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
              <ChevronRight class="icon-sm" />
            </button>
          </div>
        </div>
      </div>

      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>{{ isEdit ? 'Sửa thông tin Kho' : 'Thêm Vị trí Kho mới' }}</h3>
            <button @click="closeModal" class="btn-close">
              <X class="icon-sm" />
            </button>
          </div>

          <form @submit.prevent="confirmSave">
            <div class="form-group">
              <label
                >Mã Kho (Code)
                <span class="text-danger" v-if="!isEdit">*</span></label
              >
              <input
                type="text"
                v-model="form.ma_kho"
                :disabled="isEdit"
                required
                placeholder="VD: HCM, HN"
              />
              <small v-if="isEdit" class="text-muted"
                >Mã định danh kho không thể thay đổi.</small
              >
            </div>
            <div class="form-group">
              <label>Tên Vị trí Kho <span class="text-danger">*</span></label>
              <input
                type="text"
                v-model="form.ten_kho"
                required
                placeholder="VD: Kho Tổng Hồ Chí Minh"
              />
            </div>

            <div class="modal-actions">
              <button
                type="button"
                @click="closeModal"
                class="btn btn-secondary"
              >
                Hủy
              </button>
              <button type="submit" class="btn btn-save" :disabled="isSaving">
                <Save class="icon-sm" v-if="!isSaving" />
                {{ isSaving ? 'Đang lưu...' : 'Lưu lại' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <ConfirmModal
        :isOpen="showConfirm"
        :title="isEdit ? 'Xác nhận Cập nhật' : 'Xác nhận Thêm mới'"
        :message="
          isEdit
            ? 'Bạn có chắc chắn muốn thay đổi Tên kho này?'
            : 'Bạn có chắc chắn muốn tạo mã Kho mới này vào hệ thống?'
        "
        @confirm="executeSave"
        @cancel="showConfirm = false"
      />
    </div>
  </component>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { viTriKhoService } from '../services/vi_tri_kho';
import AdminLayout from '../layouts/AdminLayout.vue';
import DefaultLayout from '../layouts/DefaultLayout.vue';
import ConfirmModal from '../components/ConfirmModal.vue';
import {
  MapPin,
  Plus,
  Edit,
  Save,
  X,
  ChevronLeft,
  ChevronRight,
  ArrowLeft,
} from 'lucide-vue-next';
import { useToast } from '../composables/useToast';

const authStore = useAuthStore();
const toast = useToast();

const currentLayout = computed(() =>
  authStore.hasPermission('FUNC_ADMIN_ALL') ? AdminLayout : DefaultLayout
);

const dataList = ref([]);
const showModal = ref(false);
const showConfirm = ref(false);
const isEdit = ref(false);
const isSaving = ref(false);
const currentId = ref(null);

const form = ref({ ma_kho: '', ten_kho: '' });

const currentPage = ref(1);
const limit = ref(8);
const totalItems = computed(() => dataList.value.length);
const totalPages = computed(() => Math.ceil(totalItems.value / limit.value));
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * limit.value;
  return dataList.value.slice(start, start + limit.value);
});

const changePage = (pageNumber) => {
  if (pageNumber >= 1 && pageNumber <= totalPages.value)
    currentPage.value = pageNumber;
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const d = new Date(dateString);
  return `${d.getDate().toString().padStart(2, '0')}/${(d.getMonth() + 1)
    .toString()
    .padStart(2, '0')}/${d.getFullYear()} ${d
    .getHours()
    .toString()
    .padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`;
};

const loadData = async () => {
  try {
    const res = await viTriKhoService.getViTriKho();
    dataList.value = res.data;
    if (paginatedData.value.length === 0 && currentPage.value > 1)
      currentPage.value--;
  } catch (error) {
    toast.error('Lỗi khi tải dữ liệu vị trí kho!');
  }
};

onMounted(loadData);

const openModal = (item = null) => {
  if (item) {
    isEdit.value = true;
    currentId.value = item.id;
    form.value = { ma_kho: item.ma_kho, ten_kho: item.ten_kho };
  } else {
    isEdit.value = false;
    currentId.value = null;
    form.value = { ma_kho: '', ten_kho: '' };
  }
  showModal.value = true;
};

const closeModal = () => (showModal.value = false);
const confirmSave = () => (showConfirm.value = true);

const executeSave = async () => {
  showConfirm.value = false;
  isSaving.value = true;
  try {
    if (isEdit.value) {
      await viTriKhoService.updateViTriKho(currentId.value, {
        ten_kho: form.value.ten_kho,
      });
      toast.success('Cập nhật tên kho thành công!');
    } else {
      await viTriKhoService.createViTriKho(form.value);
      toast.success('Thêm vị trí kho mới thành công!');
      currentPage.value = 1;
    }
    await loadData();
    closeModal();
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Lỗi khi lưu dữ liệu!');
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
/* WRAPPER GIỚI HẠN CHIỀU RỘNG */
.dashboard-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

/* NÚT QUAY LẠI */
.mb-4 {
  margin-bottom: 1.5rem;
}
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

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.title-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #0f3d26;
}
.title-icon {
  width: 28px;
  height: 28px;
  color: #2e7d32;
}
.title-group h2 {
  margin: 0;
  font-size: 1.5rem;
}
.icon-sm {
  width: 16px;
  height: 16px;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
}
.modal-header h3 {
  margin: 0;
}
.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #aaa;
  transition: 0.2s;
  display: flex;
  align-items: center;
}
.btn-close:hover {
  color: #ef4444;
}
.text-center {
  text-align: center;
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
</style>
