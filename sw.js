/* 서비스 워커 — network-first
   목적: 홈화면(standalone) 앱이 옛 HTML을 캐싱해 코드 변경이 안 보이던 문제 해결.
   - 온라인: 항상 네트워크에서 최신(캐시 우회)으로 받고, 쉘(HTML/에셋)은 오프라인용으로 캐시.
   - 오프라인: 캐시로 폴백.
   데이터(data/**?v=시각)는 쿼리가 있어 캐시에 남기지 않는다(매번 새로 받으므로). */
const CACHE = 'vq-shell-v2';

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
      // 쿼리 없는 쉘 파일만 오프라인용으로 보관 (데이터의 ?v= 는 제외)
      if (req.mode === 'navigate' || !url.search) {
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
