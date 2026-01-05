// Chatbot functionality
class Chatbot {
  constructor() {
    this.messages = [];
    this.isOpen = false;
    this.init();
  }

  init() {
    this.createChatbotHTML();
    this.attachEventListeners();
    this.addWelcomeMessage();
  }

  createChatbotHTML() {
    const chatbotHTML = `
      <div class="chatbot-container" id="chatbotContainer">
        <div class="chatbot-window" id="chatbotWindow">
          <div class="chatbot-header">
            <h3><i class="bi bi-chat-dots me-2"></i>CDOE Assistant</h3>
            <button class="close-btn" id="chatbotCloseBtn">&times;</button>
          </div>
          <div class="chatbot-messages" id="chatbotMessages"></div>
          <div class="chatbot-input-area">
            <input type="text" class="chatbot-input" id="chatbotInput" placeholder="Type your message..." />
            <button class="chatbot-send-btn" id="chatbotSendBtn">
              <i class="bi bi-send"></i>
            </button>
          </div>
        </div>
        <button class="chatbot-button" id="chatbotButton">
          <i class="bi bi-chat-dots-fill"></i>
        </button>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', chatbotHTML);
  }

  attachEventListeners() {
    const button = document.getElementById('chatbotButton');
    const closeBtn = document.getElementById('chatbotCloseBtn');
    const sendBtn = document.getElementById('chatbotSendBtn');
    const input = document.getElementById('chatbotInput');
    const window = document.getElementById('chatbotWindow');

    button.addEventListener('click', () => this.toggleChatbot());
    closeBtn.addEventListener('click', () => this.closeChatbot());
    sendBtn.addEventListener('click', () => this.sendMessage());
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        this.sendMessage();
      }
    });
  }

  toggleChatbot() {
    this.isOpen = !this.isOpen;
    const window = document.getElementById('chatbotWindow');
    const button = document.getElementById('chatbotButton');
    
    if (this.isOpen) {
      window.classList.add('active');
      button.classList.add('active');
      document.getElementById('chatbotInput').focus();
    } else {
      window.classList.remove('active');
      button.classList.remove('active');
    }
  }

  closeChatbot() {
    this.isOpen = false;
    const window = document.getElementById('chatbotWindow');
    const button = document.getElementById('chatbotButton');
    window.classList.remove('active');
    button.classList.remove('active');
  }

  addWelcomeMessage() {
    const welcomeMessage = "Hello! I'm CDOE Assistant. How can I help you today?";
    const quickReplies = [
      "Courses",
      "Registration",
      "Inquiry",
      "Contact Info"
    ];
    this.addMessage('bot', welcomeMessage, quickReplies);
  }

  addMessage(sender, text, quickReplies = null) {
    const messagesContainer = document.getElementById('chatbotMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const time = new Date().toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });

    const avatar = sender === 'bot' 
      ? '<i class="bi bi-robot"></i>' 
      : '<i class="bi bi-person"></i>';

    messageDiv.innerHTML = `
      <div class="message-avatar">${avatar}</div>
      <div>
        <div class="message-content">${this.formatMessage(text)}</div>
        <div class="message-time">${time}</div>
        ${quickReplies ? this.createQuickReplies(quickReplies) : ''}
      </div>
    `;

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    this.messages.push({ sender, text, time });
  }

  createQuickReplies(replies) {
    const repliesHTML = replies.map(reply => 
      `<button class="quick-reply-btn" onclick="chatbot.sendQuickReply('${reply}')">${reply}</button>`
    ).join('');
    return `<div class="quick-replies">${repliesHTML}</div>`;
  }

  formatMessage(text) {
    // Convert URLs to links
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, '<a href="$1" target="_blank" style="color: inherit; text-decoration: underline;">$1</a>');
  }

  sendQuickReply(text) {
    this.addMessage('user', text);
    setTimeout(() => this.processMessage(text), 500);
  }

  sendMessage() {
    const input = document.getElementById('chatbotInput');
    const message = input.value.trim();

    if (!message) return;

    this.addMessage('user', message);
    input.value = '';

    // Show typing indicator
    this.showTypingIndicator();

    // Process message after a short delay
    setTimeout(() => {
      this.hideTypingIndicator();
      this.processMessage(message);
    }, 1000);
  }

  showTypingIndicator() {
    const messagesContainer = document.getElementById('chatbotMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
      <div class="message-avatar"><i class="bi bi-robot"></i></div>
      <div class="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
      </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
      typingIndicator.remove();
    }
  }

  processMessage(message) {
    const lowerMessage = message.toLowerCase();
    let response = '';
    let quickReplies = null;

    // Greeting patterns
    if (this.matchesPattern(lowerMessage, ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening'])) {
      response = "Hello! Welcome to Gujarat University CDOE. How can I assist you today?";
      quickReplies = ["Courses", "Registration", "Inquiry", "Contact Info"];
    }
    // Courses
    else if (this.matchesPattern(lowerMessage, ['course', 'courses', 'program', 'programs', 'study', 'education'])) {
      response = "We offer various online courses and programs. You can view all available courses on our <a href='/courses.html' style='color: #136ad5; text-decoration: underline;'>Courses page</a>. Would you like to know more about a specific course?";
      quickReplies = ["View Courses", "Inquiry Form", "Registration"];
    }
    // Registration
    else if (this.matchesPattern(lowerMessage, ['register', 'registration', 'admission', 'apply', 'enroll', 'enrollment'])) {
      response = "To register for courses, please visit our registration portal: <a href='https://online.gujaratuniversity.ac.in/admission/Registration' target='_blank' style='color: #136ad5; text-decoration: underline;'>Online Registration</a>. You can also submit an inquiry form for more information.";
      quickReplies = ["Inquiry Form", "Courses", "Contact Info"];
    }
    // Inquiry
    else if (this.matchesPattern(lowerMessage, ['inquiry', 'inquiries', 'query', 'question', 'help', 'information'])) {
      response = "You can submit an inquiry form to get more information about our courses and programs. Click here to fill the <a href='/inquiry/' style='color: #136ad5; text-decoration: underline;'>Inquiry Form</a>.";
      quickReplies = ["View Courses", "Registration", "Contact Info"];
    }
    // Contact
    else if (this.matchesPattern(lowerMessage, ['contact', 'email', 'phone', 'address', 'location', 'reach'])) {
      response = "You can contact us through our <a href='/contact/' style='color: #136ad5; text-decoration: underline;'>Contact Us page</a>. We're here to help you with any questions about our courses and programs.";
      quickReplies = ["Inquiry Form", "Courses", "Registration"];
    }
    // LMS/Login
    else if (this.matchesPattern(lowerMessage, ['lms', 'login', 'student portal', 'portal', 'dashboard'])) {
      response = "To access the Learning Management System (LMS), please visit: <a href='https://www.online-gu.com/' target='_blank' style='color: #136ad5; text-decoration: underline;'>LMS Login</a>";
      quickReplies = ["Registration", "Courses", "Contact Info"];
    }
    // IKS Course
    else if (this.matchesPattern(lowerMessage, ['iks', 'indian knowledge system'])) {
      response = "For IKS (Indian Knowledge System) Course Registration, please visit: <a href='/iks_course_registration.html' style='color: #136ad5; text-decoration: underline;'>IKS Course Registration</a>";
      quickReplies = ["Regular Courses", "Registration", "Inquiry Form"];
    }
    // About
    else if (this.matchesPattern(lowerMessage, ['about', 'who are you', 'what is cdoe', 'university'])) {
      response = "CDOE (Center for Distance and Online Education) is part of Gujarat University, offering online education programs. You can learn more on our <a href='/about.html' style='color: #136ad5; text-decoration: underline;'>About Us page</a>.";
      quickReplies = ["Courses", "Registration", "Contact Info"];
    }
    // Fees/Pricing
    else if (this.matchesPattern(lowerMessage, ['fee', 'fees', 'price', 'pricing', 'cost', 'payment'])) {
      response = "Course fees vary by program. For detailed pricing information, please check the individual course pages or submit an inquiry form. Our team will provide you with complete fee structure details.";
      quickReplies = ["View Courses", "Inquiry Form", "Contact Info"];
    }
    // Default response
    else {
      response = "I'm here to help! I can assist you with information about courses, registration, inquiries, and more. What would you like to know?";
      quickReplies = ["Courses", "Registration", "Inquiry Form", "Contact Info"];
    }

    this.addMessage('bot', response, quickReplies);
  }

  matchesPattern(text, patterns) {
    return patterns.some(pattern => text.includes(pattern));
  }
}

// Initialize chatbot when DOM is ready
let chatbot;
document.addEventListener('DOMContentLoaded', function() {
  chatbot = new Chatbot();
});
