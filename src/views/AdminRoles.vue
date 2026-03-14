<template>
  <AdminLayout>
    <div class="page-header">
      <div class="title-group">
        <ShieldCheck class="title-icon" />
        <h2>Quản lý Vai trò & Phân quyền (RBAC)</h2>
      </div>
    </div>

    <div class="layout-grid">
      <div class="card role-sidebar">
        <div class="header-action">
          <h3>Danh sách Vai trò</h3>
          <button @click="openRoleModal()" class="btn btn-sm btn-primary">
            <Plus class="icon-sm" /> Thêm Mới
          </button>
        </div>

        <div class="scrollable-list">
          <ul class="role-list">
            <li
              v-for="role in roles"
              :key="role.id"
              @click="selectRole(role)"
              :class="{ active: selectedRole?.id === role.id }"
            >
              <div class="role-item-content">
                <strong>{{ role.name }}</strong>
                <span class="badge">{{ role.code }}</span>
              </div>
              <ChevronRight
                v-if="selectedRole?.id === role.id"
                class="active-icon"
              />
            </li>
          </ul>
        </div>
      </div>

      <div class="card role-detail" v-if="selectedRole">
        <div class="detail-header">
          <div class="role-info">
            <h3>{{ selectedRole.name }}</h3>
            <span class="badge role-badge">{{ selectedRole.code }}</span>
          </div>

          <div class="detail-actions">
            <button
              @click="openRoleModal(selectedRole)"
              class="btn btn-secondary"
            >
              <Edit class="icon-sm" /> Sửa Tên
            </button>
            <button
              @click="savePermissions"
              :disabled="isSaving"
              class="btn btn-save"
            >
              <Save class="icon-sm" v-if="!isSaving" />
              {{ isSaving ? 'Đang lưu...' : 'Lưu Phân Quyền' }}
            </button>
          </div>
        </div>

        <h4 class="section-title">Cấp phát chức năng theo nhóm:</h4>
        <p class="text-muted mb-3" style="font-size: 0.9rem">
          Tick chọn nhóm nghiệp vụ để cấp toàn bộ quyền liên quan cho vai trò
          này.
        </p>

        <div class="permissions-grouped scrollable-grid">
          <div
            v-for="(group, index) in permissionGroups"
            :key="index"
            class="perm-group-card"
            :class="{ 'is-fully-checked': isGroupChecked(group) }"
          >
            <label class="group-header-label">
              <input
                type="checkbox"
                :checked="isGroupChecked(group)"
                @change="toggleGroup(group)"
                class="group-checkbox"
              />
              <span class="group-title">{{ group.title }}</span>
            </label>

            <div class="group-children">
              <span
                v-for="perm in group.perms"
                :key="perm.id"
                class="perm-badge"
                :class="{
                  'badge-active': checkedPermissionIds.includes(perm.id),
                }"
              >
                {{ perm.name || perm.code }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="card empty-state" v-else>
        <div class="empty-content">
          <ShieldCheck class="empty-icon" />
          <p>Vui lòng chọn một Vai trò ở cột bên trái để xem và phân quyền.</p>
        </div>
      </div>
    </div>

    <div
      v-if="showRoleModal"
      class="modal-overlay"
      @click.self="showRoleModal = false"
    >
      <div class="modal-content">
        <div class="modal-header">
          <h3>
            {{ isEditRole ? 'Sửa thông tin Vai trò' : 'Tạo Vai trò mới' }}
          </h3>
          <button @click="showRoleModal = false" class="btn-close">
            <X class="icon-sm" />
          </button>
        </div>
        <form @submit.prevent="saveRole">
          <div class="form-group">
            <label
              >Mã Vai trò (Code)
              <span class="text-danger" v-if="!isEditRole">*</span></label
            >
            <input
              type="text"
              v-model="roleForm.code"
              :disabled="isEditRole"
              required
              placeholder="VD: ROLE_QUAN_LY"
            />
          </div>
          <div class="form-group">
            <label>Tên Vai trò <span class="text-danger">*</span></label>
            <input
              type="text"
              v-model="roleForm.name"
              required
              placeholder="VD: Quản lý kho"
            />
          </div>
          <div class="modal-actions">
            <button
              type="button"
              @click="showRoleModal = false"
              class="btn btn-secondary"
            >
              Hủy
            </button>
            <button type="submit" class="btn btn-save" :disabled="isSavingRole">
              <Save class="icon-sm" v-if="!isSavingRole" />
              {{ isSavingRole ? 'Đang lưu...' : 'Lưu lại' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <ConfirmModal
      :isOpen="showConfirm"
      title="Xác nhận Phân Quyền"
      message="Bạn có chắc chắn muốn thay đổi quyền hạn của Vai trò này? Điều này sẽ ảnh hưởng trực tiếp đến người dùng đang giữ vai trò này."
      @confirm="executeSavePermissions"
      @cancel="showConfirm = false"
    />
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { adminService } from '../services/admin';
import AdminLayout from '../layouts/AdminLayout.vue';
import ConfirmModal from '../components/ConfirmModal.vue';
import { useToast } from '../composables/useToast';
import {
  ShieldCheck,
  Plus,
  Edit,
  Save,
  X,
  ChevronRight,
} from 'lucide-vue-next';

const roles = ref([]);
const allPermissions = ref([]);
const selectedRole = ref(null);
const checkedPermissionIds = ref([]);
const isSaving = ref(false);

const showRoleModal = ref(false);
const isEditRole = ref(false);
const isSavingRole = ref(false);
const currentRoleId = ref(null);
const roleForm = ref({ code: '', name: '' });

const toast = useToast();
const showConfirm = ref(false);

// =========================================================
// LOGIC MỚI: TỰ ĐỘNG GOM NHÓM CÁC QUYỀN (COMPUTED)
// =========================================================
const permissionGroups = computed(() => {
  const groups = {
    VIP: { title: 'Nghiệp Vụ Khách VIP', perms: [] },
    THUONG: { title: 'Nghiệp Vụ Khách Thường', perms: [] },
    LE: { title: 'Nghiệp Vụ Khách Lẻ', perms: [] },
    MASTER_DATA: {
      title: 'Danh Mục Cơ Sở (Khách hàng, Vị trí kho)',
      perms: [],
    },
    OTHER: { title: 'Các quyền hệ thống khác', perms: [] },
  };

  // Quét danh sách quyền và nhét vào đúng nhóm dựa trên mã code
  allPermissions.value.forEach((p) => {
    if (p.code.includes('_VIP_')) groups.VIP.perms.push(p);
    else if (p.code.includes('_THUONG_')) groups.THUONG.perms.push(p);
    else if (p.code.includes('_LE_')) groups.LE.perms.push(p);
    else if (p.code.includes('_CUSTOMER_') || p.code.includes('MGR')) {
      groups.MASTER_DATA.perms.push(p);
    } else groups.OTHER.perms.push(p);
  });

  return Object.values(groups).filter((g) => g.perms.length > 0);
});

// KIỂM TRA XEM 1 NHÓM ĐÃ ĐƯỢC TICK CHƯA (Nếu có TẤT CẢ quyền con thì nhóm đó = True)
const isGroupChecked = (group) => {
  if (group.perms.length === 0) return false;
  return group.perms.every((p) => checkedPermissionIds.value.includes(p.id));
};

// HÀM TOGGLE (BẬT/TẮT) CẢ 1 NHÓM QUYỀN
const toggleGroup = (group) => {
  const groupPermIds = group.perms.map((p) => p.id);
  const currentlyChecked = isGroupChecked(group);

  if (currentlyChecked) {
    // NẾU ĐANG BẬT -> TẮT: Loại bỏ toàn bộ ID của nhóm này khỏi mảng
    checkedPermissionIds.value = checkedPermissionIds.value.filter(
      (id) => !groupPermIds.includes(id)
    );
  } else {
    // NẾU ĐANG TẮT -> BẬT: Thêm toàn bộ ID của nhóm này vào mảng (dùng Set để chống trùng lặp)
    const newIds = [...checkedPermissionIds.value, ...groupPermIds];
    checkedPermissionIds.value = [...new Set(newIds)];
  }
};
// =========================================================

onMounted(async () => {
  try {
    const [rolesRes, permsRes] = await Promise.all([
      adminService.getRoles(),
      adminService.getPermissions(),
    ]);

    roles.value = rolesRes.data.filter(
      (role) => role.code !== 'ROLE_SUPER_ADMIN'
    );
    allPermissions.value = permsRes.data.filter(
      (perm) => perm.code !== 'FUNC_ADMIN_ALL'
    );
  } catch (error) {
    toast.error('Không thể tải dữ liệu từ máy chủ.');
  }
});

const selectRole = (role) => {
  if (role.code === 'ROLE_SUPER_ADMIN') {
    toast.error(
      'Bạn không thể chỉnh sửa phân quyền của Quản trị viên tối cao!'
    );
    return;
  }
  selectedRole.value = role;
  if (role.permissions) {
    checkedPermissionIds.value = role.permissions.map((p) => p.id);
  } else {
    checkedPermissionIds.value = [];
  }
};

const openRoleModal = (role = null) => {
  if (role) {
    isEditRole.value = true;
    currentRoleId.value = role.id;
    roleForm.value = { code: role.code, name: role.name };
  } else {
    isEditRole.value = false;
    currentRoleId.value = null;
    roleForm.value = { code: 'ROLE_', name: '' };
  }
  showRoleModal.value = true;
};

const saveRole = async () => {
  isSavingRole.value = true;
  try {
    if (isEditRole.value) {
      await adminService.updateRole(currentRoleId.value, {
        name: roleForm.value.name,
      });
      toast.success('Cập nhật tên Vai trò thành công!');
    } else {
      await adminService.createRole(roleForm.value);
      toast.success('Tạo Vai trò mới thành công!');
    }
    const rolesRes = await adminService.getRoles();
    roles.value = rolesRes.data.filter(
      (role) => role.code !== 'ROLE_SUPER_ADMIN'
    );

    if (isEditRole.value && selectedRole.value?.id === currentRoleId.value) {
      selectedRole.value.name = roleForm.value.name;
    }
    showRoleModal.value = false;
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Lỗi khi lưu dữ liệu!');
  } finally {
    isSavingRole.value = false;
  }
};

const savePermissions = () => {
  showConfirm.value = true;
};

const executeSavePermissions = async () => {
  showConfirm.value = false;
  isSaving.value = true;
  try {
    await adminService.syncRolePermissions(
      selectedRole.value.id,
      checkedPermissionIds.value
    );
    const updatedPermissions = allPermissions.value.filter((p) =>
      checkedPermissionIds.value.includes(p.id)
    );
    selectedRole.value.permissions = updatedPermissions;
    toast.success('Cập nhật phân quyền thành công!');
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Có lỗi xảy ra khi lưu quyền!');
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
/* CSS GIỮ NGUYÊN CỦA BẠN (Căn chỉnh Grid) */
.layout-grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 1.5rem;
  align-items: start;
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
.scrollable-list {
  max-height: calc(100vh - 220px);
  overflow-y: auto;
  margin-top: 1rem;
  padding-right: 0.25rem;
}
.role-item-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.role-list li {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 6px;
  margin-bottom: 0.25rem;
}
.role-list li:hover {
  background: #f5f7fa;
}
.role-list li.active {
  background: rgba(76, 175, 80, 0.1);
  border-left: 4px solid #2e7d32;
}
.active-icon {
  color: #2e7d32;
  width: 20px;
  height: 20px;
}
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 1.5rem;
}
.role-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.4rem;
  color: #0f3d26;
}
.role-badge {
  background-color: #e0e0e0;
  color: #333;
  font-weight: 600;
}
.detail-actions {
  display: flex;
  gap: 0.75rem;
}
.section-title {
  color: #0f3d26;
  margin-bottom: 0.5rem;
}

/* CSS MỚI CHO GOM NHÓM QUYỀN */
.permissions-grouped {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.perm-group-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.25rem;
  transition: all 0.3s ease;
}
.perm-group-card.is-fully-checked {
  border-color: #4caf50;
  background-color: #f8fff9;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
}
.group-header-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  margin-bottom: 12px;
  user-select: none;
}
.group-checkbox {
  width: 20px;
  height: 20px;
  accent-color: #2e7d32;
  cursor: pointer;
}
.group-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #1e293b;
}
.group-children {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-left: 30px; /* Lùi vào một chút cho đẹp */
}
.perm-badge {
  background-color: #f1f5f9;
  color: #64748b;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.85rem;
  border: 1px solid #e2e8f0;
}
.perm-badge.badge-active {
  background-color: #2e7d32;
  color: white;
  border-color: #2e7d32;
}

/* TRẠNG THÁI TRỐNG VÀ MODAL GIỮ NGUYÊN */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}
.empty-content {
  text-align: center;
  color: #aaaaaa;
}
.empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 1rem;
  color: #e0e0e0;
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
</style>
