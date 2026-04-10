export function renderHeader() {
  return `
    <header>
      <div class="header-left">
        <img
          src="/public/logo.png"
          alt="Infinity Logo"
          class="header-logo"
          id="header-logo"
        />
        <h1 class="header-title">Beyond8<span>Auth</span></h1>
      </div>

      <div class="header-nav" id="header-nav" style="display: none">
        <button class="nav-btn active" data-tab="otp-tab">Lấy mã OTP</button>
        <button class="nav-btn" data-tab="stats-tab">Thống kê</button>
      </div>

      <button class="logout-btn" id="header-logout-btn" style="display: none">Đăng xuất</button>
    </header>
  `
}
