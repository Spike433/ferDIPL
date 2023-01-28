import { del, entries } from "./idb-keyval.js";
const filesToCache = [
    "/",
    "manifest.json",
    "index.html",
    "offline.html",
    "404.html",
    "https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,400;0,700;1,400;1,700&display=swap",
    "https://fonts.gstatic.com/s/firasans/v11/va9E4kDNxMZdWfMOD5Vvl4jLazX3dA.woff2",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
];

const staticCacheName = "static-cache-v2";

self.addEventListener("install", (event) => {
    console.log("Attempting to install service worker and cache static assets");
    event.waitUntil(
        caches.open(staticCacheName).then((cache) => {
            return cache.addAll(filesToCache);
        })
    );
});

self.addEventListener("activate", (event) => {
    console.log("**************************************");
    console.log("**   Activating new service worker... **");
    console.log("**************************************");
    const cacheWhitelist = [staticCacheName];
    // Ovako možemo obrisati sve ostale cacheve koji nisu naš
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches
            .match(event.request)
            .then((response) => {
                if (response) {
                    // console.log("Found " + event.request.url + " in cache!");
                    //return response;
                }
                // console.log("----------------->> Network request for ",
                //     event.request.url
                // );
                return fetch(event.request).then((response) => {
                    // console.log("response.status = " + response.status);
                    if (response.status === 404) {
                        return caches.match("404.html");
                    }
                    return caches.open(staticCacheName).then((cache) => {
                        // console.log(">>> Caching: " + event.request.url);
                        cache.put(event.request.url, response.clone());
                        return response;
                    });
                });
            })
            .catch((error) => {
                console.log("Error", event.request.url, error);
                // ovdje možemo pregledati header od zahtjeva i možda vratiti različite fallback sadržaje
                // za različite zahtjeve - npr. ako je zahtjev za slikom možemo vratiti fallback sliku iz cachea
                // ali zasad, za sve vraćamo samo offline.html:
                return caches.match("offline.html");
            })
    );
});

self.addEventListener("sync", function (event) {
    console.log("Background sync!", event);
    if (event.tag === "sync-snaps") {
        event.waitUntil(syncSnaps());
    }
});

let syncSnaps = async function () {
    entries().then((entries) => {
        entries.forEach((entry) => {
            let snap = entry[1]; //  Each entry is an array of [key, value].
            let formData = new FormData();
            formData.append("id", snap.id);
            formData.append("ts", snap.ts);
            formData.append("title", snap.title);
            formData.append("image", snap.image, snap.id + ".png");
            fetch("/saveSnap", {
                method: "POST",
                body: formData,
            })
                .then(function (res) {
                    if (res.ok) {
                        res.json().then(function (data) {
                            console.log("Deleting from idb:", data.id);
                            del(data.id);
                        });
                    } else {
                        console.log(res);
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        });
    });
};

self.addEventListener("notificationclick", function (event) {
    let notification = event.notification;
    // mogli smo i definirati actions, pa ovdje granati s obzirom na:
    // let action = event.action;
    console.log("notification", notification);
    event.waitUntil(
        clients.matchAll().then(function (clis) {
            clis.forEach((client) => {
                client.navigate(notification.data.redirectUrl);
                client.focus();
            });
            notification.close();
        })
    );
});

self.addEventListener("notificationclose", function (event) {
    console.log("notificationclose", event);
});

self.addEventListener("push", function (event) {
    console.log("push event", event);

    var data = { title: "title", body: "body", redirectUrl: "/" };

    if (event.data) {
        data = JSON.parse(event.data.text());
    }

    var options = {
        body: data.body,
        icon: "assets/img/android/android-launchericon-96-96.png",
        badge: "assets/img/android/android-launchericon-96-96.png",
        vibrate: [200, 100, 200, 100, 200, 100, 200],
        data: {
            redirectUrl: data.redirectUrl,
        },
    };

    event.waitUntil(self.registration.showNotification(data.title, options));
});
