import api from './api';
const BASE = '/api/seating';

export async function seatingServiceList(p) { const r = await api.get(BASE + '/list/', { params: p }); return r.data; }

export async function seatingServiceRetrieve(p) { const r = await api.get(BASE + '/retrieve/', { params: p }); return r.data; }

export async function seatingServiceCreate(p) { const r = await api.get(BASE + '/create/', { params: p }); return r.data; }

export async function seatingServiceUpdate(p) { const r = await api.get(BASE + '/update/', { params: p }); return r.data; }

export async function seatingServiceRemove(p) { const r = await api.get(BASE + '/remove/', { params: p }); return r.data; }

export async function seatingServiceSearch(p) { const r = await api.get(BASE + '/search/', { params: p }); return r.data; }

export async function seatingServiceSummary(p) { const r = await api.get(BASE + '/summary/', { params: p }); return r.data; }

export async function seatingServiceExportCsv(p) { const r = await api.get(BASE + '/exportCsv/', { params: p }); return r.data; }

export async function seatingServiceBulkUpdate(p) { const r = await api.get(BASE + '/bulkUpdate/', { params: p }); return r.data; }

export async function seatingServiceAuditTrail(p) { const r = await api.get(BASE + '/auditTrail/', { params: p }); return r.data; }

export async function seatingServiceStats(p) { const r = await api.get(BASE + '/stats/', { params: p }); return r.data; }

export async function seatingServiceHistory(p) { const r = await api.get(BASE + '/history/', { params: p }); return r.data; }
