import {renderHeader} from './components/Header.js'
import {renderOTPPage} from './pages/OTPPage.js'
import {renderDashboardPage} from './pages/DashboardPage.js'

const isLocalhost =
  window.location.hostname === '127.0.0.1' ||
  window.location.hostname === 'localhost' ||
  window.location.protocol === 'file:'

const apiBase = isLocalhost ? 'http://127.0.0.1:3636/api' : '/api'

const OTP_API_URL = `${apiBase}/otp/generate`
const LOGIN_URL = `${apiBase}/auth/login`
const STATS_URLS = [`${apiBase}/otp-verifications`, `${apiBase}/stats/otp-verifications`]
const USERS_URLS = [
  `${apiBase}/users?offset=0&limit=200`,
  `${apiBase}/getAllUser?offset=0&limit=200`,
]
const BLOCK_USER_URLS = (userId) => [
  `${apiBase}/users/${userId}/block`,
  `${apiBase}/getAllUser/${userId}/block`,
]
const UNBLOCK_USER_URLS = (userId) => [
  `${apiBase}/users/${userId}/unblock`,
  `${apiBase}/getAllUser/${userId}/unblock`,
]
const REVOKE_COURSE_ACCESS_URLS = (userId) => [
  `${apiBase}/users/${userId}/course-access/revoke`,
  `${apiBase}/getAllUser/${userId}/course-access/revoke`,
]
const CLEAR_VERIFIED_OTP_KEY_URLS = (userId) => [
  `${apiBase}/users/${userId}/otp-verified-key/clear`,
  `${apiBase}/getAllUser/${userId}/otp-verified-key/clear`,
]
const PRICE_PER_BUYER = 35000

let countdownInterval
let pollingInterval
let currentOtpVersion = null
let activeTab = 'otp-tab'
let usersCache = []
let usersStatusFilter = 'all'
const pendingKeyActions = new Set()

function buildCookieOptions() {
  const options = ['path=/', 'SameSite=Strict']
  if (window.location.protocol === 'https:') {
    options.push('Secure')
  }
  return options.join('; ')
}

const ORIGINAL_COPY_HTML = `
  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width: 18px; height: 18px;">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2"></path>
  </svg>
  Sao chép nhanh
`

function buildAppShell() {
  return `
    ${renderHeader()}

    <div class="split-card">
      <div class="info-side">
        <h2 class="info-title">Hệ thống Trạm Cấp Phát Bảo Mật Khách Hàng</h2>
        <p class="info-desc">
          Mọi chuỗi mã hóa (OTP) được cấp phát tự động bằng thuật toán bảo vệ dữ liệu nội bộ. Thông
          tin tại trạm này chỉ dành riêng cho quyền quản trị.
        </p>

        <div class="security-badge">
          <svg fill="currentColor" viewBox="0 0 20 20" style="width: 16px; height: 16px; margin-right: 6px">
            <path
              fill-rule="evenodd"
              d="M10 2a5 5 0 00-5 5v2a2 2 0 00-2 2v5a2 2 0 002 2h10a2 2 0 002-2v-5a2 2 0 00-2-2H7V7a3 3 0 015.905-.75 1 1 0 001.937-.5A5.002 5.002 0 0010 2z"
              clip-rule="evenodd"
            ></path>
          </svg>
          Kết nối mã hóa riêng tư
        </div>
      </div>

      <div class="action-side">
        <div id="login-section" style="display: none; transition: opacity 0.3s">
          <h3 class="action-title">Đăng Nhập</h3>
          <p class="subtitle">Vui lòng nhập Email Admin để tiếp tục</p>

          <div>
            <input type="email" id="email-input" placeholder="Nhập địa chỉ email..." autocomplete="email" />
            <div class="error" id="login-error">Email không có quyền hệ thống!</div>
          </div>

          <button class="btn-primary" id="login-btn">
            Truy cập Trạm mã
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width: 20px; height: 20px">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 7l5 5m0 0l-5 5m5-5H6"
              ></path>
            </svg>
          </button>
        </div>

        <div id="otp-section" style="display: none; transition: opacity 0.3s">
          ${renderOTPPage()}
          ${renderDashboardPage()}
        </div>
      </div>
    </div>
  `
}

function getCookieToken() {
  const cookies = document.cookie.split(';')
  const authCookie = cookies.find((c) => c.trim().startsWith('auth_token='))
  return authCookie ? authCookie.split('=')[1] : null
}

function persistAuthSession(sessionPayload) {
  const accessToken = sessionPayload?.access_token

  if (!accessToken) {
    throw new Error('Thông tin phiên đăng nhập không hợp lệ')
  }

  const cookieOptions = buildCookieOptions()
  document.cookie = `auth_token=${accessToken}; ${cookieOptions}`
}

function formatVND(value) {
  return `${new Intl.NumberFormat('vi-VN').format(value)} VND`
}

function showError(errorEl) {
  errorEl.style.display = 'block'
  errorEl.style.animation = 'none'
  errorEl.offsetHeight
  errorEl.style.animation = 'shake 0.4s ease-in-out'
}

function switchTab(tabId) {
  activeTab = tabId
  const splitCard = document.querySelector('.split-card')
  const navButtons = document.querySelectorAll('.nav-btn')
  const tabPanels = document.querySelectorAll('.tab-panel')

  navButtons.forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.tab === tabId)
  })

  tabPanels.forEach((panel) => {
    panel.classList.toggle('active', panel.id === tabId)
  })

  if (splitCard) {
    splitCard.classList.toggle('stats-layout', tabId === 'stats-tab')
  }
  document.body.classList.toggle('stats-mode', tabId === 'stats-tab')

  if (tabId === 'stats-tab') {
    fetchStatsAndUsers()
  }
}

function showLoginScreen() {
  document.getElementById('login-section').style.display = 'block'
  document.getElementById('otp-section').style.display = 'none'
  document.getElementById('header-nav').style.display = 'none'
  document.getElementById('header-logout-btn').style.display = 'none'
  clearInterval(countdownInterval)
  clearInterval(pollingInterval)

  if (window.location.hostname !== '127.0.0.1' && window.location.pathname !== '/login') {
    window.history.pushState({}, '', '/login')
  }
}

function checkAuth() {
  const token = getCookieToken()

  if (token) {
    document.getElementById('login-section').style.display = 'none'
    document.getElementById('otp-section').style.display = 'block'
    document.getElementById('header-nav').style.display = 'flex'
    document.getElementById('header-logout-btn').style.display = 'block'

    if (window.location.hostname !== '127.0.0.1' && window.location.pathname !== '/admin/key') {
      window.history.pushState({}, '', '/admin/key')
    }

    switchTab('otp-tab')
    fetchOTP(true)
    startPolling()
    return
  }

  showLoginScreen()
}

async function handleLogin() {
  const emailInput = document.getElementById('email-input').value.trim()
  const errorEl = document.getElementById('login-error')

  if (!emailInput) {
    errorEl.innerText = 'Vui lòng nhập email!'
    showError(errorEl)
    return
  }

  try {
    const btn = document.getElementById('login-btn')
    const originalBtn = btn.innerHTML
    btn.innerHTML = 'Đang kiểm tra...'

    const response = await fetch(LOGIN_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email: emailInput}),
    })

    btn.innerHTML = originalBtn

    if (!response.ok) {
      errorEl.innerText = 'Email không có quyền tự kích hoạt!'
      showError(errorEl)
      return
    }

    const data = await response.json()
    persistAuthSession(data.data)
    errorEl.style.display = 'none'

    document.getElementById('login-section').style.opacity = '0'
    setTimeout(() => {
      document.getElementById('login-section').style.opacity = '1'
      checkAuth()
    }, 300)
  } catch (error) {
    errorEl.innerText = 'Lỗi kết nối Backend!'
    showError(errorEl)
  }
}

function handleLogout() {
  document.getElementById('otp-section').style.opacity = '0'
  setTimeout(() => {
    document.cookie = 'auth_token=; path=/; max-age=0'
    document.getElementById('email-input').value = ''
    document.getElementById('otp-section').style.opacity = '1'
    showLoginScreen()
  }, 300)
}

async function fetchWithAuth(url) {
  const token = getCookieToken()
  if (!token) {
    handleLogout()
    return null
  }

  const response = await fetch(url, {
    method: 'GET',
    headers: {Authorization: `Bearer ${token}`},
  })

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      handleLogout()
      return null
    }

    const payload = await response.json().catch(() => null)
    throw new Error(payload?.message || 'Không thể tải dữ liệu')
  }

  return response.json()
}

async function patchWithAuth(url, payload = null) {
  const token = getCookieToken()
  if (!token) {
    handleLogout()
    return null
  }

  const response = await fetch(url, {
    method: 'PATCH',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: payload ? JSON.stringify(payload) : null,
  })

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      handleLogout()
      return null
    }

    const payloadData = await response.json().catch(() => null)
    throw new Error(payloadData?.message || 'Không thể cập nhật trạng thái người dùng')
  }

  return response.json()
}

async function fetchWithAuthFallback(urls) {
  let lastError = null

  for (const url of urls) {
    try {
      return await fetchWithAuth(url)
    } catch (error) {
      lastError = error
    }
  }

  if (lastError) {
    throw lastError
  }

  throw new Error('Không thể tải dữ liệu')
}

async function patchWithAuthFallback(urls, payload = null) {
  let lastError = null

  for (const url of urls) {
    try {
      return await patchWithAuth(url, payload)
    } catch (error) {
      lastError = error
    }
  }

  if (lastError) {
    throw lastError
  }

  throw new Error('Không thể cập nhật trạng thái người dùng')
}

async function fetchOTP(isInitial = false) {
  clearInterval(countdownInterval)

  if (isInitial) {
    document.getElementById('loading-text').style.display = 'block'
    document.getElementById('otp-display').style.display = 'none'
    document.getElementById('copy-btn').style.display = 'none'
    document.getElementById('countdown-text').style.display = 'none'
    document.getElementById('progress-container').style.display = 'none'
  } else {
    document.getElementById('otp-display').style.opacity = '0.5'
  }

  document.getElementById('error-message').style.display = 'none'

  try {
    const data = await fetchWithAuth(OTP_API_URL)
    if (!data) {
      return
    }

    const otpPayload = data.data

    if (isInitial) {
      document.getElementById('loading-text').style.display = 'none'
      document.getElementById('otp-display').style.display = 'flex'
      document.getElementById('copy-btn').style.display = 'flex'
      document.getElementById('countdown-text').style.display = 'flex'
      document.getElementById('progress-container').style.display = 'block'
    }

    document.getElementById('otp-display').style.opacity = '1'
    document.getElementById('otp-display').innerText = otpPayload.otp

    const newVersion = otpPayload.version
    if (currentOtpVersion !== null && newVersion !== currentOtpVersion) {
      const display = document.getElementById('otp-display')
      display.style.transition = 'background 0.3s'
      display.style.background = 'rgba(46, 204, 113, 0.15)'
      setTimeout(() => {
        display.style.background = ''
      }, 1000)
    }

    currentOtpVersion = newVersion
    startCountdown(otpPayload.expires_in)
  } catch (error) {
    if (isInitial) {
      document.getElementById('loading-text').style.display = 'none'
    }

    document.getElementById('otp-display').style.opacity = '1'
    const errorEl = document.getElementById('error-message')
    errorEl.style.display = 'block'
    errorEl.innerText = 'Lỗi: ' + error.message
  }
}

async function startPolling() {
  clearInterval(pollingInterval)
  const token = getCookieToken()
  if (!token) {
    return
  }

  pollingInterval = setInterval(async () => {
    const t = getCookieToken()
    if (!t) {
      clearInterval(pollingInterval)
      return
    }

    try {
      const data = await fetchWithAuth(OTP_API_URL)
      if (!data) {
        return
      }

      const payload = data.data
      if (currentOtpVersion !== null && payload.version !== currentOtpVersion) {
        fetchOTP(false)
        if (activeTab === 'stats-tab') {
          fetchStatsAndUsers()
        }
      }
    } catch (_) {
      // Polling errors are ignored to avoid noisy UI.
    }
  }, 5000)
}

function startCountdown(seconds) {
  clearInterval(countdownInterval)
  let timeLeft = seconds
  const totalTime = seconds
  const timerElement = document.getElementById('timer')
  const progressElement = document.getElementById('progress')

  timerElement.innerText = Math.max(0, timeLeft)
  progressElement.style.width = '100%'

  countdownInterval = setInterval(() => {
    timeLeft -= 1
    if (timeLeft <= 0) {
      clearInterval(countdownInterval)
      fetchOTP()
      if (activeTab === 'stats-tab') {
        fetchStatsAndUsers()
      }
      return
    }

    timerElement.innerText = timeLeft
    progressElement.style.width = (timeLeft / totalTime) * 100 + '%'
  }, 1000)
}

function renderUsers(users) {
  const tbody = document.getElementById('users-table-body')
  tbody.innerHTML = ''

  if (!users.length) {
    const emptyRow = document.createElement('tr')
    const emptyCell = document.createElement('td')
    emptyCell.colSpan = 8
    emptyCell.textContent = 'Chưa có dữ liệu người dùng'
    emptyRow.appendChild(emptyCell)
    tbody.appendChild(emptyRow)
    return
  }

  users.forEach((user) => {
    const row = document.createElement('tr')

    const emailCell = document.createElement('td')
    emailCell.textContent = user.email

    const roleCell = document.createElement('td')
    const roleChip = document.createElement('span')
    roleChip.className = user.role === 'admin' ? 'role-chip admin' : 'role-chip'
    roleChip.textContent = user.role
    roleCell.appendChild(roleChip)

    const statusCell = document.createElement('td')
    statusCell.textContent = user.is_active ? 'Đang hoạt động' : 'Đã khóa'

    const keyStatusCell = document.createElement('td')
    keyStatusCell.textContent = user.course_access_active ? 'Đang có key' : 'Chưa có key'
    if (user.course_access_active) {
      keyStatusCell.classList.add('key-active')
    }

    const reasonCell = document.createElement('td')
    reasonCell.textContent = user.blocked_reason || '-'

    const createdCell = document.createElement('td')
    createdCell.textContent = new Date(user.created_at).toLocaleString('vi-VN')

    const accountActionCell = document.createElement('td')
    const actionBtn = document.createElement('button')
    actionBtn.className = user.is_active ? 'user-action-btn block' : 'user-action-btn unblock'

    const keyActionCell = document.createElement('td')
    const keyActionsWrap = document.createElement('div')
    keyActionsWrap.className = 'key-actions-wrap'

    const revokeBtn = document.createElement('button')
    revokeBtn.className = 'user-action-btn revoke'
    revokeBtn.textContent = 'Thu hồi key'

    if (user.role === 'admin') {
      actionBtn.classList.add('disabled')
      actionBtn.disabled = true
      actionBtn.textContent = 'Admin'
      revokeBtn.classList.add('disabled')
      revokeBtn.disabled = true
    } else {
      actionBtn.textContent = user.is_active ? 'Khóa' : 'Mở khóa'
      actionBtn.addEventListener('click', () => toggleUserBlock(user))

      revokeBtn.disabled = !user.course_access_active
      if (!user.course_access_active) {
        revokeBtn.classList.add('disabled')
      }
      revokeBtn.addEventListener('click', () => revokeUserCourseAccess(user, revokeBtn))
    }
    accountActionCell.appendChild(actionBtn)
    keyActionsWrap.appendChild(revokeBtn)
    keyActionCell.appendChild(keyActionsWrap)

    row.appendChild(emailCell)
    row.appendChild(roleCell)
    row.appendChild(statusCell)
    row.appendChild(keyStatusCell)
    row.appendChild(reasonCell)
    row.appendChild(createdCell)
    row.appendChild(accountActionCell)
    row.appendChild(keyActionCell)

    tbody.appendChild(row)
  })
}

function applyUsersFilter() {
  const filteredUsers = usersCache.filter((user) => {
    if (usersStatusFilter === 'active') {
      return user.is_active
    }
    if (usersStatusFilter === 'blocked') {
      return !user.is_active
    }
    return true
  })

  renderUsers(filteredUsers)
}

async function toggleUserBlock(user) {
  const statsError = document.getElementById('stats-error')
  statsError.style.display = 'none'

  try {
    if (user.is_active) {
      const reasonInput = window.prompt('Nhập lý do khóa tài khoản (có thể bỏ trống):', '')
      if (reasonInput === null) {
        return
      }
      await patchWithAuthFallback(BLOCK_USER_URLS(user.id), {reason: reasonInput.trim()})
    } else {
      await patchWithAuthFallback(UNBLOCK_USER_URLS(user.id))
    }

    await fetchStatsAndUsers()
  } catch (error) {
    statsError.innerText = 'Lỗi cập nhật người dùng: ' + error.message
    showError(statsError)
  }
}

async function revokeUserCourseAccess(user, buttonEl = null) {
  const statsError = document.getElementById('stats-error')
  statsError.style.display = 'none'

  if (pendingKeyActions.has(user.id)) {
    return
  }

  try {
    const confirmed = window.confirm(
      `Thu hồi key của ${user.email}? Hành động này sẽ thu hồi course access và xóa OTP key đã verify.`
    )
    if (!confirmed) {
      return
    }

    pendingKeyActions.add(user.id)
    if (buttonEl) {
      buttonEl.disabled = true
      buttonEl.classList.add('disabled')
    }

    const revokePromise = patchWithAuthFallback(REVOKE_COURSE_ACCESS_URLS(user.id))
    const clearPromise = patchWithAuthFallback(CLEAR_VERIFIED_OTP_KEY_URLS(user.id))
    const [revokeResult, clearResult] = await Promise.allSettled([revokePromise, clearPromise])

    await fetchStatsAndUsers()

    const errors = []
    if (revokeResult.status === 'rejected') {
      errors.push(
        `Thu hồi course access thất bại: ${revokeResult.reason?.message || revokeResult.reason}`
      )
    }
    if (clearResult.status === 'rejected') {
      errors.push(
        `Xóa OTP key đã verify thất bại: ${clearResult.reason?.message || clearResult.reason}`
      )
    }

    if (errors.length > 0) {
      throw new Error(errors.join(' | '))
    }
  } catch (error) {
    statsError.innerText = 'Lỗi thu hồi key: ' + error.message
    showError(statsError)
  } finally {
    pendingKeyActions.delete(user.id)
  }
}

async function fetchStatsAndUsers() {
  const statsError = document.getElementById('stats-error')
  const usersLoading = document.getElementById('users-loading')
  statsError.style.display = 'none'
  usersLoading.style.display = 'block'

  try {
    const [statsData, usersData] = await Promise.all([
      fetchWithAuthFallback(STATS_URLS),
      fetchWithAuthFallback(USERS_URLS),
    ])

    if (!statsData || !usersData) {
      return
    }

    const verifiedUsers = statsData.data?.verified_users || 0
    const totalUsers = usersData.data?.total_users || 0

    document.getElementById('verified-users-value').innerText = verifiedUsers
    document.getElementById('total-users-value').innerText = totalUsers
    document.getElementById('revenue-value').innerText = formatVND(verifiedUsers * PRICE_PER_BUYER)

    usersCache = usersData.data?.users || []
    applyUsersFilter()
  } catch (error) {
    statsError.innerText = 'Lỗi tải thống kê: ' + error.message
    showError(statsError)
  } finally {
    usersLoading.style.display = 'none'
  }
}

function copyToClipboardAction() {
  const otpDisplay = document.getElementById('otp-display')
  const copyBtn = document.getElementById('copy-btn')
  const otpText = otpDisplay.innerText

  if (otpText === 'BY8-????-????-????') {
    return
  }

  navigator.clipboard.writeText(otpText)

  const originalColor = otpDisplay.style.color
  otpDisplay.style.color = '#222222'
  otpDisplay.style.transform = 'scale(0.98)'

  setTimeout(() => {
    otpDisplay.style.color = originalColor
    otpDisplay.style.transform = ''
  }, 200)

  copyBtn.classList.add('success')
  copyBtn.innerHTML =
    '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width: 18px; height: 18px;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Đã sao chép!'

  setTimeout(() => {
    copyBtn.classList.remove('success')
    copyBtn.innerHTML = ORIGINAL_COPY_HTML
  }, 2000)
}

function bindEvents() {
  const logo = document.getElementById('header-logo')
  if (logo) {
    logo.onerror = () => {
      logo.style.display = 'none'
    }
  }

  document.getElementById('header-logout-btn').addEventListener('click', handleLogout)
  document.getElementById('login-btn').addEventListener('click', handleLogin)

  document.getElementById('email-input').addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
      handleLogin()
    }
  })

  document.getElementById('otp-display').addEventListener('click', copyToClipboardAction)
  document.getElementById('copy-btn').addEventListener('click', copyToClipboardAction)

  document.querySelectorAll('.nav-btn').forEach((btn) => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab))
  })

  document.querySelectorAll('.users-filter-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      usersStatusFilter = btn.dataset.statusFilter || 'all'
      document.querySelectorAll('.users-filter-btn').forEach((item) => {
        item.classList.toggle('active', item === btn)
      })
      applyUsersFilter()
    })
  })
}

function bootstrap() {
  const app = document.getElementById('app')
  if (!app) {
    return
  }

  app.insertAdjacentHTML('beforebegin', buildAppShell())
  app.remove()
  bindEvents()
  checkAuth()
}

bootstrap()
