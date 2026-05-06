from pathlib import Path
root = Path('.')
style = '''<style>
:root {
  color-scheme: dark;
  --bg: #050618;
  --panel: rgba(12, 18, 42, 0.92);
  --panel-soft: rgba(24, 32, 70, 0.88);
  --panel-strong: rgba(10, 14, 30, 0.98);
  --accent: #9b5cff;
  --accent-soft: rgba(155, 92, 255, 0.22);
  --text: #eef2ff;
  --muted: #a9b4ff;
  --border: rgba(255, 255, 255, 0.08);
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html {
  scroll-behavior: smooth;
}
body {
  min-height: 100vh;
  background: radial-gradient(circle at 20% 15%, rgba(155, 92, 255, 0.14), transparent 18%),
              radial-gradient(circle at 80% 10%, rgba(81, 141, 255, 0.12), transparent 18%),
              linear-gradient(180deg, #03050d 0%, #050717 45%, #090f22 100%);
  color: var(--text);
  font-family: Inter, "Segoe UI", Arial, sans-serif;
  overflow-x: hidden;
  position: relative;
}
body::before {
  content: "";
  position: fixed;
  inset: 0;
  background-image: linear-gradient(180deg, rgba(255,255,255,0.04) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 80px 80px;
  opacity: 0.24;
  pointer-events: none;
  z-index: 0;
}
.topbar {
  position: fixed;
  left: 1.5rem;
  right: 1.5rem;
  top: 1.2rem;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border-radius: 26px;
  background: rgba(8, 12, 29, 0.9);
  border: 1px solid var(--border);
  box-shadow: 0 26px 90px rgba(0, 0, 0, 0.24);
  backdrop-filter: blur(16px);
}
.brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.brand-icon {
  width: 54px;
  height: 54px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(255, 102, 196, 0.96), rgba(155, 92, 255, 0.96));
  box-shadow: 0 0 28px rgba(255, 102, 196, 0.2);
  display: grid;
  place-items: center;
  color: #fff;
  font-size: 1.3rem;
}
.brand-info h1 {
  font-size: 1rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  line-height: 1.1;
  color: var(--text);
}
.brand-info p {
  font-size: 0.8rem;
  color: var(--muted);
  max-width: 36ch;
}
.status-line {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}
.status-chip {
  padding: 0.65rem 0.9rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e8ecff;
  font-size: 0.8rem;
  letter-spacing: 0.03em;
}
main.page-shell {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  padding: 7rem 1.5rem 4rem;
}
.page-card {
  width: 100%;
  max-width: 1400px;
  background: rgba(11, 16, 37, 0.94);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 32px;
  box-shadow: 0 26px 90px rgba(0, 0, 0, 0.24);
  padding: 2rem;
  overflow: hidden;
}
.page-card h1,
.page-card h2 {
  color: #eef2ff;
  margin-bottom: 1rem;
}
.page-card h1 {
  font-size: clamp(2rem, 2.5vw, 3rem);
}
.page-card p,
.page-card li,
.page-card td,
.page-card th {
  color: var(--muted);
}
.page-card a {
  color: var(--accent);
}
.page-card .panel {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 1.25rem;
  margin-bottom: 1.25rem;
}
.page-grid {
  display: grid;
  gap: 1.25rem;
}
.page-grid.columns-2 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
.page-grid.columns-3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}
.stats-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}
.stat-card {
  padding: 1rem;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.stat-card strong {
  display: block;
  font-size: 1.7rem;
  margin-bottom: 0.45rem;
  color: #fff;
}
.btn {
  display: inline-flex;
  gap: 0.5rem;
  align-items: center;
  padding: 0.9rem 1.2rem;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(155, 92, 255, 0.14);
  color: #eef2ff;
  text-decoration: none;
  font-weight: 700;
  transition: transform 0.2s ease, background 0.2s ease;
}
.btn:hover {
  transform: translateY(-1px);
  background: rgba(155, 92, 255, 0.2);
}
.user-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}
.user-card {
  padding: 1.25rem;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.user-card h3 {
  margin-bottom: 0.75rem;
  color: #fff;
}
.user-card p {
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}
section.panel + section.panel {
  margin-top: 1rem;
}
footer {
  margin-top: 2rem;
  padding: 1.25rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  text-align: center;
  color: var(--muted);
}
footer a {
  color: var(--accent);
  text-decoration: none;
}
.hint-strip {
  position: fixed;
  left: 50%;
  bottom: 1.4rem;
  transform: translateX(-1.5%);
  z-index: 11;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
  padding: 1rem 1.2rem;
  border-radius: 999px;
  background: rgba(10, 14, 28, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.24);
  color: #c9d3ff;
  font-size: 0.84rem;
}
.hint-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.55rem 0.8rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.hint-chip span {
  display: inline-flex;
  width: 30px;
  height: 30px;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  font-size: 0.88rem;
  letter-spacing: 0.05em;
}
.back-to-top {
  position: fixed;
  right: 24px;
  bottom: 90px;
  width: 48px;
  height: 48px;
  border: 2px solid rgba(255,255,255,0.15);
  border-radius: 50%;
  background: rgba(155, 92, 255, 0.18);
  color: #fff;
  display: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 12;
}
.back-to-top.show {
  display: flex;
}
@media (max-width: 980px) {
  .page-grid.columns-2 { grid-template-columns: 1fr; }
  .page-grid.columns-3 { grid-template-columns: 1fr; }
}
@media (max-width: 860px) {
  .topbar { flex-direction: column; align-items: flex-start; }
  .hint-strip { width: calc(100% - 3rem); }
}
</style>'''
header = '''<header class="topbar" aria-label="Site header">
  <div class="brand">
    <div class="brand-icon">CD</div>
    <div class="brand-info">
      <h1>CDKK XMB Lounge</h1>
      <p>PS3-inspired interface for the CDKK site.</p>
    </div>
  </div>
  <div class="status-line" aria-label="System status">
    <span class="status-chip">Online</span>
    <span class="status-chip">PSN Connected</span>
    <span class="status-chip" id="clock">--/-- --:--:--</span>
  </div>
</header>'''
hint = '''<div class="hint-strip" aria-hidden="true">
  <div class="hint-chip"><span>X</span>Select</div>
  <div class="hint-chip"><span>O</span>Back</div>
  <div class="hint-chip"><span>? ?</span>Navigate</div>
</div>'''
script = '''<script>
const clock = document.getElementById('clock');
const updateClock = () => {
  if (!clock) return;
  const now = new Date();
  const date = String(now.getDate()).padStart(2, '0');
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  clock.textContent = f"{date}/{month} {hours}:{minutes}:{seconds}";
};
updateClock();
setInterval(updateClock, 1000);
const backToTop = document.querySelector('.back-to-top');
if (backToTop) {
  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 260) backToTop.classList.add('show');
    else backToTop.classList.remove('show');
  });
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}
</script>'''

pages = {
  'about.html': '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>About - CDKK Network</title>
  <link rel="icon" type="image/x-icon" href="Assets/Favicon/favicon.ico" />
  <meta name="theme-color" content="#24144d" />
  ''' + style + '''
</head>
<body>
''' + header + '''
<main class="page-shell" id="main">
  <article class="page-card">
    <h1>About CDKK Network</h1>
    <div class="page-grid columns-2">
      <section class="panel">
        <h2>?? Security & Site Policy</h2>
        <p>This site implements basic security measures including Content Security Policy, frame protection, and XSS prevention. Browse the CDKK network with confidence, but always scan downloads and verify sources.</p>
        <p>Files are shared by community members and are not hosted by the site itself. Use the network responsibly and report suspicious content.</p>
      </section>
      <section class="panel">
        <h2>?? Who We Are</h2>
        <p>CDKK is a community-driven network built around retro downloads, user profiles, forum activity, and creative sharing. Since 2004, the site has embraced old-school web culture with modern styling.</p>
        <p>Whether you are looking for downloads, forum discussions, or profile features, this interface brings the XMB aesthetic to every page.</p>
      </section>
    </div>
    <footer>
      © 2004 CDKK Network · <a href="index.html">Home</a> · <a href="downloads.html">Downloads</a> · <a href="forum.html">Forum</a>
    </footer>
  </article>
</main>
''' + hint + '''
''' + script + '''
</body>
</html>''',
  'downloads.html': '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Downloads - CDKK Network</title>
  <link rel="icon" type="image/x-icon" href="Assets/Favicon/favicon.ico" />
  <meta name="theme-color" content="#24144d" />
  ''' + style + '''
</head>
<body>
''' + header + '''
<main class="page-shell" id="main">
  <article class="page-card">
    <h1>Downloads</h1>
    <div class="stats-grid">
      <div class="stat-card"><strong>342</strong>Available Files</div>
      <div class="stat-card"><strong>99%</strong>Safe Scan Rate</div>
      <div class="stat-card"><strong>4.8?</strong>Community Rating</div>
    </div>
    <section class="panel">
      <h2>Featured Collections</h2>
      <div class="page-grid columns-3">
        <article class="user-card">
          <h3>Theme Packs</h3>
          <p>Retro XMB wallpapers, icons, and skins for classic desktop setups.</p>
        </article>
        <article class="user-card">
          <h3>Mods & Tools</h3>
          <p>Utilities for system tweaks, converters, and community-created enhancements.</p>
        </article>
        <article class="user-card">
          <h3>Archives</h3>
          <p>Vintage files, downloads, and collections preserved from the early web era.</p>
        </article>
      </div>
    </section>
    <section class="panel">
      <h2>Popular Downloads</h2>
      <div class="page-grid columns-2">
        <article class="user-card">
          <h3>Retro Skin Pack v3</h3>
          <p>Complete PS3/XMB-inspired visual overhaul for your site.</p>
          <p>Category: Themes · Rating: ?????</p>
        </article>
        <article class="user-card">
          <h3>CDKK Member Icon Set</h3>
          <p>Custom avatar and badge icons created by the community.</p>
          <p>Category: Graphics · Rating: ?????</p>
        </article>
        <article class="user-card">
          <h3>Wallpaper Collection</h3>
          <p>High-resolution backgrounds with neon and night city styles.</p>
          <p>Category: Wallpapers · Rating: ?????</p>
        </article>
        <article class="user-card">
          <h3>Download Launcher</h3>
          <p>Batch download helper for archived content and media packs.</p>
          <p>Category: Utilities · Rating: ?????</p>
        </article>
      </div>
    </section>
    <footer>
      © 2004 CDKK Network · <a href="index.html">Home</a> · <a href="about.html">About</a> · <a href="forum.html">Forum</a>
    </footer>
  </article>
</main>
''' + hint + '''
''' + script + '''
</body>
</html>''',
  'forum.html': '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Forum - CDKK Network</title>
  <link rel="icon" type="image/x-icon" href="Assets/Favicon/favicon.ico" />
  <meta name="theme-color" content="#24144d" />
  ''' + style + '''
</head>
<body>
''' + header + '''
<main class="page-shell" id="main">
  <article class="page-card">
    <h1>Forum</h1>
    <section class="panel">
      <h2>Community Boards</h2>
      <p>Classic discussions with modern XMB-inspired navigation and polished UI.</p>
      <div class="page-grid columns-2">
        <article class="user-card">
          <h3>General Discussion</h3>
          <p>News, introductions, and off-topic chat from the CDKK community.</p>
        </article>
        <article class="user-card">
          <h3>Downloads & Releases</h3>
          <p>Announcements, upload threads, and mirrored content for members.</p>
        </article>
      </div>
    </section>
    <section class="stats-grid">
      <div class="stat-card"><strong>1,874</strong>Members</div>
      <div class="stat-card"><strong>6,552</strong>Threads</div>
      <div class="stat-card"><strong>54,113</strong>Posts</div>
      <div class="stat-card"><strong>1,420</strong>Online</div>
    </section>
    <section class="panel">
      <h2>Latest Threads</h2>
      <ul>
        <li>[Guide] How to style profile signatures (2006 look)</li>
        <li>[Release] Neon icon pack v2.3 now available</li>
        <li>[Help] Instagram embeds not loading on mobile</li>
        <li>[Poll] Best CDKK theme color set?</li>
      </ul>
    </section>
    <footer>
      © 2004 CDKK Network · <a href="index.html">Home</a> · <a href="downloads.html">Downloads</a> · <a href="about.html">About</a>
    </footer>
  </article>
</main>
''' + hint + '''
''' + script + '''
</body>
</html>''',
  'profile.html': '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Profile - CDKK Network</title>
  <link rel="icon" type="image/x-icon" href="Assets/Favicon/favicon.ico" />
  <meta name="theme-color" content="#24144d" />
  ''' + style + '''
</head>
<body>
''' + header + '''
<main class="page-shell" id="main">
  <article class="page-card">
    <h1>User Profile</h1>
    <section class="panel">
      <div class="page-grid columns-2">
        <div>
          <h2>RetroCat_2004</h2>
          <p>Power Uploader • Berlin</p>
          <p>“Keeping the 2000s internet alive, one upload at a time.”</p>
        </div>
        <div class="stats-grid">
          <div class="stat-card"><strong>1,284</strong> Posts</div>
          <div class="stat-card"><strong>356</strong> Uploads</div>
          <div class="stat-card"><strong>4.9?</strong> Rating</div>
          <div class="stat-card"><strong>8,940</strong> Downloads</div>
        </div>
      </div>
    </section>
    <section class="page-grid columns-2">
      <article class="user-card">
        <h3>Recent Activity</h3>
        <ul>
          <li>Uploaded Retro Skin Pack v3</li>
          <li>Replied in “Best 2000s themes?”</li>
          <li>Favorited Electronic Beats Collection</li>
          <li>Downloaded 4K Wallpaper Bundle</li>
        </ul>
      </article>
      <article class="user-card">
        <h3>Badges</h3>
        <p>?? Top Contributor</p>
        <p>?? 300+ Uploads</p>
        <p>?? Forum Veteran</p>
        <p>?? Trending Creator</p>
      </article>
    </section>
    <footer>
      © 2004 CDKK Network · <a href="index.html">Home</a> · <a href="downloads.html">Downloads</a> · <a href="forum.html">Forum</a>
    </footer>
  </article>
</main>
<button class="back-to-top" title="Back to top">??</button>
''' + hint + '''
''' + script + '''
</body>
</html>''',
  'users.html': '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Users - CDKK Network</title>
  <link rel="icon" type="image/x-icon" href="Assets/Favicon/favicon.ico" />
  <meta name="theme-color" content="#24144d" />
  ''' + style + '''
</head>
<body>
''' + header + '''
<main class="page-shell" id="main">
  <article class="page-card">
    <h1>Users</h1>
    <section class="panel">
      <h2>Top Community Members</h2>
      <div class="user-grid">
        <article class="user-card"><h3>RetroCat_2004</h3><p>Power Uploader • Online</p><p>Active since 2004</p></article>
        <article class="user-card"><h3>FileWizard</h3><p>Release Manager • Online</p><p>Known for fast uploads</p></article>
        <article class="user-card"><h3>PixelRider</h3><p>Graphics Creator • Away</p><p>Theme and icon sets</p></article>
        <article class="user-card"><h3>Admin</h3><p>Moderator • Online</p><p>Support and site updates</p></article>
      </div>
    </section>
    <section class="stats-grid">
      <div class="stat-card"><strong>4,912</strong> Members</div>
      <div class="stat-card"><strong>1,420</strong> Online</div>
      <div class="stat-card"><strong>24</strong> New Today</div>
      <div class="stat-card"><strong>512</strong> Active Threads</div>
    </section>
    <footer>
      © 2004 CDKK Network · <a href="index.html">Home</a> · <a href="downloads.html">Downloads</a> · <a href="forum.html">Forum</a>
    </footer>
  </article>
</main>
<button class="back-to-top" title="Back to top">??</button>
''' + hint + '''
''' + script + '''
</body>
</html>''',
}
for filename, content in pages.items():
    path = root / filename
    path.write_text(content, encoding='utf-8')
    print(f'Wrote {filename}')
