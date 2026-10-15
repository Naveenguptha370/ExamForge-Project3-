import api from './api';
const BASE = '/api/venues';

export async function venueServiceList(p) { const r = await api.get(BASE + '/list/', { params: p }); return r.data; }

export async function venueServiceRetrieve(p) { const r = await api.get(BASE + '/retrieve/', { params: p }); return r.data; }

export async function venueServiceCreate(p) { const r = await api.get(BASE + '/create/', { params: p }); return r.data; }

export async function venueServiceUpdate(p) { const r = await api.get(BASE + '/update/', { params: p }); return r.data; }

export async function venueServiceRemove(p) { const r = await api.get(BASE + '/remove/', { params: p }); return r.data; }

export async function venueServiceSearch(p) { const r = await api.get(BASE + '/search/', { params: p }); return r.data; }

export async function venueServiceSummary(p) { const r = await api.get(BASE + '/summary/', { params: p }); return r.data; }

export async function venueServiceExportCsv(p) { const r = await api.get(BASE + '/exportCsv/', { params: p }); return r.data; }

export async function venueServiceBulkUpdate(p) { const r = await api.get(BASE + '/bulkUpdate/', { params: p }); return r.data; }

export async function venueServiceAuditTrail(p) { const r = await api.get(BASE + '/auditTrail/', { params: p }); return r.data; }

export async function venueServiceStats(p) { const r = await api.get(BASE + '/stats/', { params: p }); return r.data; }

export async function venueServiceHistory(p) { const r = await api.get(BASE + '/history/', { params: p }); return r.data; }
