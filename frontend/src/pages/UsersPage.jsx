import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import Modal from '../components/Modal';
import { Users, Plus, Search, Shield, UserCheck, CheckCircle2, XCircle } from 'lucide-react';

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    username: '', email: '', first_name: '', last_name: '', role: 'FACULTY', phone: '', password: 'Password@123'
  });

  const loadUsers = async () => {
    setLoading(true);
    try {
      let q = `?search=${encodeURIComponent(search)}`;
      if (roleFilter) q += `&role=${roleFilter}`;
      const data = await api.getUsers(q);
      setUsers(data.results || data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, [search, roleFilter]);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.createUser(formData);
      setIsModalOpen(false);
      setFormData({ username: '', email: '', first_name: '', last_name: '', role: 'FACULTY', phone: '', password: 'Password@123' });
      loadUsers();
    } catch (e) {
      alert('Error: ' + e.message);
    }
  };

  const toggleActive = async (user) => {
    try {
      await api.updateUser(user.id, { is_active: !user.is_active });
      loadUsers();
    } catch (e) {
      alert('Error updating user: ' + e.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            User Accounts & Role Permissions
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 1 Module: RBAC authorization, account activation, and credential management
          </p>
        </div>

        <button onClick={() => setIsModalOpen(true)} className="btn btn-primary">
          <Plus size={16} /> Create User Account
        </button>
      </div>

      {/* Filter Bar */}
      <div className="card" style={{ padding: '1rem', marginBottom: '1.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: '220px', position: 'relative' }}>
          <Search size={16} color="var(--color-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            className="form-input"
            style={{ paddingLeft: '2.25rem' }}
            placeholder="Search username, name, email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <select
          className="form-select"
          style={{ width: 'auto', minWidth: '180px' }}
          value={roleFilter}
          onChange={(e) => setRoleFilter(e.target.value)}
        >
          <option value="">All Roles</option>
          <option value="ADMIN">Administrator</option>
          <option value="EXAM_STAFF">Examination Staff</option>
          <option value="FACULTY">Faculty / Invigilator</option>
          <option value="STUDENT">Student</option>
        </select>
      </div>

      {/* Table */}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Full Name</th>
              <th>Institutional Email</th>
              <th>Assigned Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.length === 0 ? (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center', padding: '2rem', color: 'var(--color-muted)' }}>
                  {loading ? 'Loading users...' : 'No users found.'}
                </td>
              </tr>
            ) : (
              users.map((u) => (
                <tr key={u.id}>
                  <td style={{ fontWeight: 700, color: 'var(--color-forest)' }}>{u.username}</td>
                  <td>{u.first_name ? `${u.first_name} ${u.last_name || ''}` : '—'}</td>
                  <td>{u.email}</td>
                  <td>
                    <span className={u.role === 'ADMIN' ? 'badge badge-gold' : 'badge badge-neutral'}>
                      {u.role}
                    </span>
                  </td>
                  <td>
                    <span className={u.is_active ? 'badge badge-success' : 'badge badge-danger'}>
                      {u.is_active ? 'Active' : 'Deactivated'}
                    </span>
                  </td>
                  <td>
                    <button
                      onClick={() => toggleActive(u)}
                      className={`btn btn-sm ${u.is_active ? 'btn-outline' : 'btn-secondary'}`}
                      style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}
                    >
                      {u.is_active ? 'Deactivate' : 'Activate'}
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Create Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create Institutional User">
        <form onSubmit={handleCreate}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <div className="form-group">
              <label className="form-label">Username</label>
              <input required className="form-input" value={formData.username} onChange={(e) => setFormData({ ...formData, username: e.target.value })} placeholder="e.g. jdoe" />
            </div>
            <div className="form-group">
              <label className="form-label">Email</label>
              <input required type="email" className="form-input" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} placeholder="jdoe@examforge.edu" />
            </div>
            <div className="form-group">
              <label className="form-label">First Name</label>
              <input required className="form-input" value={formData.first_name} onChange={(e) => setFormData({ ...formData, first_name: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Last Name</label>
              <input required className="form-input" value={formData.last_name} onChange={(e) => setFormData({ ...formData, last_name: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">System Role</label>
              <select className="form-select" value={formData.role} onChange={(e) => setFormData({ ...formData, role: e.target.value })}>
                <option value="ADMIN">Administrator</option>
                <option value="EXAM_STAFF">Examination Staff</option>
                <option value="FACULTY">Faculty / Invigilator</option>
                <option value="STUDENT">Student</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Initial Password</label>
              <input required type="password" className="form-input" value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} />
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.25rem' }}>
            <button type="button" onClick={() => setIsModalOpen(false)} className="btn btn-outline">Cancel</button>
            <button type="submit" className="btn btn-primary">Create Account</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
