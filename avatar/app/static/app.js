const statusElement = document.querySelector("#status");
const avatarElement = document.querySelector("#avatar");
const messagesElement = document.querySelector("#messages");
const chatForm = document.querySelector("#chatForm");
const messageInput = document.querySelector("#messageInput");
const micButton = document.querySelector("#micButton");
const voiceToggle = document.querySelector("#voiceToggle");
const memoryForm = document.querySelector("#memoryForm");
const memoryText = document.querySelector("#memoryText");
const memoryKind = document.querySelector("#memoryKind");
const memoryList = document.querySelector("#memoryList");
const memoryCount = document.querySelector("#memoryCount");

let voiceEnabled = false;
const conversationId = crypto.randomUUID ? crypto.randomUUID() : `session-${Date.now()}`;

function addMessage(role, text, error = false) {
  const article = document.createElement("article");
  article.className = `message ${role}${error ? " error" : ""}`;
  const speaker = document.createElement("span");
  speaker.className = "speaker";
  speaker.textContent = role === "user" ? "CHRIS" : error ? "SYSTEM" : "AVATAR";
  const paragraph = document.createElement("p");
  paragraph.textContent = text;
  article.append(speaker, paragraph);
  messagesElement.append(article);
  messagesElement.scrollTop = messagesElement.scrollHeight;
}

function speak(text) {
  if (!voiceEnabled || !window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 1;
  utterance.pitch = 1;
  window.speechSynthesis.speak(utterance);
}

async function checkHealth() {
  try {
    const response = await fetch("/api/health");
    const health = await response.json();
    if (health.model_online) {
      statusElement.textContent = `${health.model} · local model online`;
      statusElement.className = "status online";
    } else {
      statusElement.textContent = `${health.model} · start Ollama`;
      statusElement.className = "status offline";
    }
  } catch {
    statusElement.textContent = "Avatar service offline";
    statusElement.className = "status offline";
  }
}

async function sendChat(message) {
  addMessage("user", message);
  avatarElement.classList.add("thinking");
  const sendButton = chatForm.querySelector("button[type='submit']");
  sendButton.disabled = true;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, conversation_id: conversationId }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || "The avatar could not answer.");
    addMessage("assistant", payload.reply);
    speak(payload.reply);
  } catch (error) {
    addMessage("assistant", error.message, true);
  } finally {
    avatarElement.classList.remove("thinking");
    sendButton.disabled = false;
    messageInput.focus();
  }
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;
  messageInput.value = "";
  await sendChat(message);
});

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});

voiceToggle.addEventListener("click", () => {
  voiceEnabled = !voiceEnabled;
  voiceToggle.textContent = `Voice output: ${voiceEnabled ? "on" : "off"}`;
  if (!voiceEnabled && window.speechSynthesis) window.speechSynthesis.cancel();
});

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.addEventListener("start", () => { micButton.textContent = "Listening…"; });
  recognition.addEventListener("end", () => { micButton.textContent = "Microphone"; });
  recognition.addEventListener("result", (event) => {
    messageInput.value = event.results[0][0].transcript;
    messageInput.focus();
  });
  micButton.addEventListener("click", () => recognition.start());
} else {
  micButton.disabled = true;
  micButton.textContent = "Microphone unavailable";
}

function renderMemory(memory) {
  const card = document.createElement("article");
  card.className = "memory-card";
  const meta = document.createElement("div");
  meta.className = "memory-meta";
  meta.textContent = `#${memory.id} · ${memory.kind}`;
  const content = document.createElement("p");
  content.textContent = memory.content;
  const actions = document.createElement("div");
  actions.className = "memory-actions";
  const approve = document.createElement("button");
  approve.className = "primary";
  approve.textContent = "Approve";
  approve.addEventListener("click", () => reviewMemory(memory.id, "approve"));
  const reject = document.createElement("button");
  reject.className = "danger";
  reject.textContent = "Reject";
  reject.addEventListener("click", () => reviewMemory(memory.id, "reject"));
  actions.append(approve, reject);
  card.append(meta, content, actions);
  return card;
}

async function loadPendingMemories() {
  try {
    const response = await fetch("/api/memories?status=pending");
    const memories = await response.json();
    memoryList.replaceChildren();
    memoryCount.textContent = memories.length;
    if (!memories.length) {
      const empty = document.createElement("p");
      empty.className = "empty";
      empty.textContent = "No pending memories.";
      memoryList.append(empty);
      return;
    }
    memories.forEach((memory) => memoryList.append(renderMemory(memory)));
  } catch {
    memoryList.textContent = "Memory service unavailable.";
  }
}

async function reviewMemory(id, action) {
  await fetch(`/api/memories/${id}/${action}`, { method: "POST" });
  await loadPendingMemories();
  await checkHealth();
}

memoryForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const content = memoryText.value.trim();
  if (!content) return;
  const response = await fetch("/api/memories", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content, kind: memoryKind.value, source: "Chris review queue", confidence: 1 }),
  });
  if (response.ok) {
    memoryText.value = "";
    await loadPendingMemories();
    await checkHealth();
  }
});

checkHealth();
loadPendingMemories();

