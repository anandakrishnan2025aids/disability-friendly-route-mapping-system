import os

os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

style = open('static/css/style.css', 'w', encoding='utf-8')
style.write("""@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--bg:#060b18;--surface:#111827;--surface2:#1a2235;--surface3:#212d42;--border:rgba(255,255,255,0.07);--border-hi:rgba(255,255,255,0.14);--text:#e8eeff;--text-muted:#7a8aaa;--text-dim:#3d4f6e;--accent:#10e8b8;--accent-dim:rgba(16,232,184,0.10);--accent-glow:rgba(16,232,184,0.28);--accent2:#ff5c7a;--blue:#5b9dff;--blue-dim:rgba(91,157,255,0.10);--grad:linear-gradient(135deg,#10e8b8,#5b9dff);--shadow:0 4px 24px rgba(0,0,0,0.5);--glow:0 0 40px rgba(16,232,184,0.14);--r:12px;--r-lg:18px;--r-xl:26px;--hd:'Space Grotesk',sans-serif;--bd:'Plus Jakarta Sans',sans-serif;}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:var(--bd);font-size:16px;line-height:1.6;min-height:100vh;display:flex;flex-direction:column;overflow-x:hidden;}
body::after{content:'';position:fixed;inset:0;background-image:radial-gradient(rgba(255,255,255,0.03) 1px,transparent 1px);background-size:28px 28px;pointer-events:none;z-index:0;}
main{flex:1;position:relative;z-index:1}
a{color:var(--accent);text-decoration:none}
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:var(--surface3);border-radius:3px}
.navbar{position:sticky;top:0;z-index:1000;background:rgba(6,11,24,0.88);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;padding:0 2.5rem;height:66px;}
.nav-brand{display:flex;align-items:center;gap:.65rem;text-decoration:none}
.brand-icon{width:36px;height:36px;background:var(--grad);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;box-shadow:0 0 22px var(--accent-glow);flex-shrink:0;}
.brand-text{font-family:var(--hd);font-size:1.2rem;font-weight:700;color:var(--text);letter-spacing:-.02em}
.brand-text strong{color:var(--accent)}
.nav-links{display:flex;gap:.2rem;align-items:center}
.nav-link{font-size:.875rem;font-weight:500;color:var(--text-muted);padding:.48rem 1rem;border-radius:8px;transition:all .18s;text-decoration:none;}
.nav-link:hover{background:var(--surface2);color:var(--text)}
.nav-link.active{background:var(--accent-dim);color:var(--accent);}
.nav-toggle{display:none;background:none;border:none;color:var(--text);font-size:1.4rem;cursor:pointer;padding:.3rem}
.mobile-menu{display:none;flex-direction:column;background:var(--surface);border-bottom:1px solid var(--border)}
.mobile-menu.open{display:flex}
.mobile-link{padding:.9rem 2rem;color:var(--text-muted);font-weight:500;border-bottom:1px solid var(--border);}
.mobile-link:hover{background:var(--surface2);color:var(--text)}
.btn{display:inline-flex;align-items:center;gap:.5rem;font-family:var(--bd);font-size:.9rem;font-weight:700;padding:.75rem 1.6rem;border-radius:10px;border:none;cursor:pointer;transition:all .2s;text-decoration:none;line-height:1;}
.btn-primary{background:var(--grad);color:#060b18;box-shadow:0 4px 20px var(--accent-glow);}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 32px var(--accent-glow);color:#060b18}
.btn-outline{background:transparent;border:1px solid var(--border-hi);color:var(--text);}
.btn-outline:hover{border-color:var(--accent);color:var(--accent);background:var(--accent-dim)}
.btn-lg{padding:1rem 2.2rem;font-size:1rem;border-radius:12px}
.hero{position:relative;min-height:calc(100vh - 66px);display:flex;align-items:center;overflow:hidden;}
.hero-orb{position:absolute;border-radius:50%;filter:blur(90px);pointer-events:none}
.orb-1{width:680px;height:680px;background:radial-gradient(circle,rgba(16,232,184,.1),transparent 70%);top:-220px;right:-160px;animation:orbf 10s ease-in-out infinite;}
.orb-2{width:480px;height:480px;background:radial-gradient(circle,rgba(91,157,255,.09),transparent 70%);bottom:-140px;left:-120px;animation:orbf 13s ease-in-out infinite reverse;}
@keyframes orbf{0%,100%{transform:translate(0,0)}50%{transform:translate(28px,-28px)}}
.hero-inner{max-width:1200px;margin:0 auto;padding:6rem 2.5rem;display:grid;grid-template-columns:1.15fr .85fr;gap:5rem;align-items:center;width:100%;position:relative;z-index:1;}
.hero-badge{display:inline-flex;align-items:center;gap:.5rem;background:var(--accent-dim);border:1px solid rgba(16,232,184,.22);color:var(--accent);font-size:.72rem;font-weight:700;padding:.38rem 1rem;border-radius:50px;margin-bottom:1.75rem;letter-spacing:.09em;text-transform:uppercase;}
.badge-dot{width:6px;height:6px;background:var(--accent);border-radius:50%;animation:blink 2s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}
.hero-title{font-family:var(--hd);font-size:clamp(2.8rem,5.5vw,4.8rem);font-weight:700;line-height:1.0;letter-spacing:-.04em;color:var(--text);margin-bottom:1.5rem;}
.gradient-text{background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:1.05rem;color:var(--text-muted);line-height:1.8;max-width:490px;margin-bottom:2.5rem;}
.hero-actions{display:flex;gap:1rem;flex-wrap:wrap;}
.hero-stats{display:flex;flex-direction:column;gap:1rem;}
.stat-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg);padding:1.4rem 1.75rem;position:relative;overflow:hidden;transition:all .3s;}
.stat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--grad);transform:scaleX(0);transform-origin:left;transition:transform .3s;}
.stat-card:hover{border-color:var(--border-hi);transform:translateX(6px);box-shadow:var(--glow)}
.stat-card:hover::before{transform:scaleX(1)}
.stat-card-inner{display:flex;align-items:center;gap:1.2rem}
.stat-icon{width:48px;height:48px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:1.35rem;flex-shrink:0;border:1px solid var(--border);}
.icon-green{background:var(--accent-dim)}.icon-blue{background:var(--blue-dim)}.icon-orange{background:rgba(255,92,122,0.10)}
.stat-label{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:var(--text-muted);margin-bottom:.18rem}
.stat-value{font-family:var(--hd);font-size:2rem;font-weight:700;color:var(--text);line-height:1}
.stat-value span{color:var(--accent)}
.stat-sub{font-size:.76rem;color:var(--text-dim);margin-top:.12rem}
.stats-banner{background:var(--surface);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:3rem 2.5rem;position:relative;z-index:1;}
.stats-banner-inner{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:2rem;text-align:center;}
.banner-stat-num{font-family:var(--hd);font-size:3rem;font-weight:700;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1;margin-bottom:.4rem;}
.banner-stat-label{font-size:.82rem;color:var(--text-muted);font-weight:500}
.features{max-width:1200px;margin:0 auto;padding:6rem 2.5rem;position:relative;z-index:1}
.section-eyebrow{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.14em;color:var(--accent);margin-bottom:1rem;display:flex;align-items:center;gap:.5rem;}
.section-eyebrow::before{content:'';width:22px;height:2px;background:var(--accent);border-radius:1px}
.section-title{font-family:var(--hd);font-size:clamp(2rem,4vw,3rem);font-weight:700;letter-spacing:-.03em;line-height:1.1;margin-bottom:1rem;color:var(--text);}
.section-title span{color:var(--accent)}
.section-sub{color:var(--text-muted);font-size:1rem;max-width:480px;margin-bottom:3.5rem;line-height:1.75}
.features-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}
.feature-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg);padding:2rem;transition:all .28s;position:relative;overflow:hidden;}
.feature-card:hover{border-color:rgba(16,232,184,.28);transform:translateY(-5px);box-shadow:var(--glow)}
.feature-icon-wrap{width:50px;height:50px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;margin-bottom:1.2rem;background:var(--surface2);border:1px solid var(--border);transition:all .28s;}
.feature-card:hover .feature-icon-wrap{background:var(--accent-dim);border-color:rgba(16,232,184,.28);}
.feature-card h3{font-family:var(--hd);font-size:1rem;font-weight:600;margin-bottom:.55rem;color:var(--text)}
.feature-card p{color:var(--text-muted);font-size:.88rem;line-height:1.7}
.cta-section{max-width:1200px;margin:0 auto;padding:0 2.5rem 6rem;position:relative;z-index:1}
.cta-inner{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-xl);padding:5rem 3rem;text-align:center;position:relative;overflow:hidden;}
.cta-inner h2{font-family:var(--hd);font-size:clamp(1.8rem,3vw,2.6rem);font-weight:700;letter-spacing:-.03em;margin-bottom:1rem;}
.cta-inner p{color:var(--text-muted);font-size:1rem;margin-bottom:2rem;}
.about-page{max-width:1100px;margin:0 auto;padding:4rem 2.5rem 6rem;position:relative;z-index:1}
.about-hero{text-align:center;padding:3rem 0 4rem}
.about-hero h1{font-family:var(--hd);font-size:clamp(2.5rem,5vw,4rem);font-weight:700;letter-spacing:-.04em;margin-bottom:1.25rem;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.about-sub{font-size:1.1rem;color:var(--text-muted);max-width:560px;margin:0 auto;line-height:1.75}
.about-mission{display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start;margin-bottom:5rem}
.mission-text h2{font-family:var(--hd);font-size:2rem;font-weight:700;margin-bottom:1.25rem;letter-spacing:-.02em}
.mission-text p{color:var(--text-muted);margin-bottom:1rem;line-height:1.8}
.mission-stats{display:flex;flex-direction:column;gap:1rem}
.stat-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:1.5rem 1.75rem;transition:all .2s;}
.stat-box:hover{border-color:rgba(16,232,184,.28);box-shadow:var(--glow)}
.stat-box span{font-family:var(--hd);font-size:2.5rem;font-weight:700;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;display:block;line-height:1;margin-bottom:.3rem;}
.stat-box label{font-size:.78rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.07em}
.how-it-works{margin-bottom:5rem}
.how-it-works h2{font-family:var(--hd);font-size:2rem;font-weight:700;margin-bottom:2rem;letter-spacing:-.02em}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.25rem}
.step-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg);padding:2rem;transition:all .2s}
.step-box:hover{border-color:rgba(16,232,184,.28);transform:translateY(-3px)}
.step-num{font-family:var(--hd);font-size:3rem;font-weight:700;line-height:1;margin-bottom:1rem;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.step-box h3{font-family:var(--hd);font-weight:600;margin-bottom:.5rem}
.step-box p{color:var(--text-muted);font-size:.88rem;line-height:1.7}
.tech-section{margin-bottom:4rem}
.tech-section h2{font-family:var(--hd);font-size:2rem;font-weight:700;margin-bottom:1.5rem;letter-spacing:-.02em}
.tech-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem}
.tech-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:1.5rem;font-size:.88rem;color:var(--text-muted);line-height:1.65;transition:all .2s}
.tech-card:hover{border-color:rgba(16,232,184,.28)}
.tech-card strong{font-family:var(--hd);font-weight:700;color:var(--accent);display:block;margin-bottom:.4rem}
.contact-section{text-align:center;padding:3.5rem;background:var(--surface);border-radius:var(--r-xl);border:1px solid var(--border);}
.contact-section h2{font-family:var(--hd);font-size:1.8rem;font-weight:700;margin-bottom:.75rem;}
.contact-section p{color:var(--text-muted);margin-bottom:2rem;max-width:480px;margin-inline:auto;}
.loading-spinner{color:var(--text-muted);font-size:.875rem;padding:2rem;text-align:center;display:flex;align-items:center;justify-content:center;gap:.6rem}
.loading-spinner::before{content:'';width:16px;height:16px;border:2px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.footer{border-top:1px solid var(--border);padding:1.75rem 2.5rem;background:var(--surface);position:relative;z-index:1}
.footer-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;font-size:.83rem;color:var(--text-muted);flex-wrap:wrap;gap:.75rem}
.footer-links{display:flex;gap:1.5rem}
.footer-links a{color:var(--text-muted);transition:color .18s}
.footer-links a:hover{color:var(--accent)}
@keyframes fiu{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:1024px){.features-grid{grid-template-columns:repeat(2,1fr)}.stats-banner-inner{grid-template-columns:repeat(2,1fr)}}
@media(max-width:900px){.hero-inner{grid-template-columns:1fr;gap:3rem;text-align:center}.hero-actions{justify-content:center}.hero-sub{margin:0 auto 2.5rem}.about-mission{grid-template-columns:1fr}}
@media(max-width:640px){.navbar{padding:0 1.25rem}.nav-links{display:none}.nav-toggle{display:block}.features-grid{grid-template-columns:1fr}.hero-inner{padding:3rem 1.25rem}.features{padding:3rem 1.25rem}}""")
style.close()
print('style.css done!')

mapcss = open('static/css/map.css', 'w', encoding='utf-8')
mapcss.write(""".map-page{display:flex;height:calc(100vh - 66px);overflow:hidden;position:relative;z-index:1}
.map-sidebar{width:370px;min-width:270px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;}
.sidebar-header{padding:1.6rem 1.75rem 1rem;border-bottom:1px solid var(--border);background:var(--bg2)}
.sidebar-header h2{font-family:var(--hd);font-size:1.25rem;font-weight:700;letter-spacing:-.02em;margin-bottom:.25rem;color:var(--text)}
.sidebar-header p{font-size:.8rem;color:var(--text-muted)}
.filter-bar{display:flex;gap:.4rem;padding:1rem 1.75rem;border-bottom:1px solid var(--border);flex-wrap:wrap;background:var(--bg2)}
.filter-btn{font-size:.75rem;font-weight:600;padding:.38rem .9rem;border-radius:50px;border:1px solid var(--border);background:transparent;cursor:pointer;color:var(--text-muted);transition:all .18s;}
.filter-btn.active,.filter-btn:hover{background:var(--accent-dim);color:var(--accent);border-color:rgba(16,232,184,.28)}
.routes-list{flex:1;overflow-y:auto;padding:1.1rem}
.route-item{background:var(--bg2);border:1px solid var(--border);border-radius:var(--r);padding:1.1rem 1.2rem;margin-bottom:.75rem;cursor:pointer;transition:all .2s;position:relative;overflow:hidden;}
.route-item::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--grad);transform:scaleY(0);transform-origin:bottom;transition:transform .2s;}
.route-item:hover,.route-item.selected{border-color:rgba(16,232,184,.28);background:var(--surface2);box-shadow:var(--glow)}
.route-item:hover::before,.route-item.selected::before{transform:scaleY(1)}
.route-name{font-family:var(--hd);font-weight:600;font-size:.92rem;margin-bottom:.35rem;color:var(--text)}
.route-desc{font-size:.78rem;color:var(--text-muted);margin-bottom:.65rem;line-height:1.5}
.route-meta{display:flex;align-items:center;justify-content:space-between;margin-bottom:.55rem}
.route-distance{font-size:.76rem;font-weight:600;color:var(--text-muted)}
.score-badge{font-size:.7rem;font-weight:700;padding:.2rem .6rem;border-radius:50px;}
.score-high{background:rgba(16,232,184,.13);color:#10e8b8;border:1px solid rgba(16,232,184,.22)}
.score-med{background:rgba(255,195,90,.13);color:#ffc35a;border:1px solid rgba(255,195,90,.22)}
.score-low{background:rgba(255,92,122,.13);color:#ff5c7a;border:1px solid rgba(255,92,122,.22)}
.route-features{display:flex;flex-wrap:wrap;gap:.32rem}
.feature-tag{font-size:.68rem;padding:.16rem .52rem;background:var(--surface3);border:1px solid var(--border);border-radius:4px;color:var(--text-muted);}
.legend{padding:1.1rem 1.75rem;border-top:1px solid var(--border);background:var(--bg2)}
.legend-title{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--text-dim);margin-bottom:.7rem}
.legend-item{display:flex;align-items:center;gap:.55rem;font-size:.78rem;color:var(--text-muted);margin-bottom:.4rem}
.legend-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.route-dot{background:#10e8b8;border-radius:2px}.ramp-dot{background:#ff5c7a}.toilet-dot{background:#5b9dff}.bench-dot{background:#c084fc}.audio-dot{background:#ffc35a}.parking-dot{background:#22d3ee}.report-dot{background:#f87171}
.map-container{flex:1;position:relative}
#map{width:100%;height:100%}
.leaflet-container{background:#060b18 !important}
.leaflet-tile{filter:invert(1) hue-rotate(180deg) brightness(.82) saturate(.65)}
.leaflet-control-zoom{border:1px solid var(--border) !important}
.leaflet-control-zoom a{background:var(--surface) !important;color:var(--text) !important;border-color:var(--border) !important}
.leaflet-control-zoom a:hover{background:var(--surface2) !important;color:var(--accent) !important}
.leaflet-popup-content-wrapper{background:var(--surface) !important;border:1px solid var(--border) !important;color:var(--text) !important;border-radius:14px !important;}
.leaflet-popup-tip{background:var(--surface) !important}
.map-controls{position:absolute;bottom:2rem;right:1rem;display:flex;flex-direction:column;gap:.5rem;z-index:500}
.map-ctrl-btn{width:42px;height:42px;border-radius:10px;border:1px solid var(--border);background:var(--surface);cursor:pointer;font-size:1.1rem;display:flex;align-items:center;justify-content:center;transition:all .2s;color:var(--text-muted);}
.map-ctrl-btn:hover{background:var(--accent-dim);border-color:rgba(16,232,184,.28);color:var(--accent);}
.point-popup h4{font-family:var(--hd);font-weight:600;margin-bottom:.4rem;font-size:.92rem;color:var(--text)}
.status{font-size:.72rem;font-weight:700;padding:.16rem .55rem;border-radius:50px;}
.status-operational{background:rgba(16,232,184,.14);color:#10e8b8}
.status-maintenance{background:rgba(255,195,90,.14);color:#ffc35a}
@media(max-width:700px){.map-page{flex-direction:column;height:auto}.map-sidebar{width:100%}.map-container{height:58vh}.routes-list{max-height:250px}}""")
mapcss.close()
print('map.css done!')

reportcss = open('static/css/report.css', 'w', encoding='utf-8')
reportcss.write(""".report-page{max-width:1200px;margin:0 auto;padding:2rem 2.5rem 6rem;position:relative;z-index:1}
.report-hero{padding:3.5rem 0 2.5rem;border-bottom:1px solid var(--border);margin-bottom:3rem}
.report-hero h1{font-family:var(--hd);font-size:clamp(2rem,4vw,3rem);font-weight:700;letter-spacing:-.04em;margin-bottom:.75rem;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.report-hero p{color:var(--text-muted);font-size:1rem;max-width:540px;line-height:1.75}
.report-layout{display:grid;grid-template-columns:2fr 1fr;gap:2.5rem;align-items:start}
.form-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-xl);padding:2.5rem;box-shadow:var(--shadow)}
.form-steps{display:flex;align-items:center;margin-bottom:2.5rem}
.step{display:flex;align-items:center;gap:.5rem;font-size:.8rem;font-weight:600;color:var(--text-muted);white-space:nowrap}
.step span{width:27px;height:27px;border-radius:50%;background:var(--surface3);border:1px solid var(--border);display:inline-flex;align-items:center;justify-content:center;font-size:.76rem;font-weight:700;flex-shrink:0;color:var(--text-muted);transition:all .2s;}
.step.active{color:var(--accent)}.step.active span{background:var(--accent-dim);border-color:rgba(16,232,184,.38);color:var(--accent);}
.step.done span{background:var(--accent);border-color:var(--accent);color:#060b18}
.step-line{flex:1;height:1px;background:var(--border);margin:0 .6rem;min-width:16px}
.form-step h3{font-family:var(--hd);font-size:1.25rem;font-weight:700;margin-bottom:1.75rem;color:var(--text)}
.form-group{margin-bottom:1.5rem}
.form-group label{display:block;font-size:.76rem;font-weight:700;margin-bottom:.55rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:.06em}
.req{color:var(--accent2)}.optional{font-weight:400;color:var(--text-dim);text-transform:none;}
input[type="text"],textarea{width:100%;font-family:var(--bd);font-size:.92rem;padding:.8rem 1.1rem;border:1px solid var(--border);border-radius:10px;background:var(--bg2);color:var(--text);transition:all .2s;resize:vertical;outline:none;}
input[type="text"]::placeholder,textarea::placeholder{color:var(--text-dim)}
input[type="text"]:focus,textarea:focus{border-color:rgba(16,232,184,.45);background:var(--surface2);box-shadow:0 0 0 3px rgba(16,232,184,.07)}
.field-error{font-size:.76rem;color:var(--accent2);margin-top:.38rem;min-height:1em}
.issue-types{display:grid;grid-template-columns:repeat(3,1fr);gap:.55rem}
.issue-type-card{display:flex;flex-direction:column;align-items:center;gap:.45rem;padding:.95rem .55rem;border:1px solid var(--border);border-radius:var(--r);cursor:pointer;font-size:.76rem;font-weight:600;text-align:center;transition:all .18s;background:var(--bg2);color:var(--text-muted);}
.issue-type-card:hover{border-color:rgba(16,232,184,.28);background:var(--surface2);color:var(--text)}
.issue-type-card input[type="radio"]{display:none}
.issue-type-card span{font-size:1.45rem}
.issue-type-card:has(input:checked){border-color:rgba(16,232,184,.38);background:var(--accent-dim);color:var(--accent);}
.severity-options{display:flex;gap:.45rem;flex-wrap:wrap}
.severity-opt{display:flex;align-items:center;gap:.38rem;padding:.45rem 1.05rem;border:1px solid var(--border);border-radius:50px;cursor:pointer;font-size:.8rem;font-weight:600;transition:all .18s;background:var(--bg2);color:var(--text-muted);}
.severity-opt input{display:none}
.severity-opt.low:has(input:checked){background:rgba(16,232,184,.1);border-color:rgba(16,232,184,.3);color:#10e8b8}
.severity-opt.medium:has(input:checked){background:rgba(255,195,90,.1);border-color:rgba(255,195,90,.3);color:#ffc35a}
.severity-opt.high:has(input:checked){background:rgba(251,146,60,.1);border-color:rgba(251,146,60,.3);color:#fb923c}
.severity-opt.critical:has(input:checked){background:rgba(255,92,122,.1);border-color:rgba(255,92,122,.3);color:#ff5c7a}
#reportMap{height:270px;border-radius:10px;border:1px solid var(--border);margin-top:.5rem;overflow:hidden}
.map-hint{font-size:.76rem;color:var(--text-dim);margin-top:.38rem}
.coords-display{font-size:.76rem;color:var(--accent);margin-top:.38rem;min-height:1.2em;font-family:monospace}
.review-box{background:var(--bg2);border:1px solid var(--border);border-radius:var(--r);padding:1.5rem;margin-bottom:1.75rem}
.review-row{display:flex;gap:1rem;margin-bottom:.8rem;align-items:baseline}
.review-label{font-size:.7rem;font-weight:700;min-width:100px;color:var(--text-dim);text-transform:uppercase;letter-spacing:.06em}
.review-value{color:var(--text);flex:1;font-size:.88rem}
.step-actions{display:flex;gap:.75rem;margin-top:.75rem}
.hidden{display:none !important}
.btn-submit{min-width:160px;justify-content:center}
.success-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-xl);padding:4rem 3rem;text-align:center;}
.success-icon{font-size:4rem;margin-bottom:1.25rem}
.success-card h2{font-family:var(--hd);font-size:2rem;font-weight:700;margin-bottom:.75rem;}
.success-card p{color:var(--text-muted);max-width:400px;margin:0 auto 2.5rem;line-height:1.75}
.success-actions{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap}
.reports-panel h3{font-family:var(--hd);font-weight:700;font-size:1rem;margin-bottom:1.25rem;color:var(--text)}
.report-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:1.1rem 1.25rem;margin-bottom:.75rem;transition:all .2s;position:relative;overflow:hidden;}
.report-card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--grad);}
.report-card:hover{border-color:var(--border-hi);}
.report-card-title{font-weight:600;font-size:.86rem;margin-bottom:.45rem;color:var(--text);padding-left:.25rem}
.report-card-meta{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.38rem;padding-left:.25rem}
.report-type-badge{font-size:.68rem;font-weight:700;padding:.16rem .55rem;border-radius:50px;background:var(--accent-dim);color:var(--accent);}
.report-time{font-size:.7rem;color:var(--text-dim)}
.upvote-btn{font-size:.7rem;background:var(--surface2);border:1px solid var(--border);border-radius:50px;padding:.18rem .65rem;cursor:pointer;color:var(--text-muted);transition:all .18s;font-weight:600;}
.upvote-btn:hover{background:var(--accent-dim);color:var(--accent)}
.no-reports{color:var(--text-muted);font-size:.88rem;font-style:italic;text-align:center;padding:2rem 0}
@media(max-width:900px){.report-layout{grid-template-columns:1fr}.issue-types{grid-template-columns:repeat(2,1fr)}}""")
reportcss.close()
print('report.css done!')

with open('static/js/main.js', 'w', encoding='utf-8') as f:
    f.write("function toggleMenu(){const m=document.getElementById('mobileMenu');if(m)m.classList.toggle('open');}")
print('main.js done!')

print('\nAll CSS files written successfully!')
print('Now run: python app.py')