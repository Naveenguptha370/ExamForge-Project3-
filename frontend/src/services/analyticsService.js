import api from './api';
const BASE = '/api/analytics';

export async function analyticsServiceList(p) { const r = await api.get(BASE + '/list/', { params: p }); return r.data; }

export async function analyticsServiceRetrieve(p) { const r = await api.get(BASE + '/retrieve/', { params: p }); return r.data; }

export async function analyticsServiceCreate(p) { const r = await api.get(BASE + '/create/', { params: p }); return r.data; }

export async function analyticsServiceUpdate(p) { const r = await api.get(BASE + '/update/', { params: p }); return r.data; }

export async function analyticsServiceRemove(p) { const r = await api.get(BASE + '/remove/', { params: p }); return r.data; }

export async function analyticsServiceSearch(p) { const r = await api.get(BASE + '/search/', { params: p }); return r.data; }

export async function analyticsServiceSummary(p) { const r = await api.get(BASE + '/summary/', { params: p }); return r.data; }

export async function analyticsServiceExportCsv(p) { const r = await api.get(BASE + '/exportCsv/', { params: p }); return r.data; }

export async function analyticsServiceBulkUpdate(p) { const r = await api.get(BASE + '/bulkUpdate/', { params: p }); return r.data; }

export async function analyticsServiceAuditTrail(p) { const r = await api.get(BASE + '/auditTrail/', { params: p }); return r.data; }

export async function analyticsServiceStats(p) { const r = await api.get(BASE + '/stats/', { params: p }); return r.data; }

export async function analyticsServiceHistory(p) { const r = await api.get(BASE + '/history/', { params: p }); return r.data; }
