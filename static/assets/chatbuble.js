const chatElement = document.querySelector('#chat');
const chatOpenElement = document.querySelector('#chat_open');
const chatIconElement = document.querySelector('#chat_icon');
const chatOptionElement = document.querySelector('#chat_option');
const chatEmailElement = document.querySelector('.email');
const chatSendEmailElement = document.querySelector('#send-email');
const chatLiveElement = document.querySelector('.live-chat');
const chatWelcomeElement = document.querySelector('#chat_welcome');
const chatJoinElement = document.querySelector("#chat_join")
const chatRoomElement = document.querySelector('#chat_room');
const chatNameElement = document.querySelector('#chat_name');
const chatLogElement = document.querySelector('#chat_log');
const chatInputElement = document.querySelector('#chat_message_input');
const chatSubmitElement = document.querySelector('#chat_message_submit');

chatIconElement.onclick = function(e){
    e.preventDefault();
    chatIconElement.classList.add('hidden');
    chatOptionElement.classList.remove('hidden');
};
chatEmailElement.onclick = function(e){
    e.preventDefault();
    chatOptionElement.classList.add('hidden');
    chatSendEmailElement.classList.remove('hidden');
};
chatLiveElement.onclick = function(e){
  e.preventDefault();
  chatOptionElement.classList.add('hidden');
  chatWelcomeElement.classList.remove('hidden');
};
chatJoinElement .onclick = function(e){
  e.preventDefault();
  chatWelcomeElement.classList.add('hidden');
  chatRoomElement.classList.remove('hidden');
};



