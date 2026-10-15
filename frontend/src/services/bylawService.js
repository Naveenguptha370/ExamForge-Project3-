import api from './api';
const BASE = '/api/bylaws';

export async function bylawServiceList(p) { const r = await api.get(BASE + '/list/', { params: p }); return r.data; }

export async function bylawServiceRetrieve(p) { const r = await api.get(BASE + '/retrieve/', { params: p }); return r.data; }

export async function bylawServiceCreate(p) { const r = await api.get(BASE + '/create/', { params: p }); return r.data; }

export async function bylawServiceUpdate(p) { const r = await api.get(BASE + '/update/', { params: p }); return r.data; }

export async function bylawServiceRemove(p) { const r = await api.get(BASE + '/remove/', { params: p }); return r.data; }

export async function bylawServiceSearch(p) { const r = await api.get(BASE + '/search/', { params: p }); return r.data; }

export async function bylawServiceSummary(p) { const r = await api.get(BASE + '/summary/', { params: p }); return r.data; }

export async function bylawServiceExportCsv(p) { const r = await api.get(BASE + '/exportCsv/', { params: p }); return r.data; }

export async function bylawServiceBulkUpdate(p) { const r = await api.get(BASE + '/bulkUpdate/', { params: p }); return r.data; }

export async function bylawServiceAuditTrail(p) { const r = await api.get(BASE + '/auditTrail/', { params: p }); return r.data; }

export async function bylawServiceStats(p) { const r = await api.get(BASE + '/stats/', { params: p }); return r.data; }

export async function bylawServiceHistory(p) { const r = await api.get(BASE + '/history/', { params: p }); return r.data; }
