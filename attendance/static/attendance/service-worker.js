// Simple service worker for the student PWA
const CACHE_NAME = 'qr-student-cache-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/static/adminpanel/style.css',
  '/static/adminpanel/scanner.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request).then((res) => {
        // Optionally cache new requests
        return res;
      }).catch(() => {
        // fallback could go here
        return caches.match('/');
      });
    })
  );
});
