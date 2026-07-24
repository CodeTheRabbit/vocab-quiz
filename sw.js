/* 서비스 워커 — network-first
   온라인이면 항상 네트워크 최신(캐시 우회)으로 받고, 쿼리 없는 정상(200) 쉘 파일만
   오프라인용으로 보관한다. 오프라인이면 캐시로 폴백.
   - 데이터(data/**?v=시각)는 쿼리가 있어 캐시에 남기지 않는다(매번 새로 받으므로).
   - 오류(404/500) 응답은 fresh.ok 로 걸러 캐시하지 않는다. */
const CACHE = 'vq-shell-v3';

self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', (e) => e.waitUntil((async () => {
  const keys = await caches.keys();
  await Promise.all(keys.filter(k => k.startsWith('vq-') && k !== CACHE).map(k => caches.delete(k)));
  await self.clients.claim();
})()));

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  let url;
  try { url = new URL(req.url); } catch { return; }
  if (url.origin !== self.location.origin) return;

  e.respondWith((async () => {
    try {
      const fresh = await fetch(req, { cache: 'no-store' });
      if (!url.search && fresh.ok) {           // 쿼리 없는 정상 쉘만 보관
        const cache = await caches.open(CACHE);
        cache.put(req, fresh.clone());
      }
      return fresh;
    } catch (err) {
      const cached = await caches.match(req);
      if (cached) return cached;
      if (req.mode === 'navigate') {
        const home = await caches.match('index.html') || await caches.match('./');
        if (home) return home;
      }
      throw err;
    }
  })());
});
