<template>
  <AdminLayout>
    <div class="page-header">
      <div class="title-group">
        <Users class="title-icon" />
        <h2>Quản lý Người Dùng</h2>
      </div>
      <div class="header-actions">
        <button @click="openUserModal()" class="btn btn-primary">
          <Plus class="icon-sm" /> Thêm Người Dùng
        </button>
      </div>
    </div>

    <div class="card">
      <div class="table-responsive">
        <table class="data-table">
          <thead>
            <tr>
              <th width="80">ID</th>
              <th>Tài khoản</th>
              <th>Họ & Tên</th>
              <th>Vai trò (Roles)</th>
              <th class="text-center" width="150">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>#{{ user.id }}</td>
              <td>
                <strong class="text-primary">{{ user.username }}</strong>
              </td>
              <td>{{ user.full_name }}</td>
              <td>
                <div class="badges-wrapper">
                  <span
                    v-for="role in user.roles"
                    :key="role.id"
                    class="badge role-badge"
                  >
                    {{ role.name }}
                  </span>
                  <span v-if="!user.roles.length" class="text-muted">
                    Chưa phân quyền
                  </span>
                </div>
              </td>
              <td class="text-center actions-cell">
                <button
                  @click="openUserModal(user)"
                  class="btn btn-sm btn-secondary btn-icon-only"
                  title="Sửa thông tin"
                >
                  <Edit class="icon-sm" />
                </button>
                <button
                  @click="openRoleModal(user)"
                  class="btn btn-sm btn-save btn-icon-only"
                  title="Gán Vai trò"
                >
                  <Shield class="icon-sm" />
                </button>
              </td>
            </tr>

            <tr v-if="users.length === 0">
              <td colspan="5" class="text-center text-muted empty-row">
                Chưa có dữ liệu người dùng.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="pagination-container" v-if="totalUsers > 0">
        <div class="pagination-info">
          Hiển thị {{ (currentPage - 1) * limit + 1 }} đến
          {{ Math.min(currentPage * limit, totalUsers) }} trong tổng số
          <strong>{{ totalUsers }}</strong> người dùng
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

    <div v-if="showRoleModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content modal-lg">
        <div class="modal-header">
          <h3>
            Gán Vai trò cho:
            <span class="text-primary">{{ selectedUser?.username }}</span>
          </h3>
          <button @click="closeModal" class="btn-close">
            <X class="icon-sm" />
          </button>
        </div>

        <p class="text-muted mb-3">
          Chọn các vai trò bạn muốn cấp cho người dùng này:
        </p>

        <div class="roles-grid scrollable-grid">
          <label
            v-for="role in allRoles"
            :key="role.id"
            class="checkbox-label"
            :class="{ 'is-checked': checkedRoleIds.includes(role.id) }"
          >
            <input type="checkbox" :value="role.id" v-model="checkedRoleIds" />
            <div class="role-info">
              <span class="role-name">{{ role.name }}</span>
              <span class="role-code">{{ role.code }}</span>
            </div>
          </label>
        </div>

        <div class="modal-actions">
          <button @click="closeModal" class="btn btn-secondary">Hủy bỏ</button>
          <button
            @click="confirmSaveRoles"
            :disabled="isSaving"
            class="btn btn-save"
          >
            <Save class="icon-sm" v-if="!isSaving" />
            {{ isSaving ? 'Đang lưu...' : 'Lưu Thay Đổi' }}
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="showUserModal"
      class="modal-overlay"
      @click.self="showUserModal = false"
    >
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ isEditUser ? 'Sửa thông tin User' : 'Tạo User Mới' }}</h3>
          <button @click="showUserModal = false" class="btn-close">
            <X class="icon-sm" />
          </button>
        </div>

        <form @submit.prevent="confirmSaveUser">
          <div class="form-group">
            <label>
              Tên đăng nhập (Username)
              <span class="text-danger" v-if="!isEditUser">*</span>
            </label>
            <input
              type="text"
              v-model="userForm.username"
              :disabled="isEditUser"
              required
              placeholder="Nhập tên tài khoản"
            />
          </div>
          <div class="form-group">
            <label>Họ và Tên</label>
            <input
              type="text"
              v-model="userForm.full_name"
              required
              placeholder="VD: Nguyễn Văn A..."
            />
          </div>
          <div class="form-group">
            <label>
              Mật khẩu {{ isEditUser ? '(Bỏ trống nếu không đổi)' : '*' }}
            </label>
            <input
              type="password"
              v-model="userForm.password"
              :required="!isEditUser"
              placeholder="Nhập mật khẩu..."
            />
          </div>

          <div class="modal-actions">
            <button
              type="button"
              @click="showUserModal = false"
              class="btn btn-secondary"
            >
              Hủy
            </button>
            <button type="submit" class="btn btn-save" :disabled="isSavingUser">
              <Save class="icon-sm" v-if="!isSavingUser" />
              {{ isSavingUser ? 'Đang lưu...' : 'Lưu lại' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <ConfirmModal
      :isOpen="showConfirm"
      :title="confirmTitle"
      :message="confirmMessage"
      @confirm="handleConfirm"
      @cancel="showConfirm = false"
    />
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { adminService } from '../services/admin';
import AdminLayout from '../layouts/AdminLayout.vue';
import ConfirmModal from '../components/ConfirmModal.vue'; // Import Confirm Modal
import { useToast } from '../composables/useToast'; // Import Toast
import {
  Users,
  Plus,
  Shield,
  Edit,
  Save,
  X,
  ChevronLeft,
  ChevronRight,
} from 'lucide-vue-next';

const toast = useToast();

// --- STATE QUẢN LÝ CONFIRM MODAL ---
const showConfirm = ref(false);
const confirmTitle = ref('');
const confirmMessage = ref('');
const confirmActionType = ref(''); // Lưu cờ để biết đang xác nhận cho thao tác nào ('user' hay 'roles')

// --- LOGIC QUẢN LÝ USER ---
const showUserModal = ref(false);
const isEditUser = ref(false);
const isSavingUser = ref(false);
const editUserId = ref(null);
const userForm = ref({ username: '', full_name: '', password: '' });

const users = ref([]);
const allRoles = ref([]);
const totalUsers = ref(0);

// Cấu hình Phân trang
const currentPage = ref(1);
const limit = ref(5); // Số lượng user hiển thị trên 1 trang (bạn đang test với số 5)

// Tính tổng số trang
const totalPages = computed(() => {
  return Math.ceil(totalUsers.value / limit.value);
});

const openUserModal = (user = null) => {
  if (user) {
    isEditUser.value = true;
    editUserId.value = user.id;
    userForm.value = {
      username: user.username,
      full_name: user.full_name,
      password: '',
    };
  } else {
    isEditUser.value = false;
    editUserId.value = null;
    userForm.value = { username: '', full_name: '', password: '' };
  }
  showUserModal.value = true;
};

// Mở Confirm khi bấm Lưu User
const confirmSaveUser = () => {
  confirmTitle.value = isEditUser.value
    ? 'Xác nhận Cập nhật'
    : 'Xác nhận Tạo mới';
  confirmMessage.value = isEditUser.value
    ? 'Bạn có chắc chắn muốn thay đổi thông tin của Người dùng này?'
    : 'Bạn có chắc chắn muốn tạo Người dùng mới này vào hệ thống?';
  confirmActionType.value = 'user';
  showConfirm.value = true;
};

// Thực thi gọi API User
const executeSaveUser = async () => {
  showConfirm.value = false;
  isSavingUser.value = true;
  try {
    if (isEditUser.value) {
      const payload = { full_name: userForm.value.full_name };
      if (userForm.value.password) payload.password = userForm.value.password;
      await adminService.updateUser(editUserId.value, payload);
      toast.success('Cập nhật thông tin Người dùng thành công!');
    } else {
      await adminService.createUser(userForm.value);
      toast.success('Tạo Người dùng mới thành công!');
      await fetchData(); // <--- Tải lại bảng với trang hiện tại
    }
    await fetchData(); // <--- Tải lại bảng với trang hiện tại
    showUserModal.value = false;
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Lỗi hệ thống!');
  } finally {
    isSavingUser.value = false;
  }
};

// --- LOGIC QUẢN LÝ QUYỀN (ROLES) CHO USER ---
// const users = ref([]);
// const allRoles = ref([]);
const showRoleModal = ref(false);
const selectedUser = ref(null);
const checkedRoleIds = ref([]);
const isSaving = ref(false);

// Hàm gọi API đã được nâng cấp
const fetchData = async () => {
  try {
    // Công thức tính skip: (Trang hiện tại - 1) * Giới hạn 1 trang
    const skip = (currentPage.value - 1) * limit.value;

    // Gọi API Roles và API Users đồng thời
    const [usersRes, rolesRes] = await Promise.all([
      adminService.getUsers(skip, limit.value),
      adminService.getRoles(),
    ]);

    // Cập nhật dữ liệu
    users.value = usersRes.data.data;
    totalUsers.value = usersRes.data.total; // Lấy tổng số user từ Backend
    allRoles.value = rolesRes.data.filter(
      (role) => role.code !== 'ROLE_SUPER_ADMIN'
    );
  } catch (error) {
    toast.error('Không thể tải dữ liệu từ máy chủ.');
  }
};

// Hàm chuyển trang
const changePage = (pageNumber) => {
  if (pageNumber >= 1 && pageNumber <= totalPages.value) {
    currentPage.value = pageNumber;
    fetchData(); // Tải lại dữ liệu trang mới
  }
};

onMounted(() => fetchData());

const openRoleModal = (user) => {
  selectedUser.value = user;
  checkedRoleIds.value = user.roles.map((r) => r.id);
  showRoleModal.value = true;
};

const closeModal = () => {
  showRoleModal.value = false;
  selectedUser.value = null;
  checkedRoleIds.value = [];
};

// Mở Confirm khi bấm Lưu Vai trò
const confirmSaveRoles = () => {
  confirmTitle.value = 'Xác nhận Cấp quyền';
  confirmMessage.value =
    'Bạn có chắc chắn muốn thay đổi Vai trò của người dùng này?';
  confirmActionType.value = 'roles';
  showConfirm.value = true;
};

// Thực thi gọi API Vai trò
const executeSaveUserRoles = async () => {
  if (!selectedUser.value) return;

  showConfirm.value = false;
  isSaving.value = true;

  try {
    await adminService.syncUserRoles(
      selectedUser.value.id,
      checkedRoleIds.value
    );
    const updatedRoles = allRoles.value.filter((r) =>
      checkedRoleIds.value.includes(r.id)
    );
    selectedUser.value.roles = updatedRoles;
    toast.success('Cập nhật Vai trò thành công!');
    closeModal();
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Lỗi khi lưu vai trò!');
  } finally {
    isSaving.value = false;
  }
};

// --- HÀM ĐIỀU PHỐI KHI BẤM "ĐỒNG Ý" Ở CONFIRM MODAL ---
const handleConfirm = () => {
  if (confirmActionType.value === 'user') {
    executeSaveUser();
  } else if (confirmActionType.value === 'roles') {
    executeSaveUserRoles();
  }
};
</script>

<style scoped>
/* CSS GIỮ NGUYÊN Y HỆT */
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

.table-responsive {
  overflow-x: auto;
}
.badges-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.role-badge {
  background-color: #f1f5f9;
  color: #334155;
  border: 1px solid #e2e8f0;
  font-weight: 500;
}
.empty-row {
  padding: 2rem !important;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}
.btn-icon-only {
  padding: 0.4rem;
  line-height: 0;
  border-radius: 6px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
}
.modal-header h3 {
  margin: 0;
  color: #0f3d26;
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
.mb-3 {
  margin-bottom: 1rem;
  display: block;
}

.modal-lg {
  max-width: 600px;
}

.scrollable-grid {
  max-height: 40vh;
  overflow-y: auto;
  padding-right: 0.5rem;
  padding-bottom: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: #ffffff;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid #e0e0e0;
  transition: all 0.2s;
}
.checkbox-label:hover {
  border-color: #4caf50;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.checkbox-label.is-checked {
  border-color: #2e7d32;
  background-color: rgba(76, 175, 80, 0.05);
}
.checkbox-label input[type='checkbox'] {
  accent-color: #2e7d32;
  margin-top: 0.25rem;
  transform: scale(1.2);
}
.role-code {
  display: block;
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 0.25rem;
  font-family: monospace;
}

/* --- PHÂN TRANG (PAGINATION) --- */
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

::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
