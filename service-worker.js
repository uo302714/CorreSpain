const CACHE_NAME = 'correspain-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600&display=swap'
];

// Instalar el Service Worker y cachear la estructura base
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

// Activar y limpiar cachés obsoletas
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
});

// Estrategia: Network First con fallback a caché (ideal para las fotos locales)
self.addEventListener('fetch', (e) => {
  e.respondWith(
    fetch(e.request)
      .then((response) => {
        // Si la petición es una foto descargada o un mapa, lo guardamos dinámicamente en la caché
        if (e.request.url.includes('/fotos/') || e.request.url.includes('tile.basemaps.cartocdn.com')) {
          const resClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(e.request, resClone);
          });
        }
        return response;
      })
      .catch(() => caches.match(e.request))
  );
});