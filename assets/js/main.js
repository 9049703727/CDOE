/**
* Template Name: Learner
* Template URL: https://bootstrapmade.com/learner-bootstrap-course-template/
* Updated: Jul 08 2025 with Bootstrap v5.3.7
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function () {
  "use strict";

  /* ===============================
   SCROLL HEADER
  =============================== */
  function toggleScrolled() {
    const body = document.querySelector("body");
    const header = document.querySelector("#header");
    if (
      !header ||
      (!header.classList.contains("scroll-up-sticky") &&
        !header.classList.contains("sticky-top") &&
        !header.classList.contains("fixed-top"))
    ) return;

    window.scrollY > 100
      ? body.classList.add("scrolled")
      : body.classList.remove("scrolled");
  }

  document.addEventListener("scroll", toggleScrolled);
  window.addEventListener("load", toggleScrolled);

  /* ===============================
   MOBILE NAV
  =============================== */
  const mobileNavToggleBtn = document.querySelector(".mobile-nav-toggle");

  function mobileNavToggle() {
    document.body.classList.toggle("mobile-nav-active");
    mobileNavToggleBtn.classList.toggle("bi-list");
    mobileNavToggleBtn.classList.toggle("bi-x");
  }

  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener("click", mobileNavToggle);
  }

  document.querySelectorAll("#navmenu a").forEach((link) => {
    link.addEventListener("click", () => {
      if (document.body.classList.contains("mobile-nav-active")) {
        mobileNavToggle();
      }
    });
  });

  document.querySelectorAll(".navmenu .toggle-dropdown").forEach((item) => {
    item.addEventListener("click", function (e) {
      e.preventDefault();
      this.parentNode.classList.toggle("active");
      this.parentNode.nextElementSibling.classList.toggle("dropdown-active");
      e.stopImmediatePropagation();
    });
  });

  /* ===============================
   PRELOADER
  =============================== */
  const preloader = document.querySelector("#preloader");
  if (preloader) {
    window.addEventListener("load", () => preloader.remove());
  }

  /* ===============================
   SCROLL TOP
  =============================== */
  const scrollTop = document.querySelector(".scroll-top");

  function toggleScrollTop() {
    if (!scrollTop) return;
    window.scrollY > 100
      ? scrollTop.classList.add("active")
      : scrollTop.classList.remove("active");
  }

  scrollTop?.addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  window.addEventListener("load", toggleScrollTop);
  document.addEventListener("scroll", toggleScrollTop);

  /* ===============================
   AOS
  =============================== */
  window.addEventListener("load", () => {
    AOS.init({
      duration: 600,
      easing: "ease-in-out",
      once: true,
      mirror: false,
    });
  });

  /* ===============================
   PURE COUNTER
  =============================== */
  new PureCounter();

})();

/* ===============================
 FORM VALIDATION
=============================== */
document.getElementById("mobile")?.addEventListener("input", function () {
  this.value = this.value.replace(/[^0-9]/g, "");
});

const form = document.querySelector(".enrollment-form");
if (form) {
  const emailInput = document.getElementById("email");
  const mobileInput = document.getElementById("mobile");
  const emailError = document.getElementById("emailError");
  const mobileError = document.getElementById("mobileError");

  form.addEventListener("submit", function (e) {
    let valid = true;

    const emailPattern = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/;
    if (!emailPattern.test(emailInput.value)) {
      emailError.style.display = "block";
      valid = false;
    } else emailError.style.display = "none";

    const mobilePattern = /^[0-9]{10}$/;
    if (!mobilePattern.test(mobileInput.value)) {
      mobileError.style.display = "block";
      valid = false;
    } else mobileError.style.display = "none";

    if (!valid) e.preventDefault();
  });
}

/* ===============================
 IKS COURSE LOGIC
=============================== */
document.addEventListener("DOMContentLoaded", function () {
  const iksCourse = document.getElementById("iks_course");
  if (!iksCourse) return;

  const gcasReg = document.getElementById("gcas_reg_no");
  const gcasConf = document.getElementById("gcas_conf_no");
  const gcasRegStar = document.getElementById("gcas_reg_star");
  const gcasConfStar = document.getElementById("gcas_conf_star");

  iksCourse.addEventListener("change", function () {
    const required = this.value === "IKS_1";
    gcasReg.required = required;
    gcasConf.required = required;
    gcasRegStar.classList.toggle("d-none", !required);
    gcasConfStar.classList.toggle("d-none", !required);
    if (!required) {
      gcasReg.value = "";
      gcasConf.value = "";
    }
  });

  iksCourse.dispatchEvent(new Event("change"));
});

/* ===============================
 RANKINGS SLIDER (CUSTOM)
=============================== */
document.addEventListener("DOMContentLoaded", function () {
  const track = document.getElementById("rankingsTrack");
  const items = document.querySelectorAll(".ranking-item");

  if (!track || items.length === 0) return;

  let index = 0;
  const itemWidth = items[0].offsetWidth + 20;

  window.scrollRankings = function (direction) {
    const maxIndex = items.length - 1;
    index += direction;
    index = Math.max(0, Math.min(index, maxIndex));
    track.style.transform = `translateX(-${index * itemWidth}px)`;
  };
});

/* ===============================
 TESTIMONIALS SWIPER
=============================== */
document.addEventListener("DOMContentLoaded", function () {
  const swiperEl = document.getElementById("testimonialsSwiper");
  const prevBtn = document.getElementById("testimonialPrevBtn");
  const nextBtn = document.getElementById("testimonialNextBtn");

  if (!swiperEl || !prevBtn || !nextBtn || typeof Swiper === "undefined") return;

  new Swiper("#testimonialsSwiper", {
    loop: true,
    speed: 600,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    slidesPerView: 1,
    spaceBetween: 30,
    navigation: {
      nextEl: "#testimonialNextBtn",
      prevEl: "#testimonialPrevBtn",
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    breakpoints: {
      768: { slidesPerView: 2 },
      992: { slidesPerView: 3 },
    },
  });
});

document.addEventListener("DOMContentLoaded", function () {

  const track = document.getElementById("rankingsTrack");
  const items = document.querySelectorAll(".ranking-item");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  if (!track || items.length === 0 || !prevBtn || !nextBtn) {
    return;
  }

  let currentIndex = 0;

  function getItemWidth() {
    return items[0].offsetWidth + 20; // card width + gap
  }

  function updateSlider() {
    track.style.transform = `translateX(-${currentIndex * getItemWidth()}px)`;
  }

  nextBtn.addEventListener("click", function () {
    if (currentIndex < items.length - 1) {
      currentIndex++;
      updateSlider();
    }
  });

  prevBtn.addEventListener("click", function () {
    if (currentIndex > 0) {
      currentIndex--;
      updateSlider();
    }
  });

  // Optional: auto slide
  setInterval(function () {
    if (currentIndex < items.length - 1) {
      currentIndex++;
    } else {
      currentIndex = 0;
    }
    updateSlider();
  }, 4000);

});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(cookie => {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
      }
    });
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');
let timerInterval;

function sendOtp() {
  const emailInput = document.getElementById("email");
  const email = emailInput.value;
  const errorDiv = document.getElementById("otpError");
  
  // Clear previous errors
  if (errorDiv) {
    errorDiv.innerText = "";
  }
  
  if (!email) {
    if (errorDiv) {
      errorDiv.innerText = "Please enter your email address first.";
    }
    return;
  }
  
  fetch("/send-otp/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({
      email: email
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "success") {
      // Clear OTP input and error
      const otpInput = document.getElementById("emailOtp");
      if (otpInput) {
        otpInput.value = "";
      }
      if (errorDiv) {
        errorDiv.innerText = "";
      }
      // Hide resend link
      const resendLink = document.getElementById("resendLink");
      if (resendLink) {
        resendLink.style.display = "none";
      }
      // Show modal and start timer
      const modalElement = document.getElementById("otpModal");
      if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
        startTimer(300);
      }
    } else {
      // Show error message
      if (errorDiv) {
        errorDiv.innerText = data.message || "Failed to send OTP. Please try again.";
      }
    }
  })
  .catch(error => {
    console.error("Error sending OTP:", error);
    if (errorDiv) {
      errorDiv.innerText = "An error occurred. Please try again.";
    }
  });
}

function verifyOtp() {
  const otpInput = document.getElementById("emailOtp");
  const userOtp = otpInput ? otpInput.value.trim() : "";
  const errorDiv = document.getElementById("otpError");
  const modalElement = document.getElementById("otpModal");
  
  // Clear previous errors
  if (errorDiv) {
    errorDiv.innerText = "";
  }
  
  if (!userOtp) {
    if (errorDiv) {
      errorDiv.innerText = "Please enter the OTP.";
    }
    return;
  }
  
  if (userOtp.length !== 6) {
    if (errorDiv) {
      errorDiv.innerText = "Please enter a valid 6-digit OTP.";
    }
    return;
  }
  
  fetch("/verify-otp/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({
      emailOtp: userOtp
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "verified") {
      // Close the modal
      if (modalElement) {
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) {
          modal.hide();
        }
      }
      // Clear timer
      clearInterval(timerInterval);
      // Submit the form
      const form = document.querySelector(".enrollment-form");
      if (form) {
        form.submit();
      }
    } else if (data.status === "expired") {
      if (errorDiv) {
        errorDiv.innerText = data.message || "OTP expired. Please resend.";
      }
      // Show resend link
      const resendLink = document.getElementById("resendLink");
      if (resendLink) {
        resendLink.style.display = "block";
      }
      clearInterval(timerInterval);
    } else if (data.status === "invalid") {
      if (errorDiv) {
        errorDiv.innerText = data.message || "Invalid OTP. Please try again.";
      }
    } else if (data.status === "error") {
      if (errorDiv) {
        errorDiv.innerText = data.message || "An error occurred. Please try again.";
      }
    } else {
      if (errorDiv) {
        errorDiv.innerText = data.message || "Invalid OTP. Please try again.";
      }
    }
  })
  .catch(error => {
    console.error("Error verifying OTP:", error);
    if (errorDiv) {
      errorDiv.innerText = "An error occurred. Please try again.";
    }
  });
}

function resendOtp() {
  const errorDiv = document.getElementById("otpError");
  const resendLink = document.getElementById("resendLink");
  
  // Clear previous errors
  if (errorDiv) {
    errorDiv.innerText = "";
  }
  
  // Hide resend link temporarily
  if (resendLink) {
    resendLink.style.display = "none";
  }
  
  // Clear OTP input
  const otpInput = document.getElementById("emailOtp");
  if (otpInput) {
    otpInput.value = "";
  }
  
  // Send new OTP
  sendOtp();
}

function startTimer(seconds) {
  clearInterval(timerInterval);
  let time = seconds;
  const timerElement = document.getElementById("timer");
  const resendLink = document.getElementById("resendLink");

  timerInterval = setInterval(() => {
    let min = Math.floor(time / 60);
    let sec = time % 60;
    if (timerElement) {
      timerElement.innerText = `${min}:${sec < 10 ? '0' : ''}${sec}`;
    }
    time--;
    if (time < 0) {
      clearInterval(timerInterval);
      // Show resend link when timer expires
      if (resendLink) {
        resendLink.style.display = "block";
      }
      if (timerElement) {
        timerElement.innerText = "00:00";
      }
    }
  }, 1000);
}


  const videoSwiper = new Swiper('#videoSwiper', {
    loop: true,
    slidesPerView: 1,
    spaceBetween: 30,
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '#videoNextBtn',
      prevEl: '#videoPrevBtn',
    },
    breakpoints: {
      768: {
        slidesPerView: 2
      },
      1200: {
        slidesPerView: 3
      }
    }
  });

// Dynamic form validation based on selected IKS course
// Dynamic form validation based on selected IKS course
document.addEventListener('DOMContentLoaded', function () {
    const courseSelect = document.getElementById('iks_course');
    const gcasRegNo = document.getElementById('gcas_reg_no');
    const gcasConfNo = document.getElementById('gcas_conf_no');
    const enrollmentNo = document.getElementById('enrollment_no');

    const gcasRegStar = document.getElementById('gcas_reg_star');
    const gcasConfStar = document.getElementById('gcas_conf_star');
    const enrollmentStar = document.getElementById('enrollment_star'); // Make sure you have this in HTML

    courseSelect.addEventListener('change', function () {
        const selectedCourse = this.value;

        if (selectedCourse === 'IKS_1') {
            // IKS_1: GCAS required, Enrollment optional
            gcasRegNo.required = true;
            gcasConfNo.required = true;
            enrollmentNo.required = false;

            gcasRegStar.classList.remove('d-none');
            gcasConfStar.classList.remove('d-none');
            enrollmentStar.classList.add('d-none');
        } else if (selectedCourse === 'IKS_2') {
            // IKS_2: Enrollment required, GCAS optional
            gcasRegNo.required = false;
            gcasConfNo.required = false;
            enrollmentNo.required = true;

            gcasRegStar.classList.add('d-none');
            gcasConfStar.classList.add('d-none');
            enrollmentStar.classList.remove('d-none');
        } else if (selectedCourse === 'IKS_3') {
            // IKS_3: Enrollment required, GCAS optional
            gcasRegNo.required = false;
            gcasConfNo.required = false;
            enrollmentNo.required = true;

            gcasRegStar.classList.add('d-none');
            gcasConfStar.classList.add('d-none');
            enrollmentStar.classList.remove('d-none');
        } else {
            // Default: none required
            gcasRegNo.required = false;
            gcasConfNo.required = false;
            enrollmentNo.required = false;

            gcasRegStar.classList.add('d-none');
            gcasConfStar.classList.add('d-none');
            enrollmentStar.classList.add('d-none');
        }
    });
});
function openOtpModal() {
  // Validate form before sending OTP
  const form = document.querySelector(".enrollment-form");
  if (!form) {
    alert("Form not found. Please refresh the page.");
    return;
  }
  
  // Check if form is valid
  if (!form.checkValidity()) {
    // Trigger HTML5 validation
    form.reportValidity();
    return;
  }
  
  // Validate email field specifically
  const emailInput = document.getElementById("email");
  if (!emailInput || !emailInput.value) {
    alert("Please enter your email address.");
    if (emailInput) {
      emailInput.focus();
    }
    return;
  }
  
  // Send OTP (this will show the modal)
  sendOtp();
}
document.getElementById("verify-btn").addEventListener("click", function() {
  const otp = document.getElementById("otp").value;

  fetch("/verify-otp/", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({ otp: otp })
  })
  .then(res => res.json())
  .then(data => {
      if (data.success) {
          window.location.href = "/success/";
      } else {
          alert("Invalid OTP");
      }
  });
});
