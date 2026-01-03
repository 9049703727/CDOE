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
  fetch("/send-otp/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({
      email: document.getElementById("email").value,
      
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "success") {
      new bootstrap.Modal(document.getElementById("otpModal")).show();
      startTimer(300);
    }
  });
}

function verifyOtp() {
  fetch("/verify-otp/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({
      emailOtp: document.getElementById("emailOtp").value,
     
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "verified") {
      document.querySelector(".enrollment-form").submit();
    } else if (data.status === "expired") {
      document.getElementById("otpError").innerText = "OTP expired. Please resend.";
    } else {
      document.getElementById("otpError").innerText = "Invalid OTP";
    }
  });
}

function startTimer(seconds) {
  clearInterval(timerInterval);
  let time = seconds;

  timerInterval = setInterval(() => {
    let min = Math.floor(time / 60);
    let sec = time % 60;
    document.getElementById("timer").innerText =
      `${min}:${sec < 10 ? '0' : ''}${sec}`;
    time--;
    if (time < 0) clearInterval(timerInterval);
  }, 1000);
}
