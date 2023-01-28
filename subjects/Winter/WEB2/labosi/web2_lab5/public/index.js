if ("serviceWorker" in navigator) {
  // Register the service worker
  navigator.serviceWorker
    .register("/sw.js")
    .then((serviceWorker) => {
      console.log("Service Worker registered: ", serviceWorker);
    })
    .catch((error) => {
      console.error("Error registering the Service Worker: ", error);
    });

  // Listen for messages from the service worker
  navigator.serviceWorker.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message && message.type.includes("/api/users")) {
      console.log("List of attendees to date", message.data);
      renderAttendees(message.data);
    }
  };

  if (Notification.permission === "granted") {
    document.querySelector(".register").hidden = true;
  }
}

function registerNotification() {
  Notification.requestPermission((permission) => {
    if (permission === "granted") {
      registerBackgroundSync();
      registerPush();
    } else console.log("Permission was not granted.");
  });
}

function registerBackgroundSync() {
  if (!navigator.serviceWorker) {
    return console.log("Service Worker not supported");
  }

  navigator.serviceWorker.ready
    .then((registration) => registration.periodicSync?.register("sync"))
    .then(() => console.log("Registered background sync"))
    .catch((err) => console.log("Error registering background sync", err));
}

function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, "+")
    .replace(/_/g, "/");

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

// Register for push notifications
function registerPush() {
  if (!navigator.serviceWorker) {
    return console.log("Service Worker not supported");
  }

  navigator.serviceWorker.ready.then((registration) => {
    registration.pushManager.getSubscription().then((subscription) => {
      if (subscription) {
        console.log("Already subscribed");
      } else {
        registration.pushManager
          .subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(
              "BMcy7qUab-2BzEpH4uqV1IfW8Oyq2xSDehMLCqo8fcwXngiK-S4OD5tFE1dSRINrN9lqNBoAE3gRafHwCTOX6kA"
            ),
          })
          .then((subscription) => {
            console.log("Registered push notifications", subscription);
            return fetch("/api/subscribe", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(subscription),
            });
          })
          .catch((err) =>
            console.log("Error registering push notifications", err)
          );
      }
    });
  });
}

// Record audio from microphone
// set up basic variables for app

const record = document.querySelector(".record");
const stop = document.querySelector(".stop");
const soundClips = document.querySelector(".sound-clips");

// disable stop button while not recording

stop.disabled = true;

//main block for doing the audio recording

if (navigator.mediaDevices.getUserMedia) {
  console.log("getUserMedia supported.");

  const constraints = { audio: true };
  let chunks = [];

  let onSuccess = function (stream) {
    const mediaRecorder = new MediaRecorder(stream);

    record.onclick = function () {
      mediaRecorder.start();
      record.style.background = "red";

      stop.disabled = false;
      record.disabled = true;
    };

    stop.onclick = function () {
      mediaRecorder.stop();
      record.style.background = "";
      record.style.color = "";

      stop.disabled = true;
      record.disabled = false;
    };

    mediaRecorder.onstop = async function (e) {
      const clipName = prompt(
        "Enter a name for your sound clip?",
        "My unnamed clip"
      );

      const blob = new Blob(chunks, { type: "audio/ogg; codecs=opus" });
      chunks = [];

      fetch("/api/recordings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: clipName || "My unnamed clip",
          data: await blobToBase64(blob),
        }),
      })
        .then(async (response) => {
          const data = await response.json();
          renderRecording(data);
        })
        .catch((err) => console.log("Failed to upload recording", err));
    };

    mediaRecorder.ondataavailable = function (e) {
      chunks.push(e.data);
    };
  };

  let onError = function (err) {
    console.log("Microphone not available");
    record.hidden = true;
    stop.hidden = true;
  };

  navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);
} else {
  console.log("getUserMedia not supported on your browser!");
  record.hidden = true;
  stop.hidden = true;
}

function blobToBase64(blob) {
  return new Promise((resolve, _) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.readAsDataURL(blob);
  });
}

function renderRecording(recording) {
  const clipContainer = document.createElement("article");
  const clipLabel = document.createElement("p");
  const audio = document.createElement("audio");
  const deleteButton = document.createElement("button");

  clipContainer.classList.add("clip");
  audio.setAttribute("controls", "");
  deleteButton.textContent = "Delete";
  deleteButton.className = "delete offline-hide";
  if (!navigator.onLine) deleteButton.hidden = true;

  clipLabel.textContent = recording.name;

  clipContainer.appendChild(audio);
  clipContainer.appendChild(clipLabel);
  clipContainer.appendChild(deleteButton);
  soundClips.appendChild(clipContainer);

  audio.controls = true;
  audio.src = recording.data;

  deleteButton.onclick = function (e) {
    e.target.closest(".clip").remove();
    fetch(`/api/recordings/${recording.id}`, {
      method: "DELETE",
    });
  };
}

// Render recordings
function renderRecordings(recordings) {
  soundClips.textContent = "";

  recordings?.forEach((recording) => {
    renderRecording(recording);
  });
}

// Get all recordings
fetch("/api/recordings")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Failed to fetch recordings");
    }
    return response.json();
  })
  .then((recordings) => {
    renderRecordings(recordings);
  })
  .catch((err) => console.log("Error fetching recordings", err));

navigator.serviceWorker.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message && message.type.includes("/api/recordings")) {
    console.log("Received new recording", message.data);
    renderRecordings(message.data);
  }
};

// Offline/online
function onOnline() {
  document.querySelectorAll(".offline-hide").forEach((el) => {
    el.hidden = false;
  });
  document.querySelectorAll(".offline-show").forEach((el) => {
    el.hidden = true;
  });
}

function onOffline() {
  document.querySelectorAll(".offline-hide").forEach((el) => {
    el.hidden = true;
  });
  document.querySelectorAll(".offline-show").forEach((el) => {
    el.hidden = false;
  });
}

window.addEventListener("online", onOnline);
window.addEventListener("offline", onOffline);

if (navigator.onLine) onOnline();
else onOffline();
