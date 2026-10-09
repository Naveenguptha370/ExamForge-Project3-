import React, { createContext, useContext, useState } from 'react';
import { CheckCircle2, AlertTriangle, AlertCircle, Info, X } from 'lucide-react';

const ToastContext = createContext();

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const addToast = (message, type = 'success', duration = 4000) => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev, { id, message, type }]);

    if (duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }
  };

  const removeToast = (id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  const toastIcons = {
    success: <CheckCircle2 size={18} color="#15803D" />,
    warning: <AlertTriangle size={18} color="#D97706" />,
    error: <AlertCircle size={18} color="#DC2626" />,
    info: <Info size={18} color="#15803D" />,
  };

  const toastBg = {
    success: 'border-[#15803D] bg-[#F0FDF4]',
    warning: 'border-[#D97706] bg-[#FEF3C7]',
    error: 'border-[#DC2626] bg-[#FEE2E2]',
    info: 'border-[#14532D] bg-[#FAF9F6]',
  };

  return (
    <ToastContext.Provider value={{ addToast, success: (m) => addToast(m, 'success'), error: (m) => addToast(m, 'error'), warning: (m) => addToast(m, 'warning'), info: (m) => addToast(m, 'info') }}>
      {children}
      <div style={{ position: 'fixed', bottom: 24, right: 24, zIndex: 9999, display: 'flex', flexDirection: 'column', gap: 10, maxWidth: 380 }}>
        {toasts.map((t) => (
          <div
            key={t.id}
            className="animate-fade-in card"
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: 12,
              padding: '12px 16px',
              backgroundColor: t.type === 'success' ? '#F0FDF4' : (t.type === 'error' ? '#FEF2F2' : (t.type === 'warning' ? '#FEF3C7' : '#FFFFFF')),
              borderLeft: `4px solid ${t.type === 'success' ? '#15803D' : (t.type === 'error' ? '#DC2626' : (t.type === 'warning' ? '#D97706' : '#14532D'))}`,
              boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              {toastIcons[t.type]}
              <span style={{ fontSize: '0.88rem', fontWeight: 600, color: '#242923' }}>{t.message}</span>
            </div>
            <button
              onClick={() => removeToast(t.id)}
              style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#6B7280' }}
            >
              <X size={16} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = () => useContext(ToastContext);
