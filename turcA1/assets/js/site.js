// Le turc pour les francophones · interactions des pages de leçon (repris du site Easy French)
(function () {
  var audio = new Audio(), current = null;
  function stop() { if (current) current.classList.remove("on"); current = null; }
  audio.addEventListener("ended", stop);
  audio.addEventListener("error", stop);
  function play(btn) {
    audio.pause(); stop();
    audio.src = btn.dataset.src;
    audio.playbackRate = btn.dataset.rate ? parseFloat(btn.dataset.rate) : 1;   // les audios sont enregistrés à 90 % : 1.11 = vitesse naturelle
    current = btn; btn.classList.add("on");
    audio.play().catch(stop);
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-src]");
    if (b) { play(b); if (b.closest(".abc")) { document.querySelectorAll(".abc .on").forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on"); } return; }
    var t = e.target.closest("[data-toggle]");
    if (t) {
      var box = document.querySelector(t.dataset.toggle);
      var hidden = box.classList.toggle("hide-en");
      t.textContent = hidden ? t.dataset.show : t.dataset.hide;
      return;
    }
    var r = e.target.closest(".reveal");
    if (r) { r.closest(".step").classList.add("open"); return; }
    var o = e.target.closest(".opts button");
    if (o) {
      var q = o.closest(".q");
      if (q.dataset.done) return;
      q.dataset.done = "1";
      var good = o.hasAttribute("data-ok");
      o.classList.add(good ? "ok" : "no");
      if (!good) q.querySelector("[data-ok]").classList.add("ok");
      q.querySelector(".why").textContent = q.dataset.why;
      if (good) q.dataset.good = "1";
      var all = document.querySelectorAll(".quiz .q"), done = document.querySelectorAll(".quiz .q[data-done]");
      if (all.length === done.length) {
        var n = document.querySelectorAll(".quiz .q[data-good]").length, s = document.querySelector(".score");
        s.textContent = "Ton score : " + n + " / " + all.length + (n >= all.length * 0.8 ? ". Tu es prêt pour la leçon suivante." : ". Revois la vidéo, puis réessaie.");
      }
    }
  });
  // règle graduée : avance avec la lecture de la page
  var bar = document.querySelector(".ruler i");
  if (bar) {
    var tick = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, (window.scrollY / h) * 100) : 0) + "%";
    };
    window.addEventListener("scroll", tick, { passive: true }); tick();
  }
})();
