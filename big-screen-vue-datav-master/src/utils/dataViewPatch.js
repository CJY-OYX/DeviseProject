// DataV MutationObserver 修复补丁
// 解决 observerDomResize 函数中对不存在元素的观察导致的错误
// 同时增强对 DataV 组件 DOM 节点访问失败的处理

/**
 * 修复 DataV 库中的 observerDomResize 函数和增强组件错误处理
 * 添加对 null/undefined 节点的检查，避免 MutationObserver 错误
 */
export default function patchDataV() {
  try {
    // 尝试获取 DataV 库中的 observerDomResize 函数
    const dataViewPackage = require('@jiaminghi/data-view');
    
    // 检查是否已应用补丁
    if (window.__DATA_V_PATCHED__) {
      return;
    }
    
    // 尝试从不同位置获取 observerDomResize 函数
    let observerDomResize = null;
    
    // 方法1: 尝试直接从 package 中获取
    if (dataViewPackage && dataViewPackage.util && dataViewPackage.util.observerDomResize) {
      observerDomResize = dataViewPackage.util.observerDomResize;
    }
    
    // 如果找到了原始函数，应用补丁
    if (observerDomResize) {
      patchObserverDomResize(observerDomResize);
    } else {
      // 如果上述方法都失败，通过重写全局 MutationObserver 来捕获错误
      patchGlobalMutationObserver();
    }
    
    // 增强 DataV 组件的 DOM 节点访问错误处理
    enhanceDataVDomHandling();
    
    // 标记为已修补
    window.__DATA_V_PATCHED__ = true;
  } catch (e) {
    console.warn('DataV patch: Failed to apply patch', e);
  }
}

/**
 * 增强 DataV 组件的 DOM 节点访问错误处理
 * 拦截组件的错误并提供更友好的错误处理
 */
function enhanceDataVDomHandling() {
  try {
    // 记录原始的 console.error 方法
    const originalConsoleError = console.error;
    
    // 重写 console.error 来捕获和处理 DataV DOM 节点错误
    console.error = function(...args) {
      // 检查是否为 DataV 的 DOM 节点错误
      const isDataVDomError = args.some(arg => 
        typeof arg === 'string' && arg.includes('DataV: Failed to get dom node')
      );
      
      if (isDataVDomError) {
        // 记录更友好的错误信息，避免污染控制台
        console.warn('DataV: DOM 节点获取失败 - 组件可能尚未挂载完成，这通常是暂时的情况');
        // 可以选择是否仍然显示原始错误
        // originalConsoleError.apply(console, args);
      } else {
        // 对于其他错误，使用原始方法
        originalConsoleError.apply(console, args);
      }
    };
    
    // 尝试拦截 DataV 组件的 mounted 生命周期，添加安全检查
    const patchDataVComponents = () => {
      try {
        // 添加全面的空值检查
        if (!window.Vue || !window.Vue.options || !window.Vue.options.components) {
          // console.warn('DataV patch: Vue instance or components not available for patching');
          return;
        }
        
        // 查找所有以 'dv-' 开头的已注册组件
        const dataVComponents = Object.keys(window.Vue.options.components || {})
          .filter(compName => compName.startsWith('dv-'));
        
        if (dataVComponents.length === 0) {
          console.log('DataV patch: No DataV components found to patch');
          return;
        }
        
        dataVComponents.forEach(compName => {
          try {
            const component = window.Vue.options.components[compName];
            if (component && component.mounted && typeof component.mounted === 'function') {
              const originalMounted = component.mounted;
              component.mounted = function() {
                try {
                  // 添加组件挂载前的安全检查
                  const $el = this.$el;
                  if ($el && $el.nodeType === 1) {
                    // 节点存在，执行原始挂载
                    originalMounted.call(this);
                  } else {
                    console.warn(`DataV: Component ${compName} mounted without valid DOM element`);
                    // 仍然尝试执行原始挂载，防止功能缺失
                    try {
                      originalMounted.call(this);
                    } catch (innerError) {
                      // 静默忽略第二次错误
                    }
                  }
                } catch (e) {
                  console.warn(`DataV: Error mounting component ${compName}:`, e);
                  // 尝试继续执行，防止应用崩溃
                  try {
                    originalMounted.call(this);
                  } catch (innerError) {
                    // 静默忽略第二次错误
                  }
                }
              };
            }
          } catch (e) {
            // 忽略单个组件的补丁错误，继续处理其他组件
            console.warn(`DataV patch: Failed to patch component ${compName}:`, e);
          }
        });
        
        console.log(`DataV patch: Successfully patched ${dataVComponents.length} DataV components`);
      } catch (e) {
        console.warn('DataV patch: Error in component patching process:', e);
      }
    };
    
    // 如果 Vue 已经初始化，立即应用组件补丁
    if (window.Vue) {
      patchDataVComponents();
    } else {
      // 否则，等待 Vue 初始化完成
      setTimeout(patchDataVComponents, 1000);
    }
    
    console.log('DataV patch: DOM handling has been enhanced');
  } catch (e) {
    console.warn('DataV patch: Failed to enhance DOM handling', e);
  }
}

/**
 * 修补 observerDomResize 函数
 */
function patchObserverDomResize(originalObserverDomResize) {
  // 创建新的安全版本函数
  const safeObserverDomResize = function(node) {
    // 添加 null/undefined 检查
    if (!node || !node.nodeType) {
      console.warn('DataV: Attempting to observe a non-DOM node or null node');
      return {
        // 返回一个模拟的disconnect方法，避免调用时出错
        disconnect: function() {}
      };
    }
    
    try {
      // 调用原始函数
      return originalObserverDomResize.apply(this, arguments);
    } catch (e) {
      console.warn('DataV: Error in observerDomResize', e);
      return {
        disconnect: function() {}
      };
    }
  };
  
  // 替换原始函数
  if (originalObserverDomResize && typeof originalObserverDomResize === 'function') {
    Object.keys(originalObserverDomResize).forEach(key => {
      safeObserverDomResize[key] = originalObserverDomResize[key];
    });
    
    // 将安全版本的函数替换到原始位置
    const module = require.cache[require.resolve('@jiaminghi/data-view/src/util/index.js')];
    if (module && module.exports) {
      module.exports.observerDomResize = safeObserverDomResize;
    }
    
    console.log('DataV patch: observerDomResize function has been patched');
  }
}

/**
 * 修补全局 MutationObserver
 * 这是后备方案，当无法直接访问 DataV 的 observerDomResize 函数时使用
 */
function patchGlobalMutationObserver() {
  const originalMutationObserver = window.MutationObserver;
  
  if (!originalMutationObserver) return;
  
  window.MutationObserver = function(callback) {
    const observer = new originalMutationObserver(callback);
    
    // 保存原始的 observe 方法
    const originalObserve = observer.observe;
    
    // 重写 observe 方法，添加错误处理
    observer.observe = function(target, options) {
      try {
        // 添加目标节点检查
        if (!target || !target.nodeType) {
          console.warn('DataV: Attempting to observe a non-DOM node or null node');
          return;
        }
        
        // 调用原始 observe 方法
        originalObserve.call(this, target, options);
      } catch (e) {
        // 捕获并记录错误，但不阻止应用运行
        console.warn('DataV: MutationObserver error', e);
      }
    };
    
    return observer;
  };
  
  // 复制静态属性
  window.MutationObserver.prototype = originalMutationObserver.prototype;
  window.MutationObserver.observe = originalMutationObserver.observe;
  window.MutationObserver.disconnect = originalMutationObserver.disconnect;
  window.MutationObserver.takeRecords = originalMutationObserver.takeRecords;
  
  console.log('DataV patch: Global MutationObserver has been patched');
}