<template>
  <DefaultLayout>
    <div class="transaction-wrapper">
      <button class="btn-back" @click="$router.push('/')">
        <ArrowLeft class="icon-sm" /> Về Bảng Điều Khiển
      </button>
      <div class="page-header">
        <div class="title-group">
          <!-- <Archive class="title-icon" /> -->
          <h2>Lập Phiếu Yêu Cầu Giao / Nhận Hàng</h2>
        </div>

        <p class="text-muted">
          Hệ thống tự động hiển thị biểu mẫu phù hợp với đặc quyền tài khoản của
          bạn.
        </p>
      </div>

      <!-- <div v-if="isAdmin" class="admin-view-selector mb-4">
        <span class="label">Góc nhìn Admin:</span>
        <button
          :class="['btn-tab', { active: customerMode === 'VIP' }]"
          @click="setCustomerMode('VIP')"
        >
          Khách VIP
        </button>
        <button
          :class="['btn-tab', { active: customerMode === 'THUONG' }]"
          @click="setCustomerMode('THUONG')"
        >
          Khách Thường
        </button>
        <button
          :class="['btn-tab', { active: customerMode === 'LE' }]"
          @click="setCustomerMode('LE')"
        >
          Khách Lẻ
        </button>
      </div> -->
      <div v-if="showTabSelector" class="admin-view-selector mb-4">
        <span class="label">Chế độ hiển thị:</span>
        <button
          v-if="canViewVip"
          :class="['btn-tab', { active: customerMode === 'VIP' }]"
          @click="setCustomerMode('VIP')"
        >
          Khách VIP
        </button>
        <button
          v-if="canViewThuong"
          :class="['btn-tab', { active: customerMode === 'THUONG' }]"
          @click="setCustomerMode('THUONG')"
        >
          Khách Thường
        </button>
        <button
          v-if="canViewLe"
          :class="['btn-tab', { active: customerMode === 'LE' }]"
          @click="setCustomerMode('LE')"
        >
          Khách Lẻ
        </button>
      </div>

      <div class="split-layout">
        <div class="left-panel">
          <h3 class="panel-title">Chọn Nghiệp Vụ</h3>
          <div class="action-list">
            <template v-for="action in availableActions" :key="action.id">
              <div
                class="action-card"
                :class="{ active: currentAction === action.id }"
                @click="currentAction = action.id"
              >
                <div class="icon-box"><component :is="action.icon" /></div>
                <div class="card-text">
                  <h4>{{ action.title }}</h4>
                  <p>{{ action.desc }}</p>
                </div>
              </div>
            </template>

            <div
              v-if="availableActions.length === 0"
              class="text-muted text-center p-4"
            >
              Bạn không có quyền thực hiện nghiệp vụ nào trong nhóm này.
            </div>
          </div>
        </div>

        <div class="right-panel card">
          <h3 class="panel-title text-primary">
            {{ currentActionObj?.title || 'Vui lòng chọn nghiệp vụ' }}
          </h3>
          <hr class="divider" />

          <form v-if="currentActionObj" @submit.prevent="handleSubmit">
            <div class="form-grid">
              <div class="form-group">
                <label>Mã Kho (SPL) <span class="text-danger">*</span></label>
                <input
                  type="text"
                  v-model="form.ma_kho_spl"
                  required
                  placeholder="VD: KHO_HCM_01"
                />
              </div>
              <div
                class="form-group"
                v-if="customerMode === 'VIP' || isExportAction"
              >
                <label
                  >Mã Vận Đơn / Bill <span class="text-danger">*</span></label
                >
                <input
                  type="text"
                  v-model="form.ma_bill"
                  required
                  placeholder="VD: BILL-2026-001"
                />
              </div>

              <div class="form-group" v-if="customerMode === 'VIP'">
                <label>Số Serial <span class="text-danger">*</span></label>
                <div class="input-group" style="display: flex; gap: 8px">
                  <input
                    type="text"
                    v-model="form.serial"
                    required
                    placeholder="Nhập mã Serial duy nhất..."
                    style="flex: 1"
                    @keyup.enter.prevent="checkSerial"
                  />
                  <button
                    v-if="currentAction !== 'VIP_IMPORT_NEW'"
                    type="button"
                    class="btn btn-secondary btn-sm"
                    @click="checkSerial"
                    :disabled="isCheckingSerial"
                    style="padding: 0 15px"
                  >
                    <RefreshCcw
                      v-if="isCheckingSerial"
                      class="icon-sm spin"
                      style="margin-right: 5px"
                    />
                    Kiểm tra
                  </button>
                </div>
                <small
                  v-if="serialMessage"
                  :class="serialMessageClass"
                  style="display: block; margin-top: 5px"
                >
                  {{ serialMessage }}
                </small>
              </div>
              <template v-if="currentAction === 'VIP_IMPORT_NEW'">
                <div class="form-group">
                  <label>PXK Kho TSB</label>
                  <input
                    type="text"
                    v-model="form.pxk_kho_tsb"
                    placeholder="Phiếu xuất kho TSB..."
                  />
                </div>
                <div class="form-group">
                  <label>PXK VP TSB</label>
                  <input
                    type="text"
                    v-model="form.pxk_vp_tsb"
                    placeholder="Phiếu xuất VP TSB..."
                  />
                </div>
              </template>

              <div
                class="form-group"
                v-if="
                  currentAction === 'VIP_IMPORT_NEW' ||
                  currentAction === 'VIP_EXPORT_NEW' ||
                  currentAction === 'THUONG_IMPORT' ||
                  currentAction === 'THUONG_EXPORT'
                "
              >
                <label>Mã Sản Phẩm <span class="text-danger">*</span></label>
                <input
                  type="text"
                  v-model="form.ma_san_pham"
                  required
                  placeholder="Mã hàng từ Nhà cung cấp"
                />
              </div>

              <div
                class="form-group"
                v-if="customerMode === 'THUONG' || customerMode === 'LE'"
              >
                <label
                  >Tên Sản Phẩm
                  <span v-if="!isExportAction" class="text-danger"
                    >*</span
                  ></label
                >
                <input
                  type="text"
                  v-model="form.ten_san_pham"
                  placeholder="Tên hàng hóa..."
                />
              </div>

              <div
                class="form-group"
                v-if="
                  (customerMode === 'VIP' &&
                    currentAction === 'VIP_IMPORT_NEW') ||
                  currentAction === 'VIP_EXPORT_NEW'
                "
              >
                <label>Mã Máy <span class="text-danger">*</span></label>
                <input
                  type="text"
                  v-model="form.ma_may"
                  required
                  placeholder="VD: DELL-7400"
                />
              </div>

              <div
                class="form-group"
                v-if="customerMode === 'THUONG' || customerMode === 'LE'"
              >
                <label>Số Lượng <span class="text-danger">*</span></label>
                <input
                  type="number"
                  min="1"
                  v-model="form.so_luong"
                  required
                  placeholder="Nhập số lượng..."
                />
              </div>

              <template v-if="isExportAction">
                <div class="form-group">
                  <label
                    >Nhân Viên Giao Hàng
                    <span class="text-danger">*</span></label
                  >
                  <input
                    type="text"
                    v-model="form.nv_giao_hang"
                    required
                    placeholder="Tên người giao..."
                  />
                </div>
                <div class="form-group">
                  <label>Biển Số Xe</label>
                  <input
                    type="text"
                    v-model="form.bien_so_xe"
                    placeholder="VD: 51H-12345"
                  />
                </div>
              </template>

              <template v-if="currentAction === 'VIP_EXPORT_OLD'">
                <div class="form-group">
                  <label>Kho Trả Hàng <span class="text-danger">*</span></label>
                  <input
                    type="text"
                    v-model="form.kho_tra_hang"
                    required
                    placeholder="Tên kho nhận trả..."
                  />
                </div>
                <div class="form-group">
                  <label>Người Nhận <span class="text-danger">*</span></label>
                  <input
                    type="text"
                    v-model="form.nguoi_nhan"
                    required
                    placeholder="Tên người nhận..."
                  />
                </div>
              </template>
            </div>

            <div class="form-group full-width mt-3">
              <label>Ghi Chú</label>
              <textarea
                v-model="form.ghi_chu"
                rows="2"
                placeholder="Ghi chú thêm nếu có..."
              ></textarea>
            </div>

            <div class="form-actions mt-4">
              <button
                type="button"
                class="btn btn-secondary"
                @click="resetForm"
              >
                Làm Lại
              </button>
              <button
                type="submit"
                class="btn btn-save"
                :disabled="isSubmitting"
              >
                <Send class="icon-sm" v-if="!isSubmitting" />
                {{ isSubmitting ? 'Đang Xử Lý...' : 'Gửi Yêu Cầu' }}
              </button>
            </div>
          </form>

          <div v-else class="empty-state text-center p-5 text-muted">
            <MousePointerClick
              class="empty-icon mb-3"
              style="width: 48px; height: 48px; opacity: 0.5"
            />
            <p>Hãy chọn một nghiệp vụ ở cột bên trái để bắt đầu điền phiếu.</p>
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
import {
  Archive,
  ArrowDownToLine,
  ArrowUpFromLine,
  RefreshCcw,
  SendToBack,
  Send,
  MousePointerClick,
  ArrowLeft,
} from 'lucide-vue-next';

const authStore = useAuthStore();
const toast = useToast();

const isAdmin = computed(() => authStore.hasPermission('FUNC_ADMIN_ALL'));
const customerMode = ref(''); // 'VIP', 'REGULAR', 'RETAIL'
const currentAction = ref(''); // Lưu ID của action đang chọn
const isSubmitting = ref(false);

// 1. Kiểm tra xem User có quyền vào từng Tab hay không
const canViewVip = computed(
  () =>
    isAdmin.value ||
    ALL_ACTIONS.filter((a) => a.mode === 'VIP').some((a) =>
      authStore.hasPermission(a.perm)
    )
);
const canViewThuong = computed(
  () =>
    isAdmin.value ||
    ALL_ACTIONS.filter((a) => a.mode === 'THUONG').some((a) =>
      authStore.hasPermission(a.perm)
    )
);
const canViewLe = computed(
  () =>
    isAdmin.value ||
    ALL_ACTIONS.filter((a) => a.mode === 'LE').some((a) =>
      authStore.hasPermission(a.perm)
    )
);

// 2. Chỉ hiện thanh chuyển Tab nếu họ có quyền ở ít nhất 2 nhóm
const showTabSelector = computed(() => {
  const accessibleTabs = [
    canViewVip.value,
    canViewThuong.value,
    canViewLe.value,
  ].filter(Boolean);
  return accessibleTabs.length > 1;
});

// Định nghĩa toàn bộ các Action có thể có trong hệ thống
const ALL_ACTIONS = [
  // Nhóm VIP
  {
    id: 'VIP_IMPORT_NEW',
    mode: 'VIP',
    type: 'IMPORT',
    perm: 'FUNC_VIP_NHAP_MOI',
    title: 'Gửi Hàng Mới',
    desc: 'Nhập kho thiết bị mới',
    icon: ArrowDownToLine,
  },
  {
    id: 'VIP_EXPORT_NEW',
    mode: 'VIP',
    type: 'EXPORT',
    perm: 'FUNC_VIP_XUAT_MOI',
    title: 'Yêu Cầu Giao Hàng',
    desc: 'Xuất kho giao cho khách',
    icon: ArrowUpFromLine,
  },
  {
    id: 'VIP_IMPORT_OLD',
    mode: 'VIP',
    type: 'IMPORT',
    perm: 'FUNC_VIP_NHAP_CU',
    title: 'Khách Trả Lại',
    desc: 'Nhập lại hàng cũ',
    icon: RefreshCcw,
  },
  {
    id: 'VIP_EXPORT_OLD',
    mode: 'VIP',
    type: 'EXPORT',
    perm: 'FUNC_VIP_XUAT_CU',
    title: 'Trả Nhà Cung Cấp',
    desc: 'Xuất hàng cũ',
    icon: SendToBack,
  },
  // Nhóm THƯỜNG
  {
    id: 'THUONG_IMPORT',
    mode: 'THUONG',
    type: 'IMPORT',
    perm: 'FUNC_THUONG_NHAP',
    title: 'Nhập Lô Hàng',
    desc: 'Gửi hàng vào kho theo lô',
    icon: ArrowDownToLine,
  },
  {
    id: 'THUONG_EXPORT',
    mode: 'THUONG',
    type: 'EXPORT',
    perm: 'FUNC_THUONG_XUAT',
    title: 'Xuất Kho',
    desc: 'Xuất hàng trong kho',
    icon: ArrowUpFromLine,
  },
  // Nhóm LẺ
  {
    id: 'LE_IMPORT',
    mode: 'LE',
    type: 'IMPORT',
    perm: 'FUNC_LE_NHAP',
    title: 'Nhập Hàng Lẻ',
    desc: 'Nhập hàng vào kho',
    icon: ArrowDownToLine,
  },
  {
    id: 'LE_EXPORT',
    mode: 'LE',
    type: 'EXPORT',
    perm: 'FUNC_LE_XUAT',
    title: 'Xuất Hàng Lẻ',
    desc: 'Xuất hàng trong kho',
    icon: ArrowUpFromLine,
  },
];

// Tự động gán Mode ban đầu dựa vào quyền của User (nếu không phải Admin)
// onMounted(() => {
//   if (isAdmin.value) {
//     customerMode.value = 'VIP'; // Admin mặc định vào tab VIP
//   } else {
//     // Tìm mode đầu tiên mà user có ít nhất 1 quyền
//     const userMode = ['VIP', 'THUONG', 'LE'].find((mode) =>
//       ALL_ACTIONS.filter((a) => a.mode === mode).some((a) =>
//         authStore.hasPermission(a.perm)
//       )
//     );
//     customerMode.value = userMode || 'VIP';
//   }
// });

onMounted(() => {
  if (canViewVip.value) customerMode.value = 'VIP';
  else if (canViewThuong.value) customerMode.value = 'THUONG';
  else if (canViewLe.value) customerMode.value = 'LE';
});

const setCustomerMode = (mode) => {
  customerMode.value = mode;
};

// Lọc ra các Action bên cột trái dựa vào Mode đang chọn và Quyền của người dùng
const availableActions = computed(() => {
  return ALL_ACTIONS.filter((action) => {
    // Phải đúng Mode đang chọn
    if (action.mode !== customerMode.value) return false;
    // Phải có quyền (hoặc là Admin)
    return isAdmin.value || authStore.hasPermission(action.perm);
  });
});

// Lấy Object chi tiết của Action đang chọn
const currentActionObj = computed(() =>
  ALL_ACTIONS.find((a) => a.id === currentAction.value)
);

// Kiểm tra xem form hiện tại là Nhập hay Xuất để ẩn/hiện các trường Giao Hàng
const isExportAction = computed(
  () => currentActionObj.value?.type === 'EXPORT'
);

// ==========================================
// QUẢN LÝ STATE CỦA FORM
// ==========================================
const form = ref({
  ma_kho_spl: '',
  ma_bill: '',
  serial: '',
  ma_san_pham: '',
  ten_san_pham: '',
  ma_may: '',
  so_luong: null,
  nv_giao_hang: '',
  bien_so_xe: '',
  kho_tra_hang: '',
  nguoi_nhan: '',
  ghi_chu: '',
  pxk_kho_tsb: '',
  pxk_vp_tsb: '',
});

const isCheckingSerial = ref(false);
const serialMessage = ref('');
const serialMessageClass = ref('');

// Hàm kiểm tra Serial
const checkSerial = async () => {
  if (!form.value.serial) {
    toast.info('Vui lòng nhập số Serial trước khi kiểm tra!');
    return;
  }

  isCheckingSerial.value = true;
  serialMessage.value = '';

  try {
    const res = await inventoryService.checkVipSerial(form.value.serial);

    if (res.data.found) {
      serialMessage.value = '✓ Tìm thấy thông tin thiết bị. Đã tự động điền.';
      serialMessageClass.value = 'text-success';

      // Tự động điền dữ liệu vào form
      form.value.ma_san_pham =
        res.data.data.ma_san_pham || form.value.ma_san_pham;
      form.value.ma_may = res.data.data.ma_may || form.value.ma_may;
      form.value.ma_bill = res.data.data.ma_bill || form.value.ma_bill;
      form.value.pxk_kho_tsb = res.data.data.pxk_kho || form.value.pxk_kho_tsb;
      form.value.pxk_vp_tsb = res.data.data.pxk_vp || form.value.pxk_vp_tsb;
      form.value.ma_kho_spl = res.data.data.ma_kho_spl || form.value.ma_kho_spl;
    } else {
      serialMessage.value = '✗ Không tìm thấy Serial này trong hệ thống.';
      serialMessageClass.value = 'text-danger';

      // Xóa các trường liên quan nếu nhập sai
      form.value.ma_san_pham = '';
      form.value.ma_may = '';
      form.value.ma_bill = '';
      form.value.pxk_kho_tsb = '';
      form.value.pxk_vp_tsb = '';
      form.value.ma_kho_spl = '';
    }
  } catch (error) {
    console.error(error);
    toast.error('Lỗi khi kết nối đến máy chủ để kiểm tra Serial.');
  } finally {
    isCheckingSerial.value = false;
  }
};

/// Thêm tham số isHardReset (Mặc định là false - Xóa thông minh)
const resetForm = (isHardReset = false) => {
  serialMessage.value = '';
  if (isHardReset) {
    // CHẾ ĐỘ 1: XÓA TRẮNG (Dùng khi đổi Tab hoặc bấm "Làm Lại")
    form.value = {
      ma_kho_spl: '',
      ma_bill: '',
      serial: '',
      ma_san_pham: '',
      ten_san_pham: '',
      ma_may: '',
      so_luong: null,
      nv_giao_hang: '',
      bien_so_xe: '',
      kho_tra_hang: '',
      nguoi_nhan: '',
      ghi_chu: '',
      pxk_kho_tsb: '',
      pxk_vp_tsb: '',
    };
  } else {
    // CHẾ ĐỘ 2: XÓA THÔNG MINH (Chạy sau khi Gửi phiếu thành công)
    const currentData = { ...form.value }; // Copy lại toàn bộ form hiện tại

    // 1. Dù là Khách nào thì cũng phải xóa các trường Đơn lẻ
    currentData.serial = '';
    currentData.ghi_chu = '';
    currentData.so_luong = null;

    // 2. Nếu là Khách Thường / Khách Lẻ (Thường nhập nhiều loại hàng khác nhau)
    // -> Xóa Tên SP và Mã SP để họ nhập món tiếp theo
    if (customerMode.value === 'THUONG' || customerMode.value === 'LE') {
      currentData.ma_san_pham = '';
      currentData.ten_san_pham = '';
    }

    // 3. Nếu là VIP (Thường nhập 1 lô Laptop/Màn hình giống hệt nhau, chỉ khác Serial)
    // -> GIỮ LẠI Mã SP và Mã Máy. Thủ kho chỉ việc tít Serial mới!
    // (Nếu họ đổi sang loại máy khác thì tự gõ lại Mã SP là xong).

    // Cập nhật lại Form
    form.value = currentData;
  }
};

watch([currentAction, customerMode], () => {
  resetForm(true);
});

// ==========================================
// GỌI API THEO MAP (Mapping)
// ==========================================
const handleSubmit = async () => {
  if (
    customerMode.value === 'VIP' &&
    currentAction.value !== 'VIP_IMPORT_NEW'
  ) {
    // Nếu Form chưa có Mã Sản Phẩm (Tức là chưa được "Kiểm tra" thành công)
    if (!form.value.ma_san_pham) {
      await checkSerial(); // Tự động gọi hàm quét Serial

      // Sau khi quét, nếu vẫn sai (text-danger) thì KHÔNG CHO GỬI nữa!
      if (serialMessageClass.value === 'text-danger') {
        toast.error('Không thể gửi phiếu! Vui lòng nhập Số Serial hợp lệ.');
        return; // Dừng hàm tại đây, không gọi Backend
      }
    }
  }

  isSubmitting.value = true;

  // Ánh xạ form data sang đúng chuẩn Schema Pydantic của Backend
  let payload = {};
  try {
    if (currentAction.value === 'VIP_IMPORT_NEW') {
      payload = {
        serial_moi: form.value.serial,
        ma_kho_spl: form.value.ma_kho_spl,
        ma_san_pham: form.value.ma_san_pham,
        ma_may: form.value.ma_may,
        ma_bill: form.value.ma_bill,
        ghi_chu: form.value.ghi_chu,
        pxk_kho_tsb: form.value.pxk_kho_tsb, // <--- Thêm vào payload
        pxk_vp_tsb: form.value.pxk_vp_tsb, // <--- Thêm vào payload
      };
      await inventoryService.importNewVip(payload);
    } else if (currentAction.value === 'VIP_EXPORT_NEW') {
      payload = {
        serial_moi: form.value.serial,
        nv_giao_hang: form.value.nv_giao_hang,
        bien_so_xe: form.value.bien_so_xe,
        ma_bill: form.value.ma_bill,
        ghi_chu: form.value.ghi_chu,
      };
      await inventoryService.exportNewVip(payload);
    } else if (currentAction.value === 'VIP_IMPORT_OLD') {
      payload = {
        serial_cu: form.value.serial,
        ma_kho_spl: form.value.ma_kho_spl,
        ma_bill: form.value.ma_bill,
        ghi_chu: form.value.ghi_chu,
      };
      await inventoryService.importOldVip(payload);
    } else if (currentAction.value === 'VIP_EXPORT_OLD') {
      payload = {
        serial_cu: form.value.serial,
        ma_kho_spl: form.value.ma_kho_spl,
        ma_bill: form.value.ma_bill,
        nv_giao_hang: form.value.nv_giao_hang,
        bien_so_xe: form.value.bien_so_xe,
        kho_tra_hang: form.value.kho_tra_hang,
        nguoi_nhan: form.value.nguoi_nhan,
        ghi_chu: form.value.ghi_chu,
      };
      await inventoryService.exportOldVip(payload);
    }
    // =========================================================================================
    else if (currentAction.value === 'THUONG_IMPORT') {
      // const generatedId = stringToId(form.value.ma_san_pham); // Dùng mã SP làm ID
      // Dùng tạm mã sản phẩm làm ID định danh cho Lô theo chuẩn backend của bạn
      payload = {
        id: 0,
        ma_kho_spl: form.value.ma_kho_spl,
        ten_san_pham: form.value.ten_san_pham,
        ma_san_pham: form.value.ma_san_pham,
        so_luong: form.value.so_luong,
        ghi_chu: form.value.ghi_chu,
      };
      await inventoryService.importRegular(payload);
    } else if (currentAction.value === 'THUONG_EXPORT') {
      // const generatedId = stringToId(form.value.ma_san_pham);
      payload = {
        id: 0,
        ma_kho_spl: form.value.ma_kho_spl,
        ten_san_pham: form.value.ten_san_pham,
        ma_san_pham: form.value.ma_san_pham,
        so_luong: form.value.so_luong,
        nv_giao_hang: form.value.nv_giao_hang,
        bien_so_xe: form.value.bien_so_xe,
        ma_bill: form.value.ma_bill,
        ghi_chu: form.value.ghi_chu,
      };
      console.log(payload);
      await inventoryService.exportRegular(payload);
    }
    // Tương tự cho Retail...
    else if (currentAction.value === 'LE_IMPORT') {
      // const generatedId = stringToId(form.value.ten_san_pham);
      payload = {
        id: 0,
        ma_kho_spl: form.value.ma_kho_spl,
        ten_san_pham: form.value.ten_san_pham,
        so_luong: form.value.so_luong,
        ghi_chu: form.value.ghi_chu,
      };
      await inventoryService.importRetail(payload);
    } else if (currentAction.value === 'LE_EXPORT') {
      // const generatedId = stringToId(form.value.ten_san_pham);
      payload = {
        id: 0,
        ma_kho_spl: form.value.ma_kho_spl,
        ten_san_pham: form.value.ten_san_pham,
        so_luong: form.value.so_luong,
        nv_giao_hang: form.value.nv_giao_hang,
        bien_so_xe: form.value.bien_so_xe,
        ma_bill: form.value.ma_bill,
        ghi_chu: form.value.ghi_chu,
      };
      await inventoryService.exportRetail(payload);
    }

    toast.success('Gửi phiếu yêu cầu thành công!');
    resetForm();
  } catch (error) {
    toast.error(
      error.response?.data?.detail ||
        'Lỗi khi gửi yêu cầu. Vui lòng kiểm tra lại!'
    );
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.transaction-wrapper {
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

.split-layout {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 24px;
  align-items: start;
}
.panel-title {
  margin-bottom: 20px;
  font-size: 1.2rem;
  color: #1e293b;
}

/* Thẻ tác vụ bên trái */
.action-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.action-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  border: 2px solid transparent;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  transition: all 0.2s;
}
.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
.action-card.active {
  border-color: #2e7d32;
  background: #f0fdf4;
}
.icon-box {
  background: #f1f5f9;
  color: #64748b;
  padding: 12px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.action-card.active .icon-box {
  background: #2e7d32;
  color: white;
}
.card-text h4 {
  margin: 0 0 4px 0;
  color: #0f3d26;
  font-size: 1.05rem;
}
.card-text p {
  margin: 0;
  color: #64748b;
  font-size: 0.85rem;
  line-height: 1.3;
}

/* Form bên phải */
.right-panel {
  padding: 30px;
}
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.full-width {
  grid-column: span 2;
}
.form-group label {
  display: block;
  font-weight: 600;
  color: #334155;
  margin-bottom: 8px;
  font-size: 0.9rem;
}
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}
.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #2e7d32;
  box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
}
.form-group input:disabled {
  background-color: #f1f5f9;
  cursor: not-allowed;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #e2e8f0;
  padding-top: 20px;
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
