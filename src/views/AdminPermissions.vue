<template>
  <AdminLayout>
    <div class="page-header">
      <div class="title-group">
        <Key class="title-icon" />
        <h2>Quản lý Chức Năng & Quyền (Permissions)</h2>
      </div>
      <div class="header-actions">
        <button @click="openModal()" class="btn btn-primary">
          <Plus class="icon-sm" /> Thêm Quyền Mới
        </button>
      </div>
    </div>

    <div class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Mã Quyền (Code)</th>
            <th>Tên Quyền</th>
            <th>Mô tả</th>
            <th class="text-center">Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="perm in paginatedPermissions" :key="perm.id">
            <td>{{ perm.id }}</td>
            <td>
              <span class="badge">{{ perm.code }}</span>
            </td>
            <td>
              <strong>{{ perm.name }}</strong>
            </td>
            <td>{{ perm.description }}</td>
            <td class="text-center">
              <button
                @click="openModal(perm)"
                class="btn btn-sm btn-secondary"
                title="Sửa quyền"
              >
                <Edit class="icon-sm" /> Sửa
              </button>
            </td>
          </tr>
          <tr v-if="paginatedPermissions.length === 0">
            <td
              colspan="5"
              class="text-center text-muted"
              style="padding: 2rem"
            >
              Chưa có dữ liệu chức năng.
            </td>
          </tr>
        </tbody>
      </table>
      <div class="pagination-container" v-if="totalItems > 0">
        <div class="pagination-info">
          Hiển thị {{ (currentPage - 1) * limit + 1 }} đến
          {{ Math.min(currentPage * limit, totalItems) }} trong tổng số
          <strong>{{ totalItems }}</strong> chức năng
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
          <h3>{{ isEdit ? 'Sửa thông tin Quyền' : 'Thêm Quyền Mới' }}</h3>
          <button @click="closeModal" class="btn-close">
            <X class="icon-sm" />
          </button>
        </div>

        <form @submit.prevent="confirmSave">
          <div class="form-group">
            <label>
              Mã Quyền (Code)
              <span class="text-danger" v-if="!isEdit">*</span>
            </label>
            <input
              type="text"
              v-model="form.code"
              :disabled="isEdit"
              required
              placeholder="VD: FUNC_VIP_NHAP_MOI"
            />
            <small v-if="isEdit" class="text-muted"
              >Không thể sửa mã Code sau khi tạo.</small
            >
          </div>
          <div class="form-group">
            <label>Tên hiển thị</label>
            <input
              type="text"
              v-model="form.name"
              required
              placeholder="VD: Nhập kho VIP"
            />
          </div>
          <div class="form-group">
            <label>Mô tả chi tiết</label>
            <textarea v-model="form.description" rows="3"></textarea>
          </div>

          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn btn-secondary">
              Hủy
            </button>
            <button type="submit" class="btn btn-save" :disabled="isSaving">
              <Save class="icon-sm" v-if="!isSaving" />
              {{ isSaving ? 'Đang chờ...' : 'Lưu lại' }}
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
          ? 'Bạn có chắc chắn muốn thay đổi thông tin của Quyền này?'
          : 'Bạn có chắc chắn muốn tạo mã Quyền mới này vào hệ thống?'
      "
      @confirm="executeSavePermission"
      @cancel="showConfirm = false"
    />
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { adminService } from '../services/admin';
import AdminLayout from '../layouts/AdminLayout.vue';
import ConfirmModal from '../components/ConfirmModal.vue'; // Import ConfirmModal
import {
  Key,
  Plus,
  Edit,
  Save,
  X,
  ChevronLeft,
  ChevronRight,
} from 'lucide-vue-next';
import { useToast } from '../composables/useToast';

const permissions = ref([]);
const showModal = ref(false);
const showConfirm = ref(false); // Biến quản lý trạng thái của Confirm Dialog
const isEdit = ref(false);
const isSaving = ref(false);
const currentId = ref(null);

const form = ref({ code: '', name: '', description: '' });
const toast = useToast();

// --- STATE PHÂN TRANG (PAGINATION) ---
const currentPage = ref(1);
const limit = ref(8); // Số lượng hiển thị trên 1 trang (đặt là 8 cho đẹp)

// Tính tổng số lượng
const totalItems = computed(() => permissions.value.length);

// Tính tổng số trang
const totalPages = computed(() => Math.ceil(totalItems.value / limit.value));

// Tính toán Mảng dữ liệu con (của riêng trang hiện tại)
const paginatedPermissions = computed(() => {
  const start = (currentPage.value - 1) * limit.value;
  const end = start + limit.value;
  // Dùng hàm slice của Array để cắt dữ liệu
  return permissions.value.slice(start, end);
});

// Hàm chuyển trang
const changePage = (pageNumber) => {
  if (pageNumber >= 1 && pageNumber <= totalPages.value) {
    currentPage.value = pageNumber;
  }
};

const loadData = async () => {
  try {
    const res = await adminService.getPermissions();
    permissions.value = res.data.filter((per) => per.code !== 'FUNC_ADMIN_ALL'); // Lưu toàn bộ vào

    // Nếu dữ liệu hiện tại làm cho trang bị trống (ví dụ: xóa item cuối cùng của trang 2), lùi về 1 trang
    if (paginatedPermissions.value.length === 0 && currentPage.value > 1) {
      currentPage.value--;
    }
  } catch (error) {
    toast.error('Lỗi khi tải dữ liệu quyền!');
  }
};

onMounted(loadData);

const openModal = (perm = null) => {
  if (perm) {
    isEdit.value = true;
    currentId.value = perm.id;
    form.value = {
      code: perm.code,
      name: perm.name,
      description: perm.description,
    };
  } else {
    isEdit.value = false;
    currentId.value = null;
    form.value = { code: '', name: '', description: '' };
  }
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

// BƯỚC 3: Hàm này chỉ làm nhiệm vụ bật cái Popup Hỏi Xác Nhận
const confirmSave = () => {
  showConfirm.value = true;
};

// BƯỚC 4: Đây mới là hàm gọi API thực sự (chạy khi user bấm Đồng ý)
const executeSavePermission = async () => {
  showConfirm.value = false; // Tắt popup hỏi
  isSaving.value = true; // Bật trạng thái loading của nút (và Global Loading)

  try {
    if (isEdit.value) {
      await adminService.updatePermission(currentId.value, {
        name: form.value.name,
        description: form.value.description,
      });
      toast.success('Cập nhật quyền thành công!'); // Báo Toast xanh
    } else {
      await adminService.createPermission(form.value);
      toast.success('Thêm quyền mới thành công!'); // Báo Toast xanh
      currentPage.value = 1;
    }
    await loadData();
    closeModal();
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Lỗi khi lưu dữ liệu!'); // Báo Toast đỏ
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
/* CSS giữ nguyên không thay đổi */
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

/* --- CSS BỔ SUNG CHO THANH PHÂN TRANG --- */
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
