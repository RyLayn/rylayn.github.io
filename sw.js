/* Tabla de Tipos Pokémon - por AC - RyLayn (github.com/RyLayn)
   Trabajador offline: primero red (datos frescos), respaldo cache (funciona sin internet). */
const CACHE = 'tipos-pokemon-v1';
self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(['./'])));
});
self.addEventListener('activate', e => { e.waitUntil(clients.claim()); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request).then(r => {
      if (r.ok && new URL(e.request.url).origin === location.origin) {
        const copia = r.clone();
        caches.open(CACHE).then(c => c.put(e.request, copia));
      }
      return r;
    }).catch(() => caches.match(e.request, {ignoreSearch:true}))
  );
});
