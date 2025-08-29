// // let CURRENT_CONVO = window.__CONVERSATION_ID__;

// // async function refreshChatList(){
// //   const res = await fetch("/conversations");
// //   const chats = await res.json();
// //   const list = document.getElementById("chatList");
// //   list.innerHTML = "";
// //   chats.forEach(c => {
// //     const li = document.createElement("li");
// //     li.className = "list-group-item d-flex justify-content-between align-items-center";
// //     li.style.cursor = "pointer";
// //     li.dataset.id = c.id;
// //     li.innerHTML = `<span class="${(c.id===CURRENT_CONVO?'fw-semibold text-success':'')}">${escapeHtml(c.title)}</span>` +
// //                    (c.id===CURRENT_CONVO ? ' <span class="badge bg-success">active</span>' : '');
// //     li.addEventListener("click", () => {
// //       window.location = "/?c=" + c.id;
// //     });
// //     list.appendChild(li);
// //   });
// // }

// // async function loadHistory(convoId){
// //   const chatBox = document.getElementById("chat-box");
// //   chatBox.innerHTML = "";
// //   try{
// //     const res = await fetch(`/conversations/${convoId}/history`);
// //     const hist = await res.json();
// //     hist.forEach(turn => appendBubble(turn.content, turn.role === "user" ? "user" : "bot"));
// //   }catch(e){
// //     appendBubble("⚠️ Failed to load history.", "bot");
// //   }
// // }

// // async function newChat(){
// //   const title = "New chat";
// //   const res = await fetch("/conversations", {
// //     method: "POST",
// //     headers: {"Content-Type":"application/json"},
// //     body: JSON.stringify({title})
// //   });
// //   const data = await res.json();
// //   window.location = "/?c=" + data.id;
// // }

// // async function sendMessage() {
// //   const input = document.getElementById("message");
// //   const sendBtn = document.getElementById("sendBtn");
// //   const text = input.value.trim();
// //   if (!text) return;
// //   appendBubble(text, "user");
// //   input.value = "";
// //   sendBtn.disabled = true;

// //   const bilingual = window.__BILINGUAL__ === true;

// //   try {
// //     const res = await fetch("/chat", {
// //       method: "POST",
// //       headers: {"Content-Type":"application/json"},
// //       body: JSON.stringify({message: text, bilingual, conversation_id: CURRENT_CONVO})
// //     });
// //     const data = await res.json();
// //     if (data.reply){
// //       appendBubble(data.reply, "bot");
// //     } else if (data.error){
// //       appendBubble("⚠️ " + data.error, "bot");
// //     }
// //   } catch (err) {
// //     appendBubble("⚠️ Network error: " + err, "bot");
// //   } finally {
// //     sendBtn.disabled = false;
// //     const box = document.getElementById("chat-box");
// //     box.scrollTop = box.scrollHeight;
// //     refreshChatList();
// //   }
// // }

// // document.addEventListener("DOMContentLoaded", async () => {
// //   const newBtn = document.getElementById("newChatBtn");
// //   if (newBtn) newBtn.addEventListener("click", newChat);

// //   const resetBtn = document.getElementById("resetBtn");
// //   if (resetBtn) resetBtn.addEventListener("click", async () => {
// //     await fetch("/reset_conversation", {method:"POST", headers:{'Content-Type':'application/json'}, body: JSON.stringify({conversation_id: CURRENT_CONVO})});
// //     loadHistory(CURRENT_CONVO);
// //   });

// //   await refreshChatList();
// //   await loadHistory(CURRENT_CONVO);

// //   document.getElementById("sendBtn").addEventListener("click", sendMessage);
// //   document.getElementById("message").addEventListener("keydown", (e)=>{
// //     if(e.key === "Enter" && !e.shiftKey){
// //       e.preventDefault();
// //       sendMessage();
// //     }
// //   });
// // });

// // function appendBubble(text, who){
// //   const chatBox = document.getElementById("chat-box");
// //   const wrap = document.createElement("div");
// //   wrap.className = "d-flex align-items-start mb-2 " + (who==="user" ? "justify-content-end" : "justify-content-start");


// //   // avatar
// //   const avatar = document.createElement("img");
// //   if (who === "user") {
// //     const me = document.querySelector("nav img.rounded-circle");
// //     avatar.src = me ? me.src : "/static/img/avatar_default.png";
// //   } else {
// //     avatar.src = "/static/img/ede_avatar.png";
// //   }
// //   avatar.className = "rounded-circle me-2 ms-2";
// //   avatar.style.height = "34px";
// //   avatar.style.width = "34px";
// //   avatar.style.objectFit = "cover";

// //   // bubble
// //   const bubbleWrap = document.createElement("div");
// //   const bubble = document.createElement("div");
// //   bubble.className = "msg " + (who==="user" ? "user" : "bot");
// //   bubble.innerHTML = escapeHtml(text).replace(/\n/g, "<br>");
// //   const time = document.createElement("div");
// //   time.className = "timestamp " + (who==="user" ? "text-end" : "text-start");
// //   time.textContent = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
// //   bubbleWrap.appendChild(bubble);
// //   bubbleWrap.appendChild(time);

// //   if (who === "user") {
// //   wrap.appendChild(bubbleWrap);
// //   wrap.appendChild(avatar);
// // } else {
// //   wrap.appendChild(avatar);
// //   wrap.appendChild(bubbleWrap);
// // }

// //   chatBox.appendChild(wrap);
// //   chatBox.scrollTop = chatBox.scrollHeight;
// // }

// // function escapeHtml(str){
// //   const div = document.createElement("div");
// //   div.textContent = str;
// //   return div.innerHTML;
// // }

// // const chatListMobile = document.getElementById("chatListMobile");
// // const newChatBtnMobile = document.getElementById("newChatBtnMobile");

// // function addChatToList(id, title) {
// //   const makeItem = () => {
// //     const li = document.createElement("li");
// //     li.className = "list-group-item list-group-item-action";
// //     li.textContent = title || `Chat ${id}`;
// //     li.dataset.id = id;
// //     li.style.cursor = "pointer";
// //     li.addEventListener("click", () => {
// //       window.location.href = `/?conversation_id=${id}`;
// //     });
// //     return li;
// //   };

// //   if (chatList) chatList.appendChild(makeItem());
// //   if (chatListMobile) chatListMobile.appendChild(makeItem());
// // }
// // if (chatList) chatList.innerHTML = "";
// // if (chatListMobile) chatListMobile.innerHTML = "";

// // newChatBtnMobile?.addEventListener("click", startNewChat);

// let CURRENT_CONVO = window.__CONVERSATION_ID__;

// async function refreshChatList(){
//   const res = await fetch("/conversations");
//   const chats = await res.json();

//   const listDesktop = document.getElementById("chatList");
//   const listMobile = document.getElementById("chatListMobile");

//   if (listDesktop) listDesktop.innerHTML = "";
//   if (listMobile) listMobile.innerHTML = "";

//   chats.forEach(c => {
//     const liDesktop = makeChatListItem(c);
//     const liMobile = makeChatListItem(c);
//     if (listDesktop) listDesktop.appendChild(liDesktop);
//     if (listMobile) listMobile.appendChild(liMobile);
//   });
// }

// function makeChatListItem(c){
//   const li = document.createElement("li");
//   li.className = "list-group-item d-flex justify-content-between align-items-center";
//   li.style.cursor = "pointer";
//   li.dataset.id = c.id;

//   // title (click to load chat)
//   const titleSpan = document.createElement("span");
//   titleSpan.className = (c.id === CURRENT_CONVO ? "fw-semibold text-success" : "");
//   titleSpan.textContent = c.title || "Untitled chat";
//   titleSpan.addEventListener("click", () => {
//     window.location = "/?c=" + c.id;
//   });

//   // delete button
//   const delBtn = document.createElement("button");
//   delBtn.className = "btn btn-sm btn-outline-danger ms-2";
//   delBtn.innerHTML = "🗑️";
//   delBtn.title = "Delete chat";
//   delBtn.addEventListener("click", async (e) => {
//     e.stopPropagation(); // prevent triggering chat open
//     if (confirm("Are you sure you want to delete this chat?")) {
//       await deleteChat(c.id);
//     }
//   });

//   const left = document.createElement("div");
//   left.className = "d-flex align-items-center";
//   left.appendChild(titleSpan);

//   if (c.id === CURRENT_CONVO) {
//     const badge = document.createElement("span");
//     badge.className = "badge bg-success ms-1";
//     badge.textContent = "active";
//     left.appendChild(badge);
//   }

//   li.appendChild(left);
//   li.appendChild(delBtn);

//   return li;
// }

// async function deleteChat(chatId){
//   try {
//     await fetch(`/conversations/${chatId}`, { method: "DELETE" });
//     if (chatId === CURRENT_CONVO) {
//       // if deleted the active chat, start new one
//       newChat();
//     } else {
//       refreshChatList();
//     }
//   } catch (err) {
//     alert("⚠️ Failed to delete chat: " + err);
//   }
// }

// async function loadHistory(convoId){
//   const chatBox = document.getElementById("chat-box");
//   chatBox.innerHTML = "";
//   try{
//     const res = await fetch(`/conversations/${convoId}/history`);
//     const hist = await res.json();
//     hist.forEach(turn => appendBubble(turn.content, turn.role === "user" ? "user" : "bot"));
//   }catch(e){
//     appendBubble("⚠️ Failed to load history.", "bot");
//   }
// }

// async function newChat(){
//   const title = "New chat";
//   const res = await fetch("/conversations", {
//     method: "POST",
//     headers: {"Content-Type":"application/json"},
//     body: JSON.stringify({title})
//   });
//   const data = await res.json();
//   window.location = "/?c=" + data.id;
// }

// async function sendMessage() {
//   const input = document.getElementById("message");
//   const sendBtn = document.getElementById("sendBtn");
//   const text = input.value.trim();
//   if (!text) return;
//   appendBubble(text, "user");
//   input.value = "";
//   sendBtn.disabled = true;

//   const bilingual = window.__BILINGUAL__ === true;

//   try {
//     const res = await fetch("/chat", {
//       method: "POST",
//       headers: {"Content-Type":"application/json"},
//       body: JSON.stringify({message: text, bilingual, conversation_id: CURRENT_CONVO})
//     });
//     const data = await res.json();
//     if (data.reply){
//       appendBubble(data.reply, "bot");
//     } else if (data.error){
//       appendBubble("⚠️ " + data.error, "bot");
//     }
//   } catch (err) {
//     appendBubble("⚠️ Network error: " + err, "bot");
//   } finally {
//     sendBtn.disabled = false;
//     const box = document.getElementById("chat-box");
//     box.scrollTop = box.scrollHeight;
//     refreshChatList();
//   }
// }

// document.addEventListener("DOMContentLoaded", async () => {
//   const newBtn = document.getElementById("newChatBtn");
//   if (newBtn) newBtn.addEventListener("click", newChat);

//   const newBtnMobile = document.getElementById("newChatBtnMobile");
//   if (newBtnMobile) newBtnMobile.addEventListener("click", newChat);

//   const resetBtn = document.getElementById("resetBtn");
//   if (resetBtn) resetBtn.addEventListener("click", async () => {
//     await fetch("/reset_conversation", {
//       method:"POST",
//       headers:{'Content-Type':'application/json'},
//       body: JSON.stringify({conversation_id: CURRENT_CONVO})
//     });
//     loadHistory(CURRENT_CONVO);
//   });

//   await refreshChatList();
//   await loadHistory(CURRENT_CONVO);

//   document.getElementById("sendBtn").addEventListener("click", sendMessage);
//   document.getElementById("message").addEventListener("keydown", (e)=>{
//     if(e.key === "Enter" && !e.shiftKey){
//       e.preventDefault();
//       sendMessage();
//     }
//   });
// });

// function appendBubble(text, who){
//   const chatBox = document.getElementById("chat-box");
//   const wrap = document.createElement("div");
//   wrap.className = "d-flex align-items-start mb-2 " +
//                    (who==="user" ? "justify-content-end" : "justify-content-start");

//   // avatar
//   const avatar = document.createElement("img");
//   if (who === "user") {
//     const me = document.querySelector("nav img.rounded-circle");
//     avatar.src = me ? me.src : "/static/img/avatar_default.png";
//   } else {
//     avatar.src = "/static/img/ede_avatar.png";
//   }
//   avatar.className = "rounded-circle me-2 ms-2";
//   avatar.style.height = "34px";
//   avatar.style.width = "34px";
//   avatar.style.objectFit = "cover";

//   // bubble
//   const bubbleWrap = document.createElement("div");
//   const bubble = document.createElement("div");
//   bubble.className = "msg " + (who==="user" ? "user" : "bot");
//   bubble.innerHTML = escapeHtml(text).replace(/\n/g, "<br>");
//   const time = document.createElement("div");
//   time.className = "timestamp " + (who==="user" ? "text-end" : "text-start");
//   time.textContent = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
//   bubbleWrap.appendChild(bubble);
//   bubbleWrap.appendChild(time);

//   if (who === "user") {
//     wrap.appendChild(bubbleWrap);
//     wrap.appendChild(avatar);
//   } else {
//     wrap.appendChild(avatar);
//     wrap.appendChild(bubbleWrap);
//   }

//   chatBox.appendChild(wrap);
//   chatBox.scrollTop = chatBox.scrollHeight;
// }

// function escapeHtml(str){
//   const div = document.createElement("div");
//   div.textContent = str;
//   return div.innerHTML;
// }

let CURRENT_CONVO = window.__CONVERSATION_ID__;

async function refreshChatList(){
  const res = await fetch("/conversations");
  const chats = await res.json();

  const listDesktop = document.getElementById("chatList");
  const listMobile = document.getElementById("chatListMobile");

  if (listDesktop) listDesktop.innerHTML = "";
  if (listMobile) listMobile.innerHTML = "";

  chats.forEach(c => {
    const liDesktop = makeChatListItem(c);
    const liMobile = makeChatListItem(c);
    if (listDesktop) listDesktop.appendChild(liDesktop);
    if (listMobile) listMobile.appendChild(liMobile);
  });
}

function makeChatListItem(c){
  const li = document.createElement("li");
  li.className = "list-group-item d-flex justify-content-between align-items-center";
  li.style.cursor = "pointer";
  li.dataset.id = c.id;

  // title (click to load chat)
  const titleSpan = document.createElement("span");
  titleSpan.className = (c.id === CURRENT_CONVO ? "fw-semibold" : "");
  titleSpan.textContent = c.title || "Ibaraẹnisọrọ Alailorukọ";
  titleSpan.addEventListener("click", () => {
    window.location = "/?c=" + c.id;
  });

  // delete button
  const delBtn = document.createElement("button");
  delBtn.className = "btn btn-sm btn-outline-danger ms-2";
  delBtn.innerHTML = "🗑️";
  delBtn.title = "Delete chat";
  delBtn.addEventListener("click", async (e) => {
    e.stopPropagation(); // prevent triggering chat open
    if (confirm("Ṣe o da ọ loju pe o fẹ́ pa ibaraẹnisọrọ yii rẹ́?")) {
      await deleteChat(c.id);
    }
  });

  const left = document.createElement("div");
  left.className = "d-flex align-items-center";
  left.appendChild(titleSpan);

  if (c.id === CURRENT_CONVO) {
    const badge = document.createElement("span");
    badge.className = "badge bg-success ms-1";
    badge.textContent = "active";
    left.appendChild(badge);
  }

  li.appendChild(left);
  li.appendChild(delBtn);

  return li;
}

async function deleteChat(chatId){
  try {
    await fetch(`/conversations/${chatId}`, { method: "DELETE" });
    if (chatId === CURRENT_CONVO) {
      newChat();
    } else {
      refreshChatList();
    }
  } catch (err) {
    alert("⚠️ Failed to delete chat: " + err);
  }
}

async function loadHistory(convoId){
  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML = "";
  try{
    const res = await fetch(`/conversations/${convoId}/history`);
    const hist = await res.json();
    hist.forEach(turn => appendBubble(turn.content, turn.role === "user" ? "user" : "bot"));
  }catch(e){
    appendBubble("⚠️ Failed to load history.", "bot");
  }
}

async function newChat(){
  const title = "New chat";
  const res = await fetch("/conversations", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({title})
  });
  const data = await res.json();
  window.location = "/?c=" + data.id;
}

async function sendMessage() {
  const input = document.getElementById("message");
  const sendBtn = document.getElementById("sendBtn");
  const text = input.value.trim();
  if (!text) return;
  appendBubble(text, "user");
  input.value = "";
  sendBtn.disabled = true;

  // show typing indicator
  addTypingIndicator();

  const bilingual = window.__BILINGUAL__ === true;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({message: text, bilingual, conversation_id: CURRENT_CONVO})
    });
    const data = await res.json();

    // remove typing indicator before showing response
    removeTypingIndicator();

    if (data.reply){
      appendBubble(data.reply, "bot");
    } else if (data.error){
      appendBubble("⚠️ " + data.error, "bot");
    }
  } catch (err) {
    removeTypingIndicator();
    appendBubble("⚠️ Network error: " + err, "bot");
  } finally {
    sendBtn.disabled = false;
    const box = document.getElementById("chat-box");
    box.scrollTop = box.scrollHeight;
    refreshChatList();
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const newBtn = document.getElementById("newChatBtn");
  if (newBtn) newBtn.addEventListener("click", newChat);

  const newBtnMobile = document.getElementById("newChatBtnMobile");
  if (newBtnMobile) newBtnMobile.addEventListener("click", newChat);

  const resetBtn = document.getElementById("resetBtn");
  if (resetBtn) resetBtn.addEventListener("click", async () => {
    await fetch("/reset_conversation", {
      method:"POST",
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({conversation_id: CURRENT_CONVO})
    });
    loadHistory(CURRENT_CONVO);
  });

  await refreshChatList();
  await loadHistory(CURRENT_CONVO);

  document.getElementById("sendBtn").addEventListener("click", sendMessage);
  document.getElementById("message").addEventListener("keydown", (e)=>{
    if(e.key === "Enter" && !e.shiftKey){
      e.preventDefault();
      sendMessage();
    }
  });
});

function appendBubble(text, who){
  const chatBox = document.getElementById("chat-box");
  const wrap = document.createElement("div");
  wrap.className = "d-flex align-items-start mb-2 " +
                   (who==="user" ? "justify-content-end" : "justify-content-start");

  // avatar
  const avatar = document.createElement("img");
  if (who === "user") {
    const me = document.querySelector("nav img.rounded-circle");
    avatar.src = me ? me.src : "/static/img/avatar_default.png";
  } else {
    avatar.src = "/static/img/ede_avatar.png";
  }
  avatar.className = "rounded-circle me-2 ms-2";
  avatar.style.height = "34px";
  avatar.style.width = "34px";
  avatar.style.objectFit = "cover";

  // bubble
  const bubbleWrap = document.createElement("div");
  const bubble = document.createElement("div");
  bubble.className = "msg " + (who==="user" ? "user" : "bot");
  bubble.innerHTML = escapeHtml(text).replace(/\n/g, "<br>");
  const time = document.createElement("div");
  time.className = "timestamp " + (who==="user" ? "text-end" : "text-start");
  time.textContent = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
  bubbleWrap.appendChild(bubble);
  bubbleWrap.appendChild(time);

  if (who === "user") {
    wrap.appendChild(bubbleWrap);
    wrap.appendChild(avatar);
  } else {
    wrap.appendChild(avatar);
    wrap.appendChild(bubbleWrap);
  }

  chatBox.appendChild(wrap);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ---- Typing Indicator ----
function addTypingIndicator() {
  const chatBox = document.getElementById("chat-box");
  const wrap = document.createElement("div");
  wrap.className = "d-flex align-items-start mb-2 justify-content-start";
  wrap.id = "typing-indicator";

  const avatar = document.createElement("img");
  avatar.src = "/static/img/ede_avatar.png";
  avatar.className = "rounded-circle me-2 ms-2";
  avatar.style.height = "34px";
  avatar.style.width = "34px";
  avatar.style.objectFit = "cover";

  const bubble = document.createElement("div");
  bubble.className = "msg bot";
  bubble.innerHTML = `
    <div class="typing-indicator">
      <span></span><span></span><span></span>
    </div>`;

  wrap.appendChild(avatar);
  wrap.appendChild(bubble);
  chatBox.appendChild(wrap);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTypingIndicator() {
  const indicator = document.getElementById("typing-indicator");
  if (indicator) indicator.remove();
}

function escapeHtml(str){
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
