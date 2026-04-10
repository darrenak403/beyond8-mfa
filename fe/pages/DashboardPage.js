export function renderDashboardPage() {
  return `
    <div id="stats-tab" class="tab-panel">
      <div class="page-shell">
        <div class="page-content">
          <div class="stats-grid">
            <div class="stats-card">
              <div class="stats-label">Số người đã mua</div>
              <div class="stats-value" id="verified-users-value">0</div>
            </div>
            <div class="stats-card">
              <div class="stats-label">Doanh thu ước tính</div>
              <div class="stats-value revenue" id="revenue-value">0 VND</div>
            </div>
            <div class="stats-card">
              <div class="stats-label">Tổng user trong hệ thống</div>
              <div class="stats-value" id="total-users-value">0</div>
            </div>
          </div>

          <div class="users-block">
            <div class="users-header">
              <div class="users-title">Danh sách người dùng</div>
              <div class="users-filters" id="users-filters">
                <button class="users-filter-btn active" data-status-filter="all">Tất cả</button>
                <button class="users-filter-btn" data-status-filter="active">Đang hoạt động</button>
                <button class="users-filter-btn" data-status-filter="blocked">Đã khóa</button>
              </div>
            </div>
            <div class="loading" id="users-loading" style="display: none; margin: 14px">
              Đang tải dữ liệu người dùng...
            </div>
            <div class="error" id="stats-error" style="margin: 12px"></div>
            <div class="users-table-wrap">
              <table class="users-table">
                <thead>
                  <tr>
                    <th>Email</th>
                    <th>Vai trò</th>
                    <th>Trạng thái</th>
                    <th>Lý do khóa</th>
                    <th>Ngày tạo</th>
                    <th>Thao tác</th>
                  </tr>
                </thead>
                <tbody id="users-table-body"></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
}
