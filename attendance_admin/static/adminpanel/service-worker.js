// Very small service worker for offline caching
const CACHE_NAME = 'qr-admin-cache-v1';
const URLS_TO_CACHE = [
  '/',
  '/adminpanel/scanner/',
  '/static/adminpanel/style.css',
  '/static/adminpanel/scanner.js'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(URLS_TO_CACHE);
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});
