const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { runInNewContext } = require('node:vm');
const app = readFileSync(require('node:path').join(__dirname, '../assets/app.js'), 'utf8');
const scrollKey = 'physical-ai-sidebar:/guide';

// Run the actual page script across independent page loads. Geometry represents
// a long course menu; no document scrolling API is supplied to the script.
function page({ storage = new Map(), activeTop = 950, mobile = false, blocked = false } = {}) {
  function element() {
    const listeners = new Map();
    const classes = new Set();
    return {
      addEventListener(name, fn) { listeners.set(name, fn); },
      fire(name, event = {}) { listeners.get(name)?.(event); },
      setAttribute() {}, contains() { return false; },
      classList: {
        remove(name) { classes.delete(name); },
        toggle(name) { if (classes.has(name)) { classes.delete(name); return false; } classes.add(name); return true; },
        contains(name) { return classes.has(name); }
      }
    };
  }
  const sidebar = element(), menu = element(), nav = element(), window = element();
  let scroll = 0;
  Object.defineProperties(nav, {
    clientHeight: { get: () => mobile && !sidebar.classList.contains('is-open') ? 0 : 400 },
    scrollTop: { get: () => scroll, set: value => { scroll = Math.max(0, Math.min(1600, value)); } }
  });
  nav.getBoundingClientRect = () => ({ top: 200, bottom: 600 });
  const active = activeTop === null ? null : {
    getBoundingClientRect: () => ({ top: 200 + activeTop - scroll, bottom: 240 + activeTop - scroll })
  };
  nav.querySelector = () => active;
  const selectors = new Map([
    ['.sidebar', sidebar], ['.menu-toggle', menu], ['.lesson-links', nav],
    ...['#search-dialog', '#search-input', '.search-results', '.search-status', '.search-trigger', '.search-close'].map(name => [name, element()])
  ]);
  const document = Object.assign(element(), {
    body: { dataset: { base: '/guide' } },
    querySelector: name => selectors.get(name) || null,
    querySelectorAll: () => []
  });
  runInNewContext(app, {
    document, window,
    localStorage: { getItem: () => null },
    sessionStorage: {
      getItem(key) { if (blocked) throw Error('Storage blocked'); return storage.get(key) ?? null; },
      setItem(key, value) { if (blocked) throw Error('Storage blocked'); storage.set(key, value); }
    }
  });
  return { nav, menu, window, storage, active };
}

test('clicking an adjacent lesson preserves the sidebar position across page loads and refresh', () => {
  const first = page({ activeTop: 950 });
  first.nav.scrollTop = 800;
  first.nav.fire('click');
  const next = page({ storage: first.storage, activeTop: 1000 });
  assert.equal(next.nav.scrollTop, 800);
  const refreshed = page({ storage: next.storage, activeTop: 1000 });
  assert.equal(refreshed.nav.scrollTop, 800);
});

test('direct links and next/previous navigation bring an offscreen active lesson into view', () => {
  const direct = page({ activeTop: 1400 });
  assert.equal(direct.active.getBoundingClientRect().bottom, 600);
  const previous = page({ storage: direct.storage, activeTop: 300 });
  assert.equal(previous.active.getBoundingClientRect().top, 200);
});

test('back/forward restoration keeps the active lesson visible after another page scrolls the menu', () => {
  const current = page({ activeTop: 1000 });
  current.storage.set(scrollKey, '100');
  current.window.fire('pageshow');
  assert.equal(current.active.getBoundingClientRect().bottom, 600);
});

test('the mobile menu restores position only once it is visible', () => {
  const storage = new Map([[scrollKey, '800']]);
  const current = page({ storage, mobile: true, activeTop: 1000 });
  current.window.fire('pagehide');
  assert.equal(storage.get(scrollKey), '800');
  current.menu.fire('click');
  assert.equal(current.nav.scrollTop, 800);
  assert.ok(current.active.getBoundingClientRect().bottom <= 600);
});

test('active lessons remain visible when browser storage is blocked or malformed', () => {
  for (const options of [{ blocked: true }, { storage: new Map([[scrollKey, 'invalid']]) }]) {
    const current = page({ ...options, activeTop: 1400 });
    assert.equal(current.active.getBoundingClientRect().bottom, 600);
  }
});

test('supporting pages preserve the reader’s manual sidebar scroll without an active lesson', () => {
  const current = page({ activeTop: null });
  current.nav.scrollTop = 900;
  current.nav.fire('scroll');
  const next = page({ storage: current.storage, activeTop: null });
  assert.equal(next.nav.scrollTop, 900);
});
