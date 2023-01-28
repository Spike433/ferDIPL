const CACHE_NAME = "V1";
const STATIC_CACHE_URLS = [
  "/",
  "index.html",
  "index.js",
  "manifest.json",
  "favicon.ico",
  "icons/android/android-launchericon-72-72.png",
  "icons/android/android-launchericon-144-144.png",
  "icons/android/android-launchericon-192-192.png",
  "icons/android/android-launchericon-512-512.png",
  "icons/maskable_icon_x192.png",
];

self.addEventListener("install", (event) => {
  console.log("Service Worker installing.");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_CACHE_URLS))
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.url.includes("/api/")) {
    if (event.request.method === "GET") {
      // response to API requests, Cache Update Refresh strategy
      event.respondWith(
        caches
          .match(event.request)
          .then((cached) => cached || fetch(event.request))
      );
      if (navigator.onLine)
        event.waitUntil(update(event.request).then(refresh));
    }
  } else {
    // Cache-First Strategy
    event.respondWith(
      caches
        .match(event.request) // check if the request has already been cached
        .then((cached) => cached || fetch(event.request)) // otherwise request network
    );
  }
});

self.addEventListener("periodicsync", function (event) {
  console.log("sync event", event);
  if (event.tag === "sync") {
    event.waitUntil(sync()); // sending sync request
  }
});

// Add push notification functionality
self.addEventListener("push", function (event) {
  console.log("push event", event);
  if (event.data) {
    const data = event.data.json();
    const title = data.title;
    const options = {
      body: data.body,
      icon: data.icon,
      badge: data.badge,
      image: data.image,
      vibrate: data.vibrate,
      tag: data.tag,
      renotify: data.renotify,
      data: data.data,
    };
    event.waitUntil(self.registration.showNotification(title, options));
  }
});

// Add notification click functionality
self.addEventListener("notificationclick", (event) => {
  let notification = event.notification;

  event.waitUntil(
    clients.matchAll().then((clis) => {
      clis.forEach((client) => {
        client.navigate("/");
        client.focus();
      });

      notification.close();
    })
  );
});

// ----------------- Helper functions -----------------

async function update(request) {
  console.log(request);
  return fetch(request.url).then(
    (response) =>
      caches
        .open(CACHE_NAME)
        .then((cache) => cache.put(request?.name || request, response.clone())) // cache response
        .then(() => response) // resolve promise with the Response object
  );
}

function refresh(response) {
  return response
    .json() // read and parse JSON response
    .then((jsonResponse) => {
      self.clients.matchAll().then((clients) => {
        clients.forEach((client) => {
          // report and send new data to client
          client.postMessage(
            JSON.stringify({
              type: response.url,
              data: jsonResponse,
            })
          );
        });
      });
      return jsonResponse; // resolve promise with new data
    });
}

async function sync() {
  // Get cached response from /api/recordings
  const cachedRecordings = await caches
    .match("/api/recordings")
    .then((res) => res?.json() || []);

  // Update cache and refresh clients
  const response = await update({
    url: "/api/recordings",
    name: "/api/recordings",
  });
  const recordings = await refresh(response);

  // Get number of recordings inside recordings which id is greater then biggest id in cachedRecordings
  const newRecordings = recordings.filter(
    (recording) =>
      cachedRecordings.length === 0 ||
      recording.id > cachedRecordings[cachedRecordings.length - 1].id
  );

  // Send push notification
  fetch("/api/push", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title: "Web5 Lab2",
      body: `You have ${newRecordings.length} new recordings`,
      icon: "/icons/android/android-launchericon-72-72.png",
      badge: "/icons/android/android-launchericon-72-72.png",
      image: "/icons/android/android-launchericon-72-72.png",
      vibrate: [200, 100, 200, 100, 200, 100, 200],
      tag: "web2lab5",
      renotify: true,
    }),
  });
}
