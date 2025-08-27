/**
 * @param {Function} fn 防抖函数
 * @param {Number} delay 延迟时间
 */
export function debounce(fn, delay) {
  var timer;
  return function () {
    var context = this;
    var args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  };
}

/**
 * @param {date} time 需要转换的时间
 * @param {String} fmt 需要转换的格式 如 yyyy-MM-dd、yyyy-MM-dd HH:mm:ss
 */
export function formatTime(time, fmt) {
  if (!time) return '';
  else {
    const date = new Date(time);
    const o = {
      'M+': date.getMonth() + 1,
      'd+': date.getDate(),
      'H+': date.getHours(),
      'm+': date.getMinutes(),
      's+': date.getSeconds(),
      'q+': Math.floor((date.getMonth() + 3) / 3),
      S: date.getMilliseconds(),
    };
    if (/(y+)/.test(fmt))
      fmt = fmt.replace(
        RegExp.$1,
        (date.getFullYear() + '').substr(4 - RegExp.$1.length)
      );
    for (const k in o) {
      if (new RegExp('(' + k + ')').test(fmt)) {
        fmt = fmt.replace(
          RegExp.$1,
          RegExp.$1.length === 1
            ? o[k]
            : ('00' + o[k]).substr(('' + o[k]).length)
        );
      }
    }
    return fmt;
  }
}

/**
 * 自定义居中弹窗函数
 * @param {String} message 弹窗消息
 * @param {String} title 弹窗标题
 * @param {Function} callback 点击确认后的回调函数
 */
export function showModal(message, title = '提示', callback = null) {
  // 创建弹窗容器
  const modalContainer = document.createElement('div');
  modalContainer.className = 'custom-modal-container';
  modalContainer.innerHTML = `
    <div class="custom-modal-overlay">
      <div class="custom-modal">
        <div class="custom-modal-header">
          <h3 class="custom-modal-title">${title}</h3>
        </div>
        <div class="custom-modal-body">
          <p>${message}</p>
        </div>
        <div class="custom-modal-footer">
          <button class="custom-modal-confirm-btn">确定</button>
        </div>
      </div>
    </div>
  `;
  
  // 添加到body
  document.body.appendChild(modalContainer);
  
  // 添加确认按钮事件
  const confirmBtn = modalContainer.querySelector('.custom-modal-confirm-btn');
  const closeModal = () => {
    document.body.removeChild(modalContainer);
    if (callback && typeof callback === 'function') {
      callback();
    }
  };
  
  confirmBtn.addEventListener('click', closeModal);
  
  // 点击遮罩层也可以关闭弹窗
  const overlay = modalContainer.querySelector('.custom-modal-overlay');
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      closeModal();
    }
  });
  
  // 按ESC键关闭弹窗
  const handleEsc = (e) => {
    if (e.key === 'Escape') {
      closeModal();
      document.removeEventListener('keydown', handleEsc);
    }
  };
  
  document.addEventListener('keydown', handleEsc);
}

/**
 * 自定义居中输入弹窗函数
 * @param {String} message 弹窗消息
 * @param {String} defaultValue 默认值
 * @param {String} title 弹窗标题
 * @returns {String|null} 用户输入的值，用户取消则返回null
 */
export function showPrompt(message, defaultValue = '', title = '请输入') {
  return new Promise((resolve) => {
    // 创建弹窗容器
    const promptContainer = document.createElement('div');
    promptContainer.className = 'custom-modal-container';
    promptContainer.innerHTML = `
      <div class="custom-modal-overlay">
        <div class="custom-modal">
          <div class="custom-modal-header">
            <h3 class="custom-modal-title">${title}</h3>
          </div>
          <div class="custom-modal-body">
            <p>${message}</p>
            <input type="text" class="custom-prompt-input" value="${defaultValue}" />
          </div>
          <div class="custom-modal-footer">
            <button class="custom-modal-cancel-btn">取消</button>
            <button class="custom-modal-confirm-btn">确定</button>
          </div>
        </div>
      </div>
    `;
    
    // 添加到body
    document.body.appendChild(promptContainer);
    
    // 自动聚焦输入框
    const input = promptContainer.querySelector('.custom-prompt-input');
    input.focus();
    input.select();
    
    // 关闭弹窗函数
    const closePrompt = (value = null) => {
      document.body.removeChild(promptContainer);
      resolve(value);
      document.removeEventListener('keydown', handleKeyDown);
    };
    
    // 添加确认按钮事件
    const confirmBtn = promptContainer.querySelector('.custom-modal-confirm-btn');
    confirmBtn.addEventListener('click', () => closePrompt(input.value));
    
    // 添加取消按钮事件
    const cancelBtn = promptContainer.querySelector('.custom-modal-cancel-btn');
    cancelBtn.addEventListener('click', () => closePrompt(null));
    
    // 点击遮罩层也可以关闭弹窗
    const overlay = promptContainer.querySelector('.custom-modal-overlay');
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        closePrompt(null);
      }
    });
    
    // 处理键盘事件
    const handleKeyDown = (e) => {
      if (e.key === 'Enter') {
        closePrompt(input.value);
      } else if (e.key === 'Escape') {
        closePrompt(null);
      }
    };
    
    document.addEventListener('keydown', handleKeyDown);
  });
}
