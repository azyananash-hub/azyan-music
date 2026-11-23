import "@fontsource/cormorant-garamond/400.css";
import "@fontsource/cormorant-garamond/500.css";
import "@fontsource/manrope/400.css";
import "@fontsource/manrope/500.css";
import "@fontsource/manrope/600.css";
import "./styles.css";

import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";

gsap.registerPlugin(ScrollTrigger);

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const isDesktop = () => window.matchMedia("(min-width: 900px)").matches;

document.documentElement.classList.add("js");
document.getElementById("year").textContent = String(new Date().getFullYear());

/* ---------- Smooth scroll (Lenis) ---------- */
let lenis = null;
if (!reduceMotion) {
  lenis = new Lenis({ duration: 1.1, smoothWheel: true });
  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);
}

/* ---------- Simple fades (used in both modes) ---------- */
const revealIO = new IntersectionObserver(
  (entries) => {
    for (const e of entries) {
      if (e.isIntersecting) {
        e.target.classList.add("is-in");
        revealIO.unobserve(e.target);
      }
    }
  },
  { threshold: 0.15 }
);
document.querySelectorAll(".reveal").forEach((el) => revealIO.observe(el));

/* ---------- Hero ---------- */
if (!reduceMotion) {
  gsap.from("#hero .display-xl .line > span", {
    yPercent: 110,
    duration: 1.2,
    ease: "power4.out",
    stagger: 0.12,
    delay: 0.2,
  });
  gsap.from(".hero-copy .eyebrow, .hero-copy .lead, .hero-actions", {
    opacity: 0,
    y: 20,
    duration: 1,
    ease: "power2.out",
    stagger: 0.1,
    delay: 0.9,
  });

  // Jet approach and cloud parallax, scrubbed to the hero's scroll range.
  const heroTl = gsap.timeline({
    scrollTrigger: { trigger: "#hero", start: "top top", end: "bottom top", scrub: 0.6 },
  });
  gsap.set(".jet", { xPercent: -50 });
  heroTl
    .fromTo(".jet", { scale: 0.8, y: 0 }, { scale: 1.05, y: -80, ease: "none" }, 0)
    .fromTo(".cloud-mid", { yPercent: 0 }, { yPercent: -35, xPercent: 4, ease: "none" }, 0)
    .fromTo(".cloud-near", { yPercent: 20 }, { yPercent: -90, ease: "none" }, 0)
    .to(".hero-copy", { y: -60, opacity: 0.2, ease: "none" }, 0);
}

/* ---------- Manifesto: words light up on scroll ---------- */
const statement = document.querySelector("[data-words]");
if (statement) {
  const words = statement.textContent.trim().split(/\s+/);
  statement.setAttribute("aria-label", words.join(" "));
  statement.innerHTML = words
    .map((w) => `<span class="word" aria-hidden="true">${w}</span>`)
    .join(" ");
  const spans = statement.querySelectorAll(".word");
  if (!reduceMotion) {
    gsap.fromTo(
      spans,
      { opacity: 0.22 },
      {
        opacity: 1,
        ease: "none",
        stagger: 0.1,
        scrollTrigger: { trigger: statement, start: "top 80%", end: "bottom 45%", scrub: true },
      }
    );
  }
}

/* ---------- Window: frame zooms until the sky fills the screen ---------- */
if (!reduceMotion && isDesktop()) {
  const winTl = gsap.timeline({
    scrollTrigger: {
      trigger: "#window",
      start: "top top",
      end: "+=250%",
      pin: true,
      scrub: 0.6,
      anticipatePin: 1,
    },
  });
  winTl
    .fromTo(".window-frame", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, ease: "none", duration: 1 })
    .to(".window-copy", { opacity: 0, ease: "none", duration: 0.5 }, "<")
    .to(".window-frame", { scale: 9, ease: "power1.in", duration: 2 });
}

/* ---------- Cabin: horizontal pin on desktop ---------- */
if (!reduceMotion && isDesktop()) {
  const track = document.querySelector("[data-track]");
  const distance = () => track.scrollWidth - window.innerWidth + 2 * parseFloat(getComputedStyle(document.querySelector(".cabin-pin")).paddingLeft);
  gsap.to(track, {
    x: () => -Math.max(0, distance()),
    ease: "none",
    scrollTrigger: {
      trigger: ".cabin",
      start: "top top",
      end: () => `+=${Math.max(0, distance())}`,
      pin: ".cabin-pin",
      scrub: 0.6,
      invalidateOnRefresh: true,
      anticipatePin: 1,
    },
  });
}

/* ---------- Aircraft: draw profile, count specs ---------- */
const profileLine = document.querySelector(".profile-line");
const counters = document.querySelectorAll("[data-count]");
const aircraftIO = new IntersectionObserver(
  (entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      aircraftIO.disconnect();
      if (reduceMotion) {
        counters.forEach((el) => (el.textContent = Number(el.dataset.count).toLocaleString("en-US")));
        return;
      }
      gsap.to(profileLine, { strokeDashoffset: 0, duration: 2, ease: "power2.inOut" });
      counters.forEach((el) => {
        const target = Number(el.dataset.count);
        const obj = { v: 0 };
        gsap.to(obj, {
          v: target,
          duration: 1.6,
          ease: "power2.out",
          onUpdate: () => (el.textContent = Math.round(obj.v).toLocaleString("en-US")),
        });
      });
    }
  },
  { threshold: 0.3 }
);
const aircraftEl = document.getElementById("aircraft");
if (aircraftEl) aircraftIO.observe(aircraftEl);

/* ---------- Enquiry form: client-side validation only ---------- */
const form = document.getElementById("enquiry-form");
const status = document.getElementById("form-status");

const rules = {
  name: {
    check: (v) => v.trim().length >= 2 || "Please enter your full name.",
  },
  email: {
    check: (v) =>
      /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) || "Enter a valid email address.",
  },
  route: {
    check: (v) => v.trim().length >= 3 || "Enter the departure and destination.",
  },
  date: {
    check: (v) => {
      if (!v) return "Choose a date.";
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      return new Date(v) >= today || "The date must be today or later.";
    },
  },
  pax: {
    check: (v) => {
      const n = Number(v);
      return (Number.isInteger(n) && n >= 1 && n <= 12) || "Between 1 and 12 passengers.";
    },
  },
};

function validateField(input) {
  const rule = rules[input.name];
  const errorEl = document.getElementById(`e-${input.name}`);
  const result = rule ? rule.check(input.value) : true;
  const message = result === true ? "" : result;
  errorEl.textContent = message;
  input.setAttribute("aria-invalid", message ? "true" : "false");
  return !message;
}

form.querySelectorAll("input[name], textarea[name]").forEach((input) => {
  input.addEventListener("blur", () => validateField(input));
  input.addEventListener("input", () => {
    if (input.getAttribute("aria-invalid") === "true") validateField(input);
  });
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const fields = [...form.querySelectorAll("input[name]")];
  const results = fields.map(validateField);
  const firstBad = fields.find((_, i) => !results[i]);
  if (firstBad) {
    status.textContent = "Please fix the highlighted fields.";
    status.className = "status is-warn";
    firstBad.focus();
    return;
  }
  // Intentionally no network call: no backend is connected yet.
  status.textContent =
    "Your enquiry looks complete. This demo has no backend, so nothing was sent.";
  status.className = "status";
});

window.addEventListener("resize", () => ScrollTrigger.refresh());
