(function () {
  'use strict';

  // 移动端菜单
  var btn = document.querySelector('.menu-btn');
  var menu = document.querySelector('.nav-menu');
  if (btn && menu) {
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        menu.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // 年份
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // 入场动效（尊重系统减少动效设置）
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items = document.querySelectorAll('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
    items.forEach(function (el) { io.observe(el); });
  }

  // FAQ 单开
  document.querySelectorAll('.faq details').forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open) {
        document.querySelectorAll('.faq details').forEach(function (other) {
          if (other !== d) other.open = false;
        });
      }
    });
  });

  // 分类筛选 + 分页（案例与资讯 / 建站观察）
  document.querySelectorAll('.pager').forEach(function (pager) {
    var id = pager.getAttribute('data-pager');
    var per = parseInt(pager.getAttribute('data-per-page'), 10) || 6;
    var cards = Array.prototype.slice.call(pager.querySelectorAll('[data-pager-item="' + id + '"]'));
    var controls = pager.querySelector('[data-pager-controls="' + id + '"]');
    var filters = Array.prototype.slice.call(document.querySelectorAll('[data-pager-filter="' + id + '"]'));
    if (!controls || !cards.length) { return; }
    var page = 1;
    var cat = 'all';

    function matches() {
      return cards.filter(function (c) {
        return cat === 'all' || c.getAttribute('data-cat') === cat;
      });
    }

    function button(label, target, disabled, active) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'pager-btn' + (active ? ' active' : '');
      b.textContent = label;
      b.disabled = !!disabled;
      b.addEventListener('click', function () { page = target; render(); });
      controls.appendChild(b);
    }

    function render() {
      var list = matches();
      var pages = Math.max(1, Math.ceil(list.length / per));
      if (page > pages) { page = pages; }
      cards.forEach(function (c) { c.style.display = 'none'; });
      list.slice((page - 1) * per, page * per).forEach(function (c) {
        c.style.display = '';
        c.classList.add('in');
      });
      controls.innerHTML = '';
      if (pages < 2) { return; }
      button('‹', page - 1, page === 1, false);
      for (var i = 1; i <= pages; i++) { button(String(i), i, false, i === page); }
      button('›', page + 1, page === pages, false);
    }

    filters.forEach(function (f) {
      f.addEventListener('click', function () {
        filters.forEach(function (o) { o.classList.remove('active'); });
        f.classList.add('active');
        cat = f.getAttribute('data-cat');
        page = 1;
        render();
      });
    });
    render();
  });
})();
