export function renderOTPPage() {
  return `
    <div id="otp-tab" class="tab-panel active">
      <div class="page-shell">
        <div class="action-header-row page-header-row">
          <div>
            <h3 class="action-title" style="font-size: 24px">Mã OTP cho khách hàng</h3>
          </div>
        </div>

        <div id="otp-container" class="page-content">
          <div class="loading" id="loading-text">Đang đồng bộ phân luồng mã...</div>
          <div class="otp-display" id="otp-display" style="display: none" title="Click để sao chép mã">
            BY8-????-????-????
          </div>
          <button class="btn-copy" id="copy-btn" style="display: none">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width: 18px; height: 18px">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2"
              ></path>
            </svg>
            Sao chép nhanh
          </button>
          <div class="countdown" id="countdown-text" style="display: none">
            <span>Hiệu lực còn lại</span>
            <div><span id="timer">--</span>s</div>
          </div>
          <div class="progress-bar" id="progress-container" style="display: none">
            <div class="progress" id="progress"></div>
          </div>
          <div class="error" id="error-message"></div>
        </div>
      </div>
    </div>
  `
}
