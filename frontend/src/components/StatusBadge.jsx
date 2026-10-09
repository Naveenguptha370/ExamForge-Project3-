import React from 'react';

export const StatusBadge = ({ status }) => {
  const norm = (status || '').toUpperCase();

  const styles = {
    DRAFT: { bg: '#F3F4F6', color: '#4B5563', border: '#E5E7EB', text: 'Draft' },
    VALIDATED: { bg: '#DDEBDD', color: '#14532D', border: '#b8d6b8', text: 'Validated' },
    APPROVED: { bg: '#FEF3C7', color: '#B45309', border: '#fde68a', text: 'Approved' },
    PUBLISHED: { bg: '#DCFCE7', color: '#15803D', border: '#bbf7d0', text: 'Published' },
    IN_PROGRESS: { bg: '#FEF3C7', color: '#D97706', border: '#fde68a', text: 'In Progress' },
    COMPLETED: { bg: '#F0FDF4', color: '#166534', border: '#bbf7d0', text: 'Completed' },
    ARCHIVED: { bg: '#E7E5E4', color: '#575E54', border: '#d6d3d1', text: 'Archived' },
    ACTIVE: { bg: '#DCFCE7', color: '#15803D', border: '#bbf7d0', text: 'Active' },
    CRITICAL: { bg: '#FEE2E2', color: '#991B1B', border: '#fecaca', text: 'Critical Clash' },
    HIGH: { bg: '#FEF3C7', color: '#92400E', border: '#fde68a', text: 'High Priority' },
    MEDIUM: { bg: '#F4F9F4', color: '#15803D', border: '#c7e6c7', text: 'Medium' },
    HARD: { bg: '#FEE2E2', color: '#991B1B', border: '#fecaca', text: 'Hard' },
    EASY: { bg: '#DCFCE7', color: '#15803D', border: '#bbf7d0', text: 'Easy' },
  };

  const current = styles[norm] || { bg: '#F3F4F6', color: '#4B5563', border: '#E5E7EB', text: status };

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        padding: '3px 9px',
        fontSize: '0.73rem',
        fontWeight: 700,
        borderRadius: 9999,
        backgroundColor: current.bg,
        color: current.color,
        border: `1px solid ${current.border}`,
        textTransform: 'uppercase',
        letterSpacing: '0.03em'
      }}
    >
      {current.text}
    </span>
  );
};
