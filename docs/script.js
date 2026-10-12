/**
 * pdf-translator 仓库主页交互
 * 1) 复制安装命令  2) 本地时钟  3) 目录高亮
 */
(function () {
  'use strict';

  /* ---------- 1) 复制安装命令 ---------- */
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      var done = function () {
        var old = btn.textContent;
        btn.textContent = '已复制 ✓';
        btn.classList.add('ok');
        setTimeout(function () {
          btn.textContent = old;
          btn.classList.remove('ok');
        }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { fallback(text, done); });
      } else {
        fallback(text, done);
      }
    });
  });

  function fallback(text, cb) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); cb(); } catch (e) { /* noop */ }
    document.body.removeChild(ta);
  }

  /* ---------- 2) 本地时钟 ---------- */
  var clock = document.getElementById('clock');
  if (clock) {
    var tick = function () {
      var d = new Date();
      var p = function (n) { return (n < 10 ? '0' : '') + n; };
      clock.textContent = p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds());
    };
    tick();
    setInterval(tick, 1000);
  }

  /* ---------- 3) 目录当前章节高亮 ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
  var map = {};
  links.forEach(function (a) {
    var el = document.querySelector(a.getAttribute('href'));
    if (el) { map[a.getAttribute('href').slice(1)] = a; }
  });
  if ('IntersectionObserver' in window && Object.keys(map).length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var a = map[en.target.id];
        if (!a) { return; }
        if (en.isIntersecting) {
          links.forEach(function (x) { x.style.color = ''; });
          a.style.color = 'var(--cinnabar)';
        }
      });
    }, { rootMargin: '-56px 0px -70% 0px' });
    Object.keys(map).forEach(function (id) {
      io.observe(document.getElementById(id));
    });
  }
})();
