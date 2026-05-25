# -*- coding: utf-8 -*-
"""
AtomStack 海外客服 SOP 网站生成器
将 sheet_data.json 中的所有数据渲染为单文件 HTML 网站
"""
import json, os, re

def esc(s):
    """HTML 转义"""
    if not s:
        return ''
    return (str(s)
        .replace('&','&amp;')
        .replace('<','&lt;')
        .replace('>','&gt;')
        .replace('"','&quot;')
        .replace("'",'&#39;'))

def nl2br(s):
    """换行转 <br> + HTML 转义"""
    return esc(s).replace('\n','<br>')

# ── 读取数据 ──────────────────────────────────────────────────────────
with open('sheet_data.json', encoding='utf-8') as f:
    DATA = json.load(f)

OUT = 'sop_website.html'
parts = []   # 所有 HTML 片段，最后一次性写入

# ═══════════════════════════════════════════════════════════════════════
# 1. HEAD + CSS
# ═══════════════════════════════════════════════════════════════════════
parts.append('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AtomStack 海外客服 SOP 帮助中心</title>
<style>
:root{
  --bg:#0d1117;--bg2:#161b22;--bg3:#21262d;--bg4:#30363d;
  --border:#30363d;--text:#e6edf3;--muted:#8b949e;
  --blue:#58a6ff;--green:#3fb950;--orange:#d29922;--red:#f85149;
  --purple:#bc8cff;--cyan:#39d353;--yellow:#e3b341;
  --grad1:linear-gradient(135deg,#1f6feb,#388bfd);
  --grad2:linear-gradient(135deg,#238636,#2ea043);
  --grad3:linear-gradient(135deg,#6e40c9,#8957e5);
  --grad4:linear-gradient(135deg,#b08800,#e3b341);
  --grad5:linear-gradient(135deg,#cf222e,#f85149);
  --shadow:0 8px 24px rgba(0,0,0,.6);
  --radius:12px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:"Segoe UI",system-ui,sans-serif;min-height:100vh;overflow-x:hidden}

/* ─── scrollbar ─── */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--bg2)}
::-webkit-scrollbar-thumb{background:var(--bg4);border-radius:3px}

/* ─── header ─── */
header{background:var(--bg2);border-bottom:1px solid var(--border);padding:16px 32px;display:flex;align-items:center;gap:16px;position:sticky;top:0;z-index:100;backdrop-filter:blur(8px)}
.logo{font-size:22px;font-weight:700;background:var(--grad1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;white-space:nowrap}
.tagline{color:var(--muted);font-size:13px}
.lang-btn{margin-left:auto;display:flex;gap:8px}
.lang-btn button{background:var(--bg3);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:20px;cursor:pointer;font-size:13px;transition:.2s}
.lang-btn button:hover,.lang-btn button.active{background:var(--blue);color:#fff;border-color:var(--blue)}

/* ─── hero ─── */
.hero{padding:48px 32px 32px;text-align:center}
.hero h1{font-size:32px;font-weight:800;background:var(--grad1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px}
.hero p{color:var(--muted);font-size:15px;max-width:600px;margin:0 auto}

/* ─── main layout ─── */
.main{max-width:1400px;margin:0 auto;padding:0 24px 80px}

/* ─── section title ─── */
.sec-title{font-size:20px;font-weight:700;margin:40px 0 20px;padding-bottom:10px;border-bottom:2px solid var(--border);display:flex;align-items:center;gap:10px}

/* ─── flow grid (main process nodes) ─── */
.flow-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px;margin-bottom:32px}
.flow-card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;cursor:pointer;transition:.25s;text-align:center;position:relative;overflow:hidden}
.flow-card::before{content:'';position:absolute;inset:0;opacity:0;transition:.25s}
.flow-card:hover::before,.flow-card.active::before{opacity:1}
.flow-card.c1::before{background:var(--grad1)}
.flow-card.c2::before{background:var(--grad2)}
.flow-card.c3::before{background:var(--grad3)}
.flow-card.c4::before{background:var(--grad4)}
.flow-card.c5::before{background:var(--grad5)}
.flow-card.c6::before{background:linear-gradient(135deg,#0d419d,#388bfd)}
.flow-card.c7::before{background:linear-gradient(135deg,#145a32,#1e8449)}
.flow-card.c8::before{background:linear-gradient(135deg,#7d3c98,#a569bd)}
.flow-card.c9::before{background:linear-gradient(135deg,#b7950b,#d4ac0d)}
.flow-card .fc-inner{position:relative;z-index:1}
.flow-card:hover,.flow-card.active{border-color:transparent;box-shadow:var(--shadow);transform:translateY(-2px)}
.flow-card .fc-icon{font-size:28px;margin-bottom:8px}
.flow-card .fc-name{font-size:14px;font-weight:700;line-height:1.4}
.flow-card .fc-sub{font-size:12px;color:var(--muted);margin-top:4px}
.flow-card.active .fc-sub{color:rgba(255,255,255,.7)}

/* ─── detail panel ─── */
.dp{display:none;background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:28px;margin-bottom:24px;animation:fadeIn .3s ease}
.dp.show{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.dp-header{display:flex;align-items:center;gap:12px;margin-bottom:24px}
.dp-header h2{font-size:20px;font-weight:700}
.close-btn{margin-left:auto;background:var(--bg3);border:1px solid var(--border);color:var(--muted);width:32px;height:32px;border-radius:50%;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;transition:.2s}
.close-btn:hover{background:var(--red);color:#fff;border-color:var(--red)}

/* ─── tabs ─── */
.tab-bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px;border-bottom:1px solid var(--border);padding-bottom:12px}
.tab-btn{background:var(--bg3);border:1px solid var(--border);color:var(--muted);padding:7px 16px;border-radius:20px;cursor:pointer;font-size:13px;transition:.2s;white-space:nowrap}
.tab-btn:hover{color:var(--text);border-color:var(--blue)}
.tab-btn.active{background:var(--blue);color:#fff;border-color:var(--blue)}
.cb{display:none}
.cb.show{display:block}

/* ─── content blocks ─── */
.ic{background:var(--bg3);border-radius:10px;padding:20px;margin-bottom:16px}
.ic h3{font-size:15px;font-weight:700;margin-bottom:12px;color:var(--blue)}
.ic h4{font-size:13px;font-weight:600;margin:14px 0 6px;color:var(--orange)}
.ic p,.ic li{font-size:13px;line-height:1.7;color:var(--text)}
.ic ul,.ic ol{padding-left:20px;margin:8px 0}
.ic ol li{margin-bottom:4px}
.ic code{background:var(--bg4);padding:2px 6px;border-radius:4px;font-size:12px;font-family:monospace;color:var(--cyan)}

/* ─── step list ─── */
.steps{counter-reset:step}
.step-item{display:flex;gap:14px;margin-bottom:12px;align-items:flex-start}
.step-num{min-width:26px;height:26px;border-radius:50%;background:var(--blue);color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px}
.step-text{font-size:13px;line-height:1.7;flex:1}

/* ─── email template card ─── */
.email-card{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:12px;font-size:12px;line-height:1.7;font-family:monospace;white-space:pre-wrap;word-break:break-all;color:var(--muted)}
.email-card.cn{border-left:3px solid var(--orange)}
.email-card.en{border-left:3px solid var(--blue)}
.email-label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}
.email-label.cn{color:var(--orange)}
.email-label.en{color:var(--blue)}

/* ─── info badge ─── */
.badge{display:inline-block;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;margin-right:6px}
.badge.blue{background:rgba(88,166,255,.15);color:var(--blue);border:1px solid rgba(88,166,255,.3)}
.badge.green{background:rgba(63,185,80,.15);color:var(--green);border:1px solid rgba(63,185,80,.3)}
.badge.orange{background:rgba(210,153,34,.15);color:var(--orange);border:1px solid rgba(210,153,34,.3)}
.badge.red{background:rgba(248,81,73,.15);color:var(--red);border:1px solid rgba(248,81,73,.3)}
.badge.purple{background:rgba(188,140,255,.15);color:var(--purple);border:1px solid rgba(188,140,255,.3)}

/* ─── alert/note ─── */
.note{background:rgba(210,153,34,.1);border-left:3px solid var(--orange);padding:12px 16px;border-radius:0 8px 8px 0;font-size:13px;margin:12px 0;color:var(--yellow)}
.note.info{background:rgba(88,166,255,.1);border-color:var(--blue);color:var(--blue)}
.note.danger{background:rgba(248,81,73,.1);border-color:var(--red);color:var(--red)}
.note.success{background:rgba(63,185,80,.1);border-color:var(--green);color:var(--green)}

/* ─── table ─── */
.tbl-wrap{overflow-x:auto;margin:12px 0}
table{width:100%;border-collapse:collapse;font-size:13px}
th{background:var(--bg4);color:var(--text);padding:10px 12px;text-align:left;font-weight:600}
td{padding:9px 12px;border-bottom:1px solid var(--border);vertical-align:top;line-height:1.6}
tr:hover td{background:var(--bg3)}

/* ─── decision tree ─── */
.dtree{display:flex;flex-direction:column;gap:8px;margin:16px 0}
.dtree-row{display:flex;align-items:stretch;gap:0}
.dt-node{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:10px 14px;font-size:13px;text-align:center;min-width:130px}
.dt-arrow{display:flex;align-items:center;padding:0 8px;color:var(--muted);font-size:18px}
.dt-label{font-size:11px;color:var(--muted);text-align:center;margin-top:4px}
.dt-yes{color:var(--green);font-weight:700}
.dt-no{color:var(--red);font-weight:700}

/* ─── logistics table ─── */
.logistics-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin-top:16px}
.lg-card{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:16px}
.lg-name{font-weight:700;font-size:14px;margin-bottom:10px;color:var(--blue)}
.lg-row{display:flex;gap:8px;margin-bottom:6px;font-size:12px}
.lg-key{color:var(--muted);min-width:70px;flex-shrink:0}
.lg-val{color:var(--text);word-break:break-all}

/* ─── dealer table ─── */
.dealer-card{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:16px;margin-bottom:12px}
.dealer-no{font-size:11px;color:var(--muted);margin-bottom:4px}
.dealer-name{font-size:14px;font-weight:700;margin-bottom:8px}
.dealer-row{display:flex;gap:8px;margin-bottom:4px;font-size:12px}
.dealer-key{color:var(--muted);min-width:65px}

/* ─── back-to-top ─── */
#btt{position:fixed;bottom:28px;right:28px;width:42px;height:42px;border-radius:50%;background:var(--bg3);border:1px solid var(--border);color:var(--muted);font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;opacity:0;transition:.3s;z-index:200}
#btt.show{opacity:1}
#btt:hover{background:var(--blue);color:#fff;border-color:var(--blue)}
</style>
</head>
<body>
''')

# ═══════════════════════════════════════════════════════════════════════
# 2. HEADER
# ═══════════════════════════════════════════════════════════════════════
parts.append('''
<header>
  <div class="logo">⚡ AtomStack</div>
  <div class="tagline">海外客服 SOP 帮助中心 · Customer Service SOP Hub</div>
  <div class="lang-btn">
    <button class="active" onclick="setLang('zh')">中文</button>
    <button onclick="setLang('en')">EN</button>
  </div>
</header>
<div class="hero">
  <h1>海外客服 SOP 帮助中心</h1>
  <p>涵盖购买咨询、退货退款、物流处理、工单创建等全流程操作规范及邮件模板，支持中英文切换。</p>
</div>
<div class="main">
''')

# ═══════════════════════════════════════════════════════════════════════
# 3. 主流程图 (9 大节点)
# ═══════════════════════════════════════════════════════════════════════
parts.append('''
<div class="sec-title">📋 主流程导航 · Process Navigator</div>
<div class="flow-grid">
  <div class="flow-card c4" onclick="toggle('d-vat')">
    <div class="fc-inner"><div class="fc-icon">🏷️</div>
      <div class="fc-name">税费 VAT</div>
      <div class="fc-sub">英国 / 瑞士关税处理</div></div></div>
  <div class="flow-card c5" onclick="toggle('d-p1')">
    <div class="fc-inner"><div class="fc-icon">🔔</div>
      <div class="fc-name">P1 召回项目</div>
      <div class="fc-sub">欧盟合规升级说明</div></div></div>
  <div class="flow-card c1" onclick="toggle('d-purchase')">
    <div class="fc-inner"><div class="fc-icon">🛒</div>
      <div class="fc-name">购买咨询</div>
      <div class="fc-sub">软件 / 产品 / 配件购买</div></div></div>
  <div class="flow-card c2" onclick="toggle('d-logistics')">
    <div class="fc-inner"><div class="fc-icon">🚚</div>
      <div class="fc-name">物流相关</div>
      <div class="fc-sub">丢件 / 破损 / 退件处理</div></div></div>
  <div class="flow-card c3" onclick="toggle('d-refund')">
    <div class="fc-inner"><div class="fc-icon">↩️</div>
      <div class="fc-name">退货退款&换货</div>
      <div class="fc-sub">产品问题 / 客户原因</div></div></div>
  <div class="flow-card c6" onclick="toggle('d-policy')">
    <div class="fc-inner"><div class="fc-icon">📄</div>
      <div class="fc-name">官网售后政策</div>
      <div class="fc-sub">保修范围 / 退货政策</div></div></div>
  <div class="flow-card c7" onclick="toggle('d-ticket')">
    <div class="fc-inner"><div class="fc-icon">🎫</div>
      <div class="fc-name">创建工单</div>
      <div class="fc-sub">领星 ERP 工单操作</div></div></div>
  <div class="flow-card c8" onclick="toggle('d-other')">
    <div class="fc-inner"><div class="fc-icon">🔧</div>
      <div class="fc-name">其他事项</div>
      <div class="fc-sub">补发 / 视频会议 / 发票等</div></div></div>
  <div class="flow-card c9" onclick="toggle('d-dealer')">
    <div class="fc-inner"><div class="fc-icon">🏪</div>
      <div class="fc-name">经销商明细</div>
      <div class="fc-sub">11 家经销商信息</div></div></div>
</div>
''')

# ═══════════════════════════════════════════════════════════════════════
# 4. 购买咨询 详情面板
# ═══════════════════════════════════════════════════════════════════════
purchase_data = DATA.get('购买咨询', [])
# rows[0]=表头, rows[1]=场景1 LightBurn, rows[2]=场景2 产品购买, rows[3]=配件询问, rows[4]=配件购买流程
p1 = purchase_data[1] if len(purchase_data)>1 else {}
p2 = purchase_data[2] if len(purchase_data)>2 else {}
p3 = purchase_data[3] if len(purchase_data)>3 else {}
p4 = purchase_data[4] if len(purchase_data)>4 else {}
p2b = purchase_data[3] if len(purchase_data)>3 else {}  # index 3 has D=散客购买
# 实际 rows: [0]表头,[1]LightBurn,[2]企业购买,[3]散客购买,[4]配件询问,[5]配件购买流程
p_lb = purchase_data[1] if len(purchase_data)>1 else {}
p_b2b = purchase_data[2] if len(purchase_data)>2 else {}
p_b2c = purchase_data[3] if len(purchase_data)>3 else {}
p_acc_ask = purchase_data[4] if len(purchase_data)>4 else {}
p_acc_flow = purchase_data[5] if len(purchase_data)>5 else {}

def fmt_steps(text):
    """把 1.xxx\n2.xxx 格式化为步骤列表 HTML"""
    if not text:
        return ''
    lines = text.strip().split('\n')
    out = []
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        m = re.match(r'^(\d+)[\.、]\s*(.*)', ln)
        if m:
            out.append(f'<div class="step-item"><div class="step-num">{m.group(1)}</div><div class="step-text">{esc(m.group(2))}</div></div>')
        else:
            out.append(f'<p>{esc(ln)}</p>')
    return '\n'.join(out)

def email_block(text, lang='cn'):
    """渲染邮件模板块"""
    if not text:
        return ''
    label = '📧 中文模板' if lang=='cn' else '📧 English Template'
    return f'<div class="email-label {lang}">{label}</div><div class="email-card {lang}">{esc(text.strip())}</div>'

parts.append(f'''
<!-- ══ 购买咨询 详情 ══ -->
<div id="d-purchase" class="dp">
<div class="dp-header">
  <span style="font-size:24px">🛒</span>
  <h2>购买咨询</h2>
  <button class="close-btn" onclick="toggle('d-purchase')">✕</button>
</div>
<div class="tab-bar">
  <button class="tab-btn active" onclick="showTab('p','p-lb')">软件购买 (LightBurn)</button>
  <button class="tab-btn" onclick="showTab('p','p-b2b')">产品购买 · 企业客户</button>
  <button class="tab-btn" onclick="showTab('p','p-b2c')">产品购买 · 散客/个人</button>
  <button class="tab-btn" onclick="showTab('p','p-acc-ask')">配件询问购买</button>
  <button class="tab-btn" onclick="showTab('p','p-acc-flow')">配件购买流程</button>
</div>
''')

# 场景1 LightBurn
parts.append(f'''
<div id="p-lb" class="cb show">
<div class="ic"><h3>📌 流程说明</h3>
{fmt_steps(p_lb.get('D',''))}
</div>
{email_block(p_lb.get('E',''), 'cn')}
{email_block(p_lb.get('F',''), 'en')}
</div>
''')

# 场景2 企业客户
b2b_d = p_b2b.get('D','')
parts.append(f'''
<div id="p-b2b" class="cb">
<div class="ic"><h3>📌 流程 / 说明</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(b2b_d)}</div>
</div>
''')
for col in ['E','F','G','H','I']:
    v = p_b2b.get(col,'')
    if v:
        parts.append(email_block(v, 'en' if col in ['F','H'] else 'cn'))
parts.append('</div>')

# 场景2b 散客
b2c_d = p_b2c.get('D','')
parts.append(f'''
<div id="p-b2c" class="cb">
<div class="ic"><h3>📌 流程 / 说明</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(b2c_d)}</div>
</div>
''')
for col,lang in [('E','cn'),('F','en'),('G','cn'),('H','en')]:
    v = p_b2c.get(col,'')
    if v:
        parts.append(email_block(v, lang))
parts.append('</div>')

# 场景3 配件询问
parts.append(f'''
<div id="p-acc-ask" class="cb">
<div class="ic"><h3>📌 购买配件 — 解决思路</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(p_acc_ask.get('D',''))}</div>
</div>
{email_block(p_acc_ask.get('E',''), 'cn')}
{email_block(p_acc_ask.get('F',''), 'en')}
</div>
''')

# 场景4 配件购买流程
parts.append(f'''
<div id="p-acc-flow" class="cb">
<div class="ic"><h3>📌 配件购买流程</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(p_acc_flow.get('D',''))}</div>
</div>
{email_block(p_acc_flow.get('E',''), 'cn')}
{email_block(p_acc_flow.get('F',''), 'en')}
{email_block(p_acc_flow.get('G',''), 'cn')}
{email_block(p_acc_flow.get('H',''), 'en')}
</div>
</div><!-- end d-purchase -->
''')

# ═══════════════════════════════════════════════════════════════════════
# 5. 退货退款 详情面板
# ═══════════════════════════════════════════════════════════════════════
refund_data = DATA.get('退货退款&换货', [])
# rows: [0]=表头, [1]=产品问题已开箱未使用, [2]=产品问题已开箱已使用, [3]=客户问题已开箱, [4]=客户问题未开箱, [5]=换货

def refund_block(row):
    d = row.get('D','')
    cols = [('E','cn'),('F','en'),('G','cn'),('H','en'),('I','cn'),('J','en')]
    html = f'''<div class="ic"><h3>📌 流程 / 说明</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(d)}</div></div>\n'''
    for col,lang in cols:
        v = row.get(col,'')
        if v:
            html += email_block(v, lang)
    return html

parts.append('''
<!-- ══ 退货退款 详情 ══ -->
<div id="d-refund" class="dp">
<div class="dp-header">
  <span style="font-size:24px">↩️</span>
  <h2>退货退款 &amp; 换货</h2>
  <button class="close-btn" onclick="toggle('d-refund')">✕</button>
</div>
<div class="note">📌 退货标签申请前须确认：货值 ≥ RMB 300，否则不予退货。退款金额优先参考官网售后政策。</div>
<div class="tab-bar">
  <button class="tab-btn active" onclick="showTab('r','r-p1')">产品问题·已开箱未使用</button>
  <button class="tab-btn" onclick="showTab('r','r-p2')">产品问题·已开箱已使用</button>
  <button class="tab-btn" onclick="showTab('r','r-c1')">客户问题·已开箱</button>
  <button class="tab-btn" onclick="showTab('r','r-c2')">客户问题·未开箱</button>
  <button class="tab-btn" onclick="showTab('r','r-ex')">换货流程</button>
</div>
''')

for tab_id, idx in [('r-p1',1),('r-p2',2),('r-c1',3),('r-c2',4),('r-ex',5)]:
    row = refund_data[idx] if len(refund_data)>idx else {}
    show_cls = 'show' if tab_id=='r-p1' else ''
    scenario_title = {
        'r-p1': '产品问题 · 已开箱未使用',
        'r-p2': '产品问题 · 已开箱已使用',
        'r-c1': '客户问题 · 已开箱',
        'r-c2': '客户问题 · 未开箱',
        'r-ex': '换货操作流程',
    }[tab_id]
    ctx_c = row.get('C','')
    parts.append(f'<div id="{tab_id}" class="cb {show_cls}">')
    if ctx_c:
        parts.append(f'<div class="note info">📋 适用场景：{nl2br(ctx_c)}</div>')
    parts.append(refund_block(row))
    parts.append('</div>')

parts.append('</div><!-- end d-refund -->')

# ═══════════════════════════════════════════════════════════════════════
# 6. 创建工单 详情面板
# ═══════════════════════════════════════════════════════════════════════
ticket_data = DATA.get('创建工单', [])

def build_ticket_steps(rows, start_b):
    """从 rows 中提取某 B 列分组的步骤"""
    steps = []
    in_group = False
    for r in rows[1:]:
        b = r.get('B','').strip()
        c = r.get('C','').strip()
        d = r.get('D','').strip()
        if b == start_b:
            in_group = True
        elif b and b != start_b:
            if in_group:
                break
        if in_group and c and d:
            steps.append((c, d))
    return steps

parts.append('''
<!-- ══ 创建工单 详情 ══ -->
<div id="d-ticket" class="dp">
<div class="dp-header">
  <span style="font-size:24px">🎫</span>
  <h2>创建工单（领星 ERP）</h2>
  <button class="close-btn" onclick="toggle('d-ticket')">✕</button>
</div>
<div class="note info">💡 适用于领星ERP系统中创建售后工单，包括退货退款、仅退货、仅补发等类型。</div>
<div class="tab-bar">
  <button class="tab-btn active" onclick="showTab('t','t-rr')">退货退款</button>
  <button class="tab-btn" onclick="showTab('t','t-ro')">仅退货</button>
  <button class="tab-btn" onclick="showTab('t','t-rs')">仅补发</button>
  <button class="tab-btn" onclick="showTab('t','t-rb')">退货补发</button>
</div>
''')

def render_ticket_tab(tab_id, b_key, show=False):
    steps = build_ticket_steps(ticket_data, b_key)
    cls = 'show' if show else ''
    html = f'<div id="{tab_id}" class="cb {cls}"><div class="ic"><h3>📋 操作步骤</h3>'
    if steps:
        for num, desc in steps:
            html += f'<div class="step-item"><div class="step-num">{esc(num)}</div><div class="step-text">{nl2br(desc)}</div></div>'
    else:
        html += '<p style="color:var(--muted)">参考退货退款流程步骤1-4，然后按照对应类型操作。</p>'
    html += '</div></div>'
    return html

parts.append(render_ticket_tab('t-rr', '退货退款', True))
parts.append(render_ticket_tab('t-ro', '仅退货'))
parts.append(render_ticket_tab('t-rs', '仅补发'))
parts.append('''
<div id="t-rb" class="cb">
<div class="ic"><h3>📋 退货补发说明</h3>
<p>退货补发是退货与补发的组合流程：</p>
<div class="step-item"><div class="step-num">1</div><div class="step-text">参考"退货退款"流程创建退货工单</div></div>
<div class="step-item"><div class="step-num">2</div><div class="step-text">确认退件入仓后，在原订单上创建补发工单</div></div>
<div class="step-item"><div class="step-num">3</div><div class="step-text">补发工单中金额填写"0"</div></div>
<div class="step-item"><div class="step-num">4</div><div class="step-text">备注中详细说明退货原因及补发产品信息</div></div>
<div class="step-item"><div class="step-num">5</div><div class="step-text">在《独立站产品、订单问题解决沟通群》@钟总审批</div></div>
</div>
</div>
</div><!-- end d-ticket -->
''')

# ═══════════════════════════════════════════════════════════════════════
# 7. 物流相关 详情面板
# ═══════════════════════════════════════════════════════════════════════
logistics_data = DATA.get('物流相关', [])

# 提取物流场景分类
logistics_cats = {}
current_b = None
for r in logistics_data[1:]:
    b = r.get('B','').strip()
    if b:
        current_b = b
    if current_b:
        if current_b not in logistics_cats:
            logistics_cats[current_b] = []
        logistics_cats[current_b].append(r)

parts.append('''
<!-- ══ 物流相关 详情 ══ -->
<div id="d-logistics" class="dp">
<div class="dp-header">
  <span style="font-size:24px">🚚</span>
  <h2>物流相关</h2>
  <button class="close-btn" onclick="toggle('d-logistics')">✕</button>
</div>
<div class="tab-bar">
  <button class="tab-btn active" onclick="showTab('l','l-miss')">未妥投</button>
  <button class="tab-btn" onclick="showTab('l','l-damage')">包裹破损</button>
  <button class="tab-btn" onclick="showTab('l','l-delivery')">配送问题</button>
  <button class="tab-btn" onclick="showTab('l','l-sign')">签收异常</button>
  <button class="tab-btn" onclick="showTab('l','l-reject')">退件/拒收</button>
  <button class="tab-btn" onclick="showTab('l','l-freight')">运费争议</button>
  <button class="tab-btn" onclick="showTab('l','l-query')">物流查询表</button>
</div>
''')

# 未妥投
miss_rows = logistics_cats.get('未妥投', [])
miss_subs = [r.get('C','').strip() for r in miss_rows if r.get('C','').strip()]
# 通用补发流程
common_flow = ''
for r in logistics_data:
    h = r.get('H','')
    if h and '补发流程' in h:
        common_flow = h
        break

parts.append(f'''
<div id="l-miss" class="cb show">
<div class="ic"><h3>未妥投 — 场景分类</h3>
<ul>{''.join(f"<li>{esc(s)}</li>" for s in miss_subs if s)}</ul>
</div>
<div class="ic"><h3>📋 通用处理流程</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(common_flow)}</div>
</div>
</div>
''')

def simple_tab(tab_id, b_key, show=False):
    rows = logistics_cats.get(b_key, [])
    subs = [r.get('C','').strip() for r in rows if r.get('C','').strip()]
    notes = [r.get('G','').strip() for r in rows if r.get('G','').strip()]
    cls = 'show' if show else ''
    html = f'<div id="{tab_id}" class="cb {cls}"><div class="ic"><h3>{esc(b_key)} — 场景分类</h3>'
    if subs:
        html += '<ul>' + ''.join(f'<li>{esc(s)}</li>' for s in subs) + '</ul>'
    for n in notes:
        html += f'<div class="note">{nl2br(n)}</div>'
    html += '</div></div>'
    return html

parts.append(simple_tab('l-damage', '包裹破损'))
parts.append(simple_tab('l-delivery', '配送问题'))
parts.append(simple_tab('l-sign', '签收异常'))

# 退件/拒收 — 有详细说明
reject_rows = logistics_cats.get('退件/拒收', [])
reject_subs = [r.get('C','').strip() for r in reject_rows if r.get('C','').strip()]
reject_notes = [r.get('G','').strip() for r in reject_rows if r.get('G','').strip()]
parts.append(f'''
<div id="l-reject" class="cb">
<div class="ic"><h3>退件/拒收 — 场景分类</h3>
<ul>{''.join(f"<li>{esc(s)}</li>" for s in reject_subs if s)}</ul>
</div>
{"".join(f'<div class="note">{nl2br(n)}</div>' for n in reject_notes)}
</div>
''')

# 运费争议
freight_rows = logistics_cats.get('运费争议', [])
freight_notes = []
for r in logistics_data:
    g = r.get('G','').strip()
    if g and '退回运费' in g:
        freight_notes.append(g)
parts.append(f'''
<div id="l-freight" class="cb">
<div class="ic"><h3>运费争议 — 说明</h3>
{"".join(f'<div class="note">{esc(n)}</div>' for n in freight_notes)}
<p style="font-size:13px;margin-top:12px">退回运费 = 发货时运费（领星 → 详情 → 查询运费，注意汇率换算）</p>
</div>
</div>
''')

# 物流查询表
logistics_query = DATA.get('物流信息查询表', [])
parts.append('''<div id="l-query" class="cb">
<div class="sec-title" style="margin-top:0">📡 物流商查询表</div>
<div class="logistics-grid">''')
for row in logistics_query[1:]:
    name = row.get('C','').strip()
    if not name:
        continue
    url = row.get('D','').strip()
    fmt = row.get('E','').strip()
    eg = row.get('F','').strip()
    platform = row.get('G','').strip()
    region = row.get('H','').strip()
    note = row.get('I','').strip()
    parts.append(f'''
<div class="lg-card">
  <div class="lg-name">{esc(name)}</div>
  {f'<div class="lg-row"><div class="lg-key">查询链接</div><div class="lg-val"><a href="{esc(url)}" target="_blank" style="color:var(--blue)">{esc(url)}</a></div></div>' if url else ''}
  {f'<div class="lg-row"><div class="lg-key">单号格式</div><div class="lg-val">{nl2br(fmt)}</div></div>' if fmt else ''}
  {f'<div class="lg-row"><div class="lg-key">示例单号</div><div class="lg-val"><code>{esc(eg)}</code></div></div>' if eg else ''}
  {f'<div class="lg-row"><div class="lg-key">适用平台</div><div class="lg-val">{esc(platform)}</div></div>' if platform else ''}
  {f'<div class="lg-row"><div class="lg-key">适用地区</div><div class="lg-val">{esc(region)}</div></div>' if region else ''}
  {f'<div class="lg-row"><div class="lg-key">备注</div><div class="lg-val">{esc(note)}</div></div>' if note else ''}
</div>''')
parts.append('''</div></div>
</div><!-- end d-logistics -->''')

# ═══════════════════════════════════════════════════════════════════════
# 8. 官网售后政策 详情面板
# ═══════════════════════════════════════════════════════════════════════
policy_data = DATA.get('官网售后政策', [])

parts.append('''
<!-- ══ 官网售后政策 详情 ══ -->
<div id="d-policy" class="dp">
<div class="dp-header">
  <span style="font-size:24px">📄</span>
  <h2>官网售后政策（精简版）</h2>
  <button class="close-btn" onclick="toggle('d-policy')">✕</button>
</div>
<div class="tab-bar">
  <button class="tab-btn active" onclick="showTab('po','po-warranty')">保修范围</button>
  <button class="tab-btn" onclick="showTab('po','po-return')">退货政策</button>
  <button class="tab-btn" onclick="showTab('po','po-fee')">服务费说明</button>
  <button class="tab-btn" onclick="showTab('po','po-nocover')">不在保修范围</button>
  <button class="tab-btn" onclick="showTab('po','po-hurricane')">Hurricane CO2 特殊条款</button>
</div>
''')

# 保修范围
warranty_rows = [r for r in policy_data if r.get('A','')=='保修范围' or (r.get('B','') and r.get('C','') and r.get('A','')=='')]
# 更精确：找 B=主机核心部件 等的行
wrows = [r for r in policy_data if r.get('B','') in ['主机核心部件','主机框架部件','选配配件','耗材','LightBurn授权码']]
parts.append('''<div id="po-warranty" class="cb show">
<div class="ic"><h3>🛡️ 保修范围 / 保修期</h3>
<div class="tbl-wrap"><table>
<thead><tr><th>类别</th><th>保修期</th><th>说明</th></tr></thead><tbody>''')
for r in wrows:
    parts.append(f'<tr><td>{esc(r.get("B",""))}</td><td>{esc(r.get("C",""))}</td><td>{esc(r.get("D",""))}</td></tr>')
parts.append('</tbody></table></div></div></div>')

# 退货政策
parts.append('''<div id="po-return" class="cb">
<div class="ic"><h3>📦 退货政策 — 核心规则</h3>''')
# 关键时间节点
time_row = next((r for r in policy_data if r.get('E','').strip().startswith('\n退货申请')), None)
if time_row:
    parts.append(f'<div class="note info">⏰ 关键时间节点<br>{nl2br(time_row.get("E",""))}</div>')
# 未拆封
parts.append('''<h4 style="color:var(--orange);margin:16px 0 8px">未拆封商品</h4>
<div class="tbl-wrap"><table>
<thead><tr><th>商品类型</th><th>时间窗口</th><th>服务费</th></tr></thead><tbody>''')
sealed_rows = [r for r in policy_data if r.get('B','') in ['主机','配件','耗材'] and r.get('A','')=='']
for r in sealed_rows:
    parts.append(f'<tr><td>{esc(r.get("B",""))}</td><td>{esc(r.get("C",""))}</td><td>{esc(r.get("D",""))}</td></tr>')
parts.append('</tbody></table></div>')
# 已拆封主机
parts.append('''<h4 style="color:var(--orange);margin:16px 0 8px">已拆封商品（主机）</h4>
<div class="tbl-wrap"><table>
<thead><tr><th>状态</th><th>时间窗口</th><th>无质量问题</th><th>有质量问题</th></tr></thead><tbody>''')
opened_machine = [r for r in policy_data if r.get('B','') in ['未使用','已使用（<50次）','已使用'] and r.get('A','')=='']
for r in opened_machine:
    parts.append(f'<tr><td>{esc(r.get("B",""))}</td><td>{esc(r.get("C",""))}</td><td>{esc(r.get("D",""))}</td><td class="badge green">{esc(r.get("E",""))}</td></tr>')
parts.append('</tbody></table></div>')
# 已拆封配件
parts.append('''<h4 style="color:var(--orange);margin:16px 0 8px">已拆封商品（配件）</h4>
<div class="tbl-wrap"><table>
<thead><tr><th>状态</th><th>时间窗口</th><th>无质量问题</th><th>有质量问题</th></tr></thead><tbody>''')
opened_acc = [r for r in policy_data if r.get('B','') in ['未使用/已使用'] and r.get('A','')=='']
for r in opened_acc:
    parts.append(f'<tr><td>{esc(r.get("B",""))}</td><td>{esc(r.get("C",""))}</td><td>{esc(r.get("D",""))}</td><td class="badge green">{esc(r.get("E",""))}</td></tr>')
parts.append('</tbody></table></div></div></div>')

# 服务费说明
fee_rows = [r for r in policy_data if r.get('A','')=='服务费说明' or (r.get('B','') and r.get('A','')=='服务费说明')]
# 精确取
fee_start = False
fee_list = []
for r in policy_data:
    if r.get('A','')=='服务费说明':
        fee_start = True
    elif r.get('A','') and r.get('A','')!='服务费说明' and fee_start:
        break
    if fee_start and r.get('B',''):
        fee_list.append(r)

parts.append('''<div id="po-fee" class="cb">
<div class="ic"><h3>💰 服务费说明</h3>
<div class="tbl-wrap"><table>
<thead><tr><th>情况</th><th>服务费</th><th>说明</th><th>特殊情况</th></tr></thead><tbody>''')
for r in fee_list:
    fee_pct = r.get('C','')
    if isinstance(fee_pct, float):
        fee_pct = f'{int(fee_pct*100)}%'
    parts.append(f'<tr><td>{esc(r.get("B",""))}</td><td><span class="badge orange">{esc(str(fee_pct))}</span></td><td>{nl2br(r.get("D",""))}</td><td>{esc(r.get("E",""))}</td></tr>')
parts.append('</tbody></table></div></div></div>')

# 不在保修范围
nocover_rows = []
nc_start = False
for r in policy_data:
    if r.get('A','')=='不在保修范围内':
        nc_start = True
    elif r.get('A','') and r.get('A','')!='不在保修范围内' and nc_start:
        break
    if nc_start and r.get('B',''):
        nocover_rows.append(r.get('B',''))

parts.append(f'''<div id="po-nocover" class="cb">
<div class="ic"><h3>❌ 不在保修范围项目清单</h3>
<ul>{''.join(f"<li>{esc(item)}</li>" for item in nocover_rows if item.strip())}</ul>
</div></div>''')

# Hurricane CO2 特殊条款
hurr_rows = []
h_start = False
for r in policy_data:
    if r.get('A','') == 'Hurricane CO2激光机特殊条款':
        h_start = True
    if h_start and r.get('B','') and r.get('A','')!='Hurricane CO2激光机特殊条款':
        hurr_rows.append(r)

parts.append('''<div id="po-hurricane" class="cb">
<div class="ic"><h3>🌀 Hurricane CO2 激光机 — 特殊保修条款</h3>
<div class="tbl-wrap"><table>
<thead><tr><th>保修期</th><th>适用部件</th></tr></thead><tbody>''')
for r in hurr_rows:
    parts.append(f'<tr><td>{esc(r.get("B",""))}</td><td>{esc(r.get("C",""))}</td></tr>')
parts.append('</tbody></table></div></div></div>')

parts.append('</div><!-- end d-policy -->')

# ═══════════════════════════════════════════════════════════════════════
# 9. 其他事项 详情面板
# ═══════════════════════════════════════════════════════════════════════
other_data = DATA.get('其他', [])

def other_row(b_key):
    for r in other_data:
        if r.get('B','').strip() == b_key:
            return r
    return {}

parts.append('''
<!-- ══ 其他事项 详情 ══ -->
<div id="d-other" class="dp">
<div class="dp-header">
  <span style="font-size:24px">🔧</span>
  <h2>其他事项</h2>
  <button class="close-btn" onclick="toggle('d-other')">✕</button>
</div>
<div class="tab-bar">
  <button class="tab-btn active" onclick="showTab('o','o-resend')">售后补发</button>
  <button class="tab-btn" onclick="showTab('o','o-vm')">视频会议</button>
  <button class="tab-btn" onclick="showTab('o','o-invoice')">电子发票</button>
  <button class="tab-btn" onclick="showTab('o','o-file')">大文件分享</button>
  <button class="tab-btn" onclick="showTab('o','o-diff')">补差价链接</button>
  <button class="tab-btn" onclick="showTab('o','o-non')">非自营订单</button>
  <button class="tab-btn" onclick="showTab('o','o-addr')">地址整理</button>
  <button class="tab-btn" onclick="showTab('o','o-klarna')">Klarna规则</button>
  <button class="tab-btn" onclick="showTab('o','o-paypal')">PayPal规则</button>
</div>
''')

# 售后补发
resend_rows = [r for r in other_data if r.get('B','').strip() == '售后补发' or (r.get('B','')== '' and r.get('C','').strip().startswith(('平台补发','售后补发')))]
parts.append('''<div id="o-resend" class="cb show">
<div class="ic"><h3>📦 两类补发说明</h3>''')
for r in other_data[1:5]:
    c = r.get('C','').strip()
    if c and ('补发' in c or c.startswith('两类')):
        parts.append(f'<div style="white-space:pre-wrap;font-size:13px;line-height:1.7;margin-bottom:12px">{esc(c)}</div>')
        d = r.get('D','').strip()
        if d:
            parts.append(f'<div class="note">{esc(d)}</div>')
parts.append('</div></div>')

# 视频会议
vm_row = other_row('视频会议')
parts.append(f'''<div id="o-vm" class="cb">
<div class="ic"><h3>🎥 视频会议流程</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(vm_row.get("C",""))}</div>
</div></div>''')

# 电子发票
inv_row = other_row('电子发票')
parts.append(f'''<div id="o-invoice" class="cb">
<div class="ic"><h3>🧾 电子发票开具</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(inv_row.get("C",""))}</div>
</div></div>''')

# 大文件分享
file_rows = [r for r in other_data if r.get('B','').strip() == '大文件分享链接' or (not r.get('B','').strip() and r.get('C','').strip() and 'transfer' in r.get('C','').lower())]
parts.append('<div id="o-file" class="cb"><div class="ic"><h3>📁 大文件分享工具</h3>')
for r in file_rows:
    c = r.get('C','').strip()
    d = r.get('D','').strip()
    if c:
        parts.append(f'<div style="margin-bottom:8px"><span class="badge {("green" if d=="推荐" else "blue")}">{("⭐ 推荐" if d=="推荐" else "")}</span> {esc(c)}</div>')
parts.append('</div></div>')

# 补差价链接
diff_rows = [r for r in other_data if r.get('B','').strip() == '补差价链接' or (not r.get('B','').strip() and r.get('C','').strip() and ('atomstack.com/products/pay' in r.get('C','') or 'ikier.com/products/pay' in r.get('C','') or 'ikier.com/en' in r.get('C','')))]
parts.append('<div id="o-diff" class="cb"><div class="ic"><h3>💳 补差价链接</h3>')
for r in diff_rows:
    c = r.get('C','').strip()
    if c and 'http' in c:
        parts.append(f'<div style="margin-bottom:8px"><a href="{esc(c)}" target="_blank" style="color:var(--blue)">{esc(c)}</a></div>')
parts.append('</div></div>')

# 非自营订单
non_row = other_row('非自营订单')
parts.append(f'''<div id="o-non" class="cb">
<div class="ic"><h3>🏪 非自营订单处理</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(non_row.get("C",""))}</div>
</div>
<div class="ic"><h4>群内通知模板</h4>
<div class="email-card cn">{esc(non_row.get("D",""))}</div>
</div>
</div>''')

# 地址整理
addr_rows = [r for r in other_data if r.get('B','').strip() == '地址整理']
addr_tmpl = addr_rows[0].get('C','') if addr_rows else ''
parts.append(f'''<div id="o-addr" class="cb">
<div class="ic"><h3>📬 地址整理模板</h3>
<div class="email-card cn">{esc(addr_tmpl)}</div>
</div></div>''')

# Klarna
klarna_row = other_row('Klarna 规则')
parts.append(f'''<div id="o-klarna" class="cb">
<div class="ic"><h3>💳 Klarna 规则（先买后付）</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(klarna_row.get("C",""))}</div>
</div>
<div class="ic"><h3>📋 退款规则 / 不接受退款情况</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(klarna_row.get("D",""))}</div>
</div></div>''')

# PayPal
paypal_row = other_row('PayPal 规则')
parts.append(f'''<div id="o-paypal" class="cb">
<div class="ic"><h3>💰 PayPal 规则</h3>
<p style="color:var(--muted);font-size:13px">PayPal 规则详情请参考内部运营文档或向运营团队确认最新规则。</p>
{f'<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(paypal_row.get("C",""))}</div>' if paypal_row.get("C","") else ""}
</div></div>''')

parts.append('</div><!-- end d-other -->')

# ═══════════════════════════════════════════════════════════════════════
# 10. VAT 税费 详情面板
# ═══════════════════════════════════════════════════════════════════════
vat_uk_flow = other_row('英国 - 关税 流程 / 说明')
vat_uk_yes = other_row('英国 - 客户接受关税')
vat_uk_no  = other_row('英国 - 客户不接受关税')
vat_ch_flow = other_row('瑞士 - 关税 流程 / 说明')
vat_ch_yes  = other_row('瑞士 - 客户接受关税')
vat_ch_no   = other_row('瑞士 - 客户不接受关税')

parts.append('''
<!-- ══ VAT 税费 详情 ══ -->
<div id="d-vat" class="dp">
<div class="dp-header">
  <span style="font-size:24px">🏷️</span>
  <h2>税费 VAT 处理</h2>
  <button class="close-btn" onclick="toggle('d-vat')">✕</button>
</div>
<div class="tab-bar">
  <button class="tab-btn active" onclick="showTab('v','v-uk-flow')">英国 · 关税流程</button>
  <button class="tab-btn" onclick="showTab('v','v-uk-yes')">英国 · 客户接受</button>
  <button class="tab-btn" onclick="showTab('v','v-uk-no')">英国 · 客户不接受</button>
  <button class="tab-btn" onclick="showTab('v','v-ch-flow')">瑞士 · 关税流程</button>
  <button class="tab-btn" onclick="showTab('v','v-ch-yes')">瑞士 · 客户接受</button>
  <button class="tab-btn" onclick="showTab('v','v-ch-no')">瑞士 · 客户不接受</button>
</div>
''')

for tab_id, row, show in [
    ('v-uk-flow', vat_uk_flow, True),
    ('v-uk-yes',  vat_uk_yes,  False),
    ('v-uk-no',   vat_uk_no,   False),
    ('v-ch-flow', vat_ch_flow, False),
    ('v-ch-yes',  vat_ch_yes,  False),
    ('v-ch-no',   vat_ch_no,   False),
]:
    cls = 'show' if show else ''
    c_text = row.get('C','') or row.get('B','')
    parts.append(f'''<div id="{tab_id}" class="cb {cls}">
<div class="ic"><h3>📋 流程 / 说明</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(c_text)}</div>
</div>
{email_block(row.get("D",""), "cn")}
{email_block(row.get("E",""), "en")}
</div>''')

parts.append('</div><!-- end d-vat -->')

# ═══════════════════════════════════════════════════════════════════════
# 11. P1 召回 详情面板
# ═══════════════════════════════════════════════════════════════════════
p1_rows = [r for r in other_data if 'P1召回项目' in r.get('B','')]

parts.append('''
<!-- ══ P1 召回 详情 ══ -->
<div id="d-p1" class="dp">
<div class="dp-header">
  <span style="font-size:24px">🔔</span>
  <h2>P1 召回项目</h2>
  <button class="close-btn" onclick="toggle('d-p1')">✕</button>
</div>
<div class="note danger">⚠️ 此召回为基于欧盟监管要求的预防性合规升级，并非产品存在安全事故。</div>
<div class="tab-bar">
  <button class="tab-btn active" onclick="showTab('p1','p1-non-eu')">非欧盟国家 · 咨询回复</button>
  <button class="tab-btn" onclick="showTab('p1','p1-eu')">欧盟国家 · 咨询回复</button>
  <button class="tab-btn" onclick="showTab('p1','p1-refund')">退货退款流程（仅自营）</button>
</div>
''')

for row in other_data:
    b = row.get('B','').strip()
    c = row.get('C','').strip()
    if 'P1召回' in b and '仅咨询' in b:
        # 非欧盟
        non_eu_row = next((r for r in other_data if r.get('C','').strip().startswith('非欧盟国家')), None)
        eu_row = next((r for r in other_data if r.get('C','').strip().startswith('欧盟国家')), None)
        break

# 非欧盟
non_eu_rows = [r for r in other_data if r.get('C','').strip().startswith('非欧盟国家')]
eu_rows = [r for r in other_data if r.get('C','').strip().startswith('欧盟国家')]
refund_p1_rows = [r for r in other_data if 'P1召回' in r.get('B','') and '退货退款' in r.get('B','')]

if non_eu_rows:
    r = non_eu_rows[0]
    parts.append(f'''<div id="p1-non-eu" class="cb show">
<div class="ic"><h3>🌎 非欧盟国家 — 咨询官方统一回复</h3></div>
{email_block(r.get("D",""), "cn")}
{email_block(r.get("E",""), "en")}
</div>''')
else:
    parts.append('<div id="p1-non-eu" class="cb show"><div class="note">暂无数据</div></div>')

if eu_rows:
    r = eu_rows[0]
    parts.append(f'''<div id="p1-eu" class="cb">
<div class="ic"><h3>🇪🇺 欧盟国家 — 咨询说明/回复</h3></div>
{email_block(r.get("D",""), "cn")}
{email_block(r.get("E",""), "en")}
</div>''')
else:
    parts.append('<div id="p1-eu" class="cb"><div class="note">暂无数据</div></div>')

if refund_p1_rows:
    r = refund_p1_rows[0]
    parts.append(f'''<div id="p1-refund" class="cb">
<div class="ic"><h3>📋 P1 退货退款 — 处理说明（仅针对自营订单）</h3>
<div style="white-space:pre-wrap;font-size:13px;line-height:1.7">{esc(r.get("C",""))}</div>
</div>
{email_block(r.get("D",""), "cn")}
{email_block(r.get("E",""), "en")}
</div>''')
else:
    parts.append('<div id="p1-refund" class="cb"><div class="note">暂无数据</div></div>')

parts.append('</div><!-- end d-p1 -->')

# ═══════════════════════════════════════════════════════════════════════
# 12. 经销商明细 详情面板
# ═══════════════════════════════════════════════════════════════════════
dealer_data = DATA.get('经销商明细', [])

parts.append('''
<!-- ══ 经销商明细 详情 ══ -->
<div id="d-dealer" class="dp">
<div class="dp-header">
  <span style="font-size:24px">🏪</span>
  <h2>经销商明细</h2>
  <button class="close-btn" onclick="toggle('d-dealer')">✕</button>
</div>
<div class="note info">💡 质保期内的非直营订单，需先确认所属经销商后再处理。</div>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px;margin-top:16px">
''')

for r in dealer_data[1:]:
    no = r.get('A','')
    if not no:
        continue
    platform = r.get('B','')
    shop = r.get('C','')
    dealer = r.get('D','')
    note = r.get('E','')
    contact = r.get('G','')
    parts.append(f'''
<div class="dealer-card">
  <div class="dealer-no">#{esc(str(no))}</div>
  <div class="dealer-name">{esc(dealer)} <span class="badge blue">{esc(platform)}</span></div>
  {f'<div class="dealer-row"><div class="dealer-key">店铺名</div><div>{esc(shop)}</div></div>' if shop else ''}
  {f'<div class="dealer-row"><div class="dealer-key">备注</div><div style="white-space:pre-wrap">{esc(note)}</div></div>' if note else ''}
  {f'<div class="dealer-row"><div class="dealer-key">内部对接</div><div><span class="badge purple">{esc(contact)}</span></div></div>' if contact else ''}
</div>''')

parts.append('''</div>
</div><!-- end d-dealer -->
''')

# ═══════════════════════════════════════════════════════════════════════
# 13. CLOSE MAIN + JS + FOOTER
# ═══════════════════════════════════════════════════════════════════════
parts.append('''
</div><!-- end .main -->

<button id="btt" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>

<script>
// ─── toggle detail panel ───
function toggle(id){
  const el = document.getElementById(id);
  if(!el) return;
  const isShow = el.classList.contains('show');
  // close all
  document.querySelectorAll('.dp').forEach(d=>{ d.classList.remove('show'); });
  if(!isShow){
    el.classList.add('show');
    el.scrollIntoView({behavior:'smooth', block:'start'});
  }
}

// ─── tab switcher ───
function showTab(group, tabId){
  // hide all .cb in same panel
  const panel = document.getElementById(tabId).closest('.dp');
  if(!panel) return;
  panel.querySelectorAll('.cb').forEach(c=>c.classList.remove('show'));
  panel.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  const target = document.getElementById(tabId);
  if(target) target.classList.add('show');
  // find clicked btn
  event.target.classList.add('active');
}

// ─── back to top ───
window.addEventListener('scroll',()=>{
  const b = document.getElementById('btt');
  if(b) b.classList.toggle('show', window.scrollY > 300);
});

// ─── language switch (hide/show CN vs EN elements) ───
function setLang(lang){
  document.querySelectorAll('.lang-btn button').forEach(b=>b.classList.remove('active'));
  event.target.classList.add('active');
  if(lang==='en'){
    document.querySelectorAll('.email-card.cn,.email-label.cn').forEach(e=>e.style.display='none');
    document.querySelectorAll('.email-card.en,.email-label.en').forEach(e=>e.style.display='block');
  } else {
    document.querySelectorAll('.email-card.cn,.email-label.cn,.email-card.en,.email-label.en').forEach(e=>e.style.display='');
  }
}
</script>
</body>
</html>
''')

# ═══════════════════════════════════════════════════════════════════════
# 写入文件
# ═══════════════════════════════════════════════════════════════════════
html = ''.join(parts)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = os.path.getsize(OUT) // 1024
print(f'✅ 生成完成: {OUT}  ({size_kb} KB)')
