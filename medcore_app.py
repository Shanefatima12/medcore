"""
MedCore — Hospital Intelligence Platform v2.0
Enhanced with real hospital data & charts
HOD Pitch Ready | Deploy Ready
Run: streamlit run medcore_app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MedCore — Hospital Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# LOGIN SYSTEM
# ─────────────────────────────────────────
USERS = {
    "drfatima":   ["doctor123",   "doctor",     "Dr. Fatima Zahra"],
    "drkhan":     ["doctor456",   "doctor",     "Dr. Ahmed Khan"],
    "reception1": ["recep123",    "reception",  "Reception Staff"],
    "director":   ["director123", "management", "Hospital Director"],
}
ROLE_VIEW  = {"doctor":"👨‍⚕️ Doctor View","reception":"🧾 Reception & Admin",
               "management":"📊 Management"}
ROLE_EMOJI = {"doctor":"👨‍⚕️","reception":"🧾","management":"📊"}

def show_login():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"]{background:#04080f !important;}
    [data-testid="stSidebar"]{display:none;}
    </style>""", unsafe_allow_html=True)
    col1,col2,col3 = st.columns([1,1.1,1])
    with col2:
        st.markdown("""
        <div style='text-align:center;padding:3rem 0 1.5rem;'>
          <div style='font-size:3.5rem;'>🏥</div>
          <div style='font-family:"IBM Plex Mono",monospace;font-size:1.8rem;
                      font-weight:700;letter-spacing:3px;
                      background:linear-gradient(90deg,#00e5ff,#00ff9d);
                      -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
            MedCore</div>
          <div style='font-size:0.72rem;color:#4a6fa5;letter-spacing:3px;
                      text-transform:uppercase;margin-top:0.3rem;'>
            Hospital Intelligence Platform</div>
          <div style='font-size:0.65rem;color:#1a3058;margin-top:0.3rem;
                      font-family:"IBM Plex Mono",monospace;'>
            v2.0 · SSUET BME · Karachi</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:#0b1425;border:1px solid #112240;border-radius:16px;
                    padding:1.5rem 1.5rem 0.5rem;margin-bottom:0.8rem;'>
          <div style='font-family:"IBM Plex Mono",monospace;font-size:0.68rem;
                      color:#4a6fa5;letter-spacing:2px;text-transform:uppercase;
                      text-align:center;margin-bottom:1rem;'>🔐 Secure Clinical Access</div>
        </div>""", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter username", key="lu")
        password = st.text_input("Password", placeholder="Enter password",
                                  type="password", key="lp")
        if st.button("Login to MedCore →", use_container_width=True):
            if username in USERS:
                if USERS[username][0] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["username"]  = username
                    st.session_state["user_role"] = USERS[username][1]
                    st.session_state["user_name"] = USERS[username][2]
                    st.rerun()
                else: st.error("❌ Wrong password")
            else: st.error("❌ Username not found")
        st.markdown("""
        <div style='margin-top:1.2rem;background:#080f1e;border:1px solid #112240;
                    border-radius:10px;padding:1rem;'>
          <div style='font-family:"IBM Plex Mono",monospace;font-size:0.6rem;
                      color:#4a6fa5;text-transform:uppercase;letter-spacing:1px;
                      margin-bottom:0.6rem;'>Demo Credentials</div>
          <div style='font-family:"IBM Plex Mono",monospace;font-size:0.7rem;
                      color:#4a6fa5;line-height:2.2;'>
            👨‍⚕️ drfatima &nbsp;&nbsp;&nbsp;/ doctor123<br>
            🧾 reception1 &nbsp;/ recep123<br>
            📊 director &nbsp;&nbsp;&nbsp;/ director123
          </div>
        </div>
        <div style='text-align:center;margin-top:1rem;font-family:"IBM Plex Mono",
                    monospace;font-size:0.6rem;color:#1a3058;'>
          MedCore v2.0 · SSUET BME · 2026</div>
        """, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if not st.session_state["logged_in"]:
    show_login()
    st.stop()

user_role = st.session_state["user_role"]
user_name = st.session_state["user_name"]
username  = st.session_state["username"]

# ─────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');
:root{--bg:#04080f;--surface:#080f1e;--card:#0b1425;--border:#112240;--border2:#1a3058;
  --cyan:#00e5ff;--green:#00ff9d;--red:#ff3d6b;--amber:#ffb700;--purple:#a78bfa;--text:#ccd6f6;--muted:#4a6fa5;}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important;}
[data-testid="stSidebar"]{background:#060d1b!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
#MainMenu,footer,header{visibility:hidden;}[data-testid="stToolbar"]{display:none;}
[data-testid="stMetric"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:12px!important;padding:1rem!important;}
[data-testid="stMetricValue"]{font-family:'IBM Plex Mono',monospace!important;color:var(--cyan)!important;font-size:1.4rem!important;}
[data-testid="stMetricLabel"]{color:var(--muted)!important;font-size:0.73rem!important;}
.stButton>button{background:linear-gradient(135deg,#1a3058,#112240)!important;color:var(--cyan)!important;border:1px solid var(--border2)!important;border-radius:8px!important;font-family:'IBM Plex Mono',monospace!important;font-size:0.78rem!important;}
.stButton>button:hover{background:linear-gradient(135deg,#00e5ff22,#00e5ff11)!important;border-color:var(--cyan)!important;}
[data-testid="stSelectbox"]>div>div{background:var(--card)!important;border-color:var(--border)!important;color:var(--text)!important;border-radius:8px!important;}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input{background:var(--card)!important;border-color:var(--border)!important;color:var(--text)!important;border-radius:8px!important;}
[data-testid="stTabs"] [role="tablist"]{background:var(--surface)!important;border-radius:10px!important;padding:4px!important;border:1px solid var(--border)!important;}
[data-testid="stTabs"] [role="tab"]{color:var(--muted)!important;font-family:'IBM Plex Mono',monospace!important;font-size:0.75rem!important;border-radius:7px!important;}
[data-testid="stTabs"] [role="tab"][aria-selected="true"]{background:rgba(0,229,255,0.12)!important;color:var(--cyan)!important;}
hr{border-color:var(--border)!important;}
.mc-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:0.8rem;position:relative;overflow:hidden;}
.mc-card-top::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.mc-card-top.cyan::before{background:linear-gradient(90deg,var(--cyan),transparent);}
.mc-card-top.green::before{background:linear-gradient(90deg,var(--green),transparent);}
.mc-card-top.red::before{background:linear-gradient(90deg,var(--red),transparent);}
.mc-card-top.amber::before{background:linear-gradient(90deg,var(--amber),transparent);}
.mc-card-top.purple::before{background:linear-gradient(90deg,var(--purple),transparent);}
.mc-label{font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:var(--muted);text-transform:uppercase;letter-spacing:2px;margin-bottom:0.5rem;}
.badge{display:inline-block;padding:2px 10px;border-radius:20px;font-size:0.65rem;font-family:'IBM Plex Mono',monospace;font-weight:700;letter-spacing:1px;text-transform:uppercase;}
.badge-green{background:rgba(0,255,157,0.12);color:#00ff9d;border:1px solid rgba(0,255,157,0.25);}
.badge-amber{background:rgba(255,183,0,0.12);color:#ffb700;border:1px solid rgba(255,183,0,0.25);}
.badge-red{background:rgba(255,61,107,0.12);color:#ff3d6b;border:1px solid rgba(255,61,107,0.25);}
.badge-cyan{background:rgba(0,229,255,0.12);color:#00e5ff;border:1px solid rgba(0,229,255,0.25);}
.badge-purple{background:rgba(167,139,250,0.12);color:#a78bfa;border:1px solid rgba(167,139,250,0.25);}
.section-header{font-family:'IBM Plex Mono',monospace;font-size:0.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:2px;padding:0.8rem 0 0.4rem;border-bottom:1px solid var(--border);margin-bottom:0.8rem;}
.vital-row{display:flex;justify-content:space-between;align-items:center;padding:0.5rem 0;border-bottom:1px solid var(--border);font-size:0.85rem;}
.alert-row{display:flex;align-items:flex-start;gap:0.8rem;padding:0.65rem 0;border-bottom:1px solid var(--border);}
.alert-dot{width:8px;height:8px;border-radius:50%;margin-top:5px;flex-shrink:0;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HOSPITAL DATA
# ─────────────────────────────────────────
PATIENTS = [
    {"id":"PKR-0312","name":"Bilal Khan","age":58,"gender":"M","dept":"Ophthalmology","status":"Critical","wait":5,"bp":"158/96","hr":88,"spo2":96,"dx":"Proliferative DR","risk":"High"},
    {"id":"PKR-0847","name":"Ayesha Noor","age":54,"gender":"F","dept":"Ophthalmology","status":"Waiting","wait":12,"bp":"138/88","hr":78,"spo2":98,"dx":"Mild DR","risk":"Medium"},
    {"id":"PKR-0561","name":"Sana Raza","age":42,"gender":"F","dept":"Cardiology","status":"In Consult","wait":0,"bp":"120/78","hr":72,"spo2":99,"dx":"Normal ECG","risk":"Low"},
    {"id":"PKR-0223","name":"Ahmed Tariq","age":61,"gender":"M","dept":"Ophthalmology","status":"Waiting","wait":25,"bp":"145/92","hr":82,"spo2":97,"dx":"Moderate DR","risk":"High"},
    {"id":"PKR-0115","name":"Fatima Sheikh","age":35,"gender":"F","dept":"General OPD","status":"Waiting","wait":18,"bp":"118/75","hr":68,"spo2":99,"dx":"Hypertension","risk":"Low"},
    {"id":"PKR-0678","name":"Usman Ali","age":47,"gender":"M","dept":"Cardiology","status":"Critical","wait":2,"bp":"170/105","hr":102,"spo2":94,"dx":"Arrhythmia","risk":"High"},
    {"id":"PKR-0901","name":"Zara Malik","age":29,"gender":"F","dept":"General OPD","status":"Waiting","wait":8,"bp":"115/72","hr":70,"spo2":99,"dx":"Migraine","risk":"Low"},
    {"id":"PKR-1023","name":"Hassan Rauf","age":66,"gender":"M","dept":"ICU","status":"Critical","wait":0,"bp":"190/110","hr":110,"spo2":91,"dx":"Acute MI","risk":"High"},
]
DR_SCANS = [
    {"pid":"PKR-0312","name":"Bilal Khan","time":"14:22","grade":"Severe","confidence":"94%","flag":"🔴"},
    {"pid":"PKR-0847","name":"Ayesha Noor","time":"13:55","grade":"Mild","confidence":"89%","flag":"🟡"},
    {"pid":"PKR-0561","name":"Sana Raza","time":"13:10","grade":"No DR","confidence":"97%","flag":"🟢"},
    {"pid":"PKR-0223","name":"Ahmed Tariq","time":"12:44","grade":"Moderate","confidence":"91%","flag":"🟠"},
    {"pid":"PKR-1002","name":"Zara Malik","time":"12:01","grade":"No DR","confidence":"96%","flag":"🟢"},
    {"pid":"PKR-0789","name":"Imran Baig","time":"11:30","grade":"Proliferative","confidence":"93%","flag":"🔴"},
]
APPOINTMENTS = [
    {"token":"T-001","name":"Bilal Khan","time":"09:00","dept":"Ophthalmology","type":"Follow-up","status":"Done"},
    {"token":"T-002","name":"Sana Raza","time":"09:30","dept":"Cardiology","type":"New","status":"In Consult"},
    {"token":"T-003","name":"Ayesha Noor","time":"10:00","dept":"Ophthalmology","type":"Screening","status":"Waiting"},
    {"token":"T-004","name":"Ahmed Tariq","time":"10:30","dept":"Ophthalmology","type":"Follow-up","status":"Waiting"},
    {"token":"T-005","name":"Fatima Sheikh","time":"11:00","dept":"General OPD","type":"New","status":"Waiting"},
    {"token":"T-006","name":"Usman Ali","time":"11:30","dept":"Cardiology","type":"Emergency","status":"Critical"},
    {"token":"T-007","name":"Zara Malik","time":"12:00","dept":"Ophthalmology","type":"Screening","status":"Scheduled"},
    {"token":"T-008","name":"Hassan Rauf","time":"12:30","dept":"General OPD","type":"New","status":"Scheduled"},
]
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
MONTHLY_PATIENTS  = [1240,1380,1290,1520,1610,1480,1390,1560,1720,1840,1780,1950]
MONTHLY_REVENUE   = [820,940,880,1050,1120,1080,990,1150,1280,1350,1310,1450]
MONTHLY_COST      = [610,680,650,720,780,710,680,790,850,920,880,970]
MONTHLY_SURGERIES = [42,55,48,61,70,65,58,72,80,88,84,95]
DEPT_NAMES   = ["Ophthalmology","Cardiology","General OPD","ICU","Surgery","Lab","Pharmacy"]
DEPT_PTS     = [380,220,520,45,120,280,180]
DEPT_REV     = [420,380,280,850,620,180,120]
DEPT_SAT     = [4.7,4.5,4.2,4.8,4.6,4.3,4.1]
DISEASES     = ["Diabetic Retinopathy","Hypertension","Cardiac Arrhythmia","Glaucoma",
                "Cataracts","Heart Failure","Diabetes Type 2","Pneumonia","Fractures","Appendicitis"]
DISEASE_CASES= [247,312,98,145,203,76,289,134,87,45]
DISEASE_TREND= [12,-3,5,8,-2,3,7,-8,2,-5]
BED_WARDS    = ["General","Cardiology","Ophthalmology","ICU","Surgery","Pediatrics"]
BED_TOTAL    = [40,20,15,10,18,12]
BED_OCC      = [32,16,11,9,14,8]
STAFF_ROLES  = ["Doctors","Nurses","Technicians","Admin","Support"]
STAFF_TOTAL  = [24,48,18,12,20]
STAFF_DUTY   = [18,36,14,8,16]
DEPT_COLORS  = ['#00e5ff','#a78bfa','#00ff9d','#ff3d6b','#ffb700','#3b82f6','#f97316']

def make_ecg():
    t = np.linspace(0,4*np.pi,400); ecg = np.zeros(400)
    for i,x in enumerate(t):
        n = (x%(2*np.pi))/(2*np.pi)
        if 0.05<n<0.15:    ecg[i]=np.sin((n-.05)/.1*np.pi)*.2
        elif .22<n<.24:    ecg[i]=(n-.22)/.02*.15
        elif .24<=n<.265:  ecg[i]=-(n-.24)/.025*1.8
        elif .265<=n<.29:  ecg[i]=-1.8+(n-.265)/.025*2.
        elif .29<=n<.31:   ecg[i]=.2-(n-.29)/.02*.2
        elif .38<n<.55:    ecg[i]=-np.sin((n-.38)/.17*np.pi)*.35
    return t, ecg+np.random.normal(0,.015,400)

PL   = dict(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(11,20,37,0.6)',
            font=dict(family='DM Sans',color='#4a6fa5',size=11),
            margin=dict(l=10,r=10,t=35,b=10))
AXIS = dict(gridcolor='#112240',linecolor='#112240',
            tickfont=dict(family='IBM Plex Mono',size=10))

now = datetime.now()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1rem 0 0.5rem;'>
      <div style='font-size:2rem'>🏥</div>
      <div style='font-family:"IBM Plex Mono",monospace;font-size:1.1rem;
                  background:linear-gradient(90deg,#00e5ff,#00ff9d);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  font-weight:700;letter-spacing:2px;'>MedCore</div>
      <div style='font-size:0.6rem;color:#4a6fa5;letter-spacing:2px;
                  text-transform:uppercase;margin-top:0.2rem;'>v2.0 · Hospital Intelligence</div>
    </div><hr style='border-color:#112240;margin:0.8rem 0;'/>
    """, unsafe_allow_html=True)

    view = ROLE_VIEW.get(user_role,"👨‍⚕️ Doctor View")

    st.markdown(f"""
    <div style='background:#0b1425;border:1px solid #112240;border-radius:10px;
                padding:0.8rem;margin-bottom:1rem;text-align:center;'>
      <div style='font-size:1.5rem;'>{ROLE_EMOJI.get(user_role,"👤")}</div>
      <div style='font-size:0.85rem;font-weight:600;color:#ccd6f6;margin-top:0.3rem;'>{user_name}</div>
      <div style='font-family:"IBM Plex Mono",monospace;font-size:0.62rem;color:#4a6fa5;
                  text-transform:uppercase;letter-spacing:1px;margin-top:0.2rem;'>{user_role}</div>
    </div>""", unsafe_allow_html=True)

    if st.button("🚪 Logout", use_container_width=True):
        for k in ["logged_in","username","user_role","user_name"]:
            st.session_state[k] = "" if k!="logged_in" else False
        st.rerun()

    st.markdown("<div class='section-header'>Live Stats</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-family:"IBM Plex Mono",monospace;font-size:0.72rem;color:#4a6fa5;line-height:2.2;'>
    🕐 {now.strftime('%H:%M')} · {now.strftime('%d %b %Y')}<br>
    👥 Today: <span style='color:#00e5ff;font-weight:700;'>47</span> patients<br>
    🛏 Beds: <span style='color:#00ff9d;font-weight:700;'>12</span> available<br>
    🔴 Critical: <span style='color:#ff3d6b;font-weight:700;'>3</span> cases<br>
    💊 Pharmacy: <span style='color:#ffb700;font-weight:700;'>Open</span><br>
    🧪 Lab: <span style='color:#00ff9d;font-weight:700;'>Open</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-header' style='margin-top:1rem;'>Departments</div>",
                unsafe_allow_html=True)
    for icon,name,stat in [("👁","Ophthalmology","38 pts"),("💓","Cardiology","22 pts"),
                            ("🏥","General OPD","52 pts"),("🚨","ICU","9/10 beds"),
                            ("🔪","Surgery","3 today"),("🧪","Lab","Open"),("💊","Pharmacy","Open")]:
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;
                    padding:0.32rem 0.2rem;border-bottom:1px solid #080f1e;'>
          <div style='font-size:0.76rem;color:#4a6fa5;'>{icon} {name}</div>
          <div style='font-family:"IBM Plex Mono",monospace;font-size:0.6rem;color:#1a3058;'>{stat}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='font-size:0.6rem;color:#1a3058;font-family:"IBM Plex Mono",monospace;
                text-align:center;padding:1rem 0 0.3rem;'>
    MedCore v2.0 · SSUET BME · HOD Pitch Ready</div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# VIEW 1: DOCTOR
# ─────────────────────────────────────────
if "Doctor" in view:
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1.2rem;'>
      <div style='font-size:1.5rem'>👨‍⚕️</div>
      <div><div style='font-family:"IBM Plex Mono",monospace;font-size:1.1rem;
                       color:#00e5ff;font-weight:700;'>Doctor Dashboard</div>
           <div style='font-size:0.75rem;color:#4a6fa5;'>{user_name} · {now.strftime('%d %b %Y')}</div>
      </div>
      <div style='margin-left:auto;'><span class='badge badge-green'>● On Duty</span></div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.metric("👥 My Queue","8","2 critical")
    with c2: st.metric("✅ Seen Today","18","+3 vs yesterday")
    with c3: st.metric("🚨 Alerts","5","↑ urgent")
    with c4: st.metric("⏱ Avg Wait","14 min","-2 min")
    with c5: st.metric("📋 Reports Due","3","")
    st.markdown("---")

    cl,cr = st.columns([1.4,1])
    with cl:
        st.markdown("<div class='section-header'>Patient Queue — Today</div>",
                    unsafe_allow_html=True)
        for p in PATIENTS:
            rc = {"High":"red","Medium":"amber","Low":"green"}[p["risk"]]
            sc = {"Critical":"badge-red","Waiting":"badge-amber",
                  "In Consult":"badge-cyan"}[p["status"]]
            st.markdown(f"""
            <div class='mc-card mc-card-top {rc}'>
              <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:0.5rem;'>
                <div>
                  <div style='font-weight:600;font-size:0.9rem;'>{p["name"]}
                    <span style='font-family:"IBM Plex Mono",monospace;font-size:0.67rem;
                                 color:#4a6fa5;margin-left:0.5rem;'>{p["id"]}</span></div>
                  <div style='font-size:0.7rem;color:#4a6fa5;margin-top:0.12rem;'>
                    {p["dept"]} · {p["gender"]}, {p["age"]}yr</div>
                </div>
                <div style='text-align:right;'>
                  <span class='badge {sc}'>{p["status"]}</span><br>
                  <span style='font-family:"IBM Plex Mono",monospace;font-size:0.6rem;color:#4a6fa5;'>
                    {"⏱ "+str(p["wait"])+"m wait" if p["wait"]>0 else "● In Room"}</span>
                </div>
              </div>
              <div style='display:flex;gap:1rem;flex-wrap:wrap;font-family:"IBM Plex Mono",monospace;font-size:0.7rem;'>
                <span>BP:<span style='color:#ccd6f6;margin-left:3px;'>{p["bp"]}</span></span>
                <span>HR:<span style='color:#ccd6f6;margin-left:3px;'>{p["hr"]}</span></span>
                <span>SpO₂:<span style='color:#00ff9d;margin-left:3px;'>{p["spo2"]}%</span></span>
                <span>Dx:<span style='color:#00e5ff;margin-left:3px;'>{p["dx"]}</span></span>
                <span class='badge badge-{rc}' style='margin-left:auto;'>{p["risk"]} Risk</span>
              </div>
            </div>""", unsafe_allow_html=True)

    with cr:
        st.markdown("<div class='section-header'>ECG Monitor — Lead II</div>",
                    unsafe_allow_html=True)
        t,ecg = make_ecg()
        fig_e = go.Figure()
        fig_e.add_trace(go.Scatter(x=t,y=ecg,mode='lines',
            line=dict(color='#00ff9d',width=1.5),
            fill='tozeroy',fillcolor='rgba(0,255,157,0.04)'))
        el=dict(PL); el['xaxis']=dict(showticklabels=False,gridcolor='#112240')
        el['yaxis']=dict(showticklabels=False,gridcolor='#112240')
        fig_e.update_layout(**el,height=155,showlegend=False,
            title=dict(text='Lead II · 72 BPM · NSR',font=dict(color='#4a6fa5',size=10)))
        st.plotly_chart(fig_e,use_container_width=True,config={'displayModeBar':False})

        st.markdown("<div class='section-header'>Patient Vitals</div>",unsafe_allow_html=True)
        for icon,label,val,c in [("💓","Heart Rate","78 BPM","#00ff9d"),
            ("🩸","Blood Pressure","138/88 mmHg","#ffb700"),
            ("💧","SpO₂","98%","#00ff9d"),("🌡️","Temperature","36.7°C","#00ff9d"),
            ("🫁","Resp. Rate","16/min","#00ff9d")]:
            st.markdown(f"""
            <div class='vital-row'>
              <div style='font-size:0.8rem;'>{icon} {label}</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.85rem;
                          font-weight:700;color:{c};'>{val}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div class='section-header' style='margin-top:0.8rem;'>Alerts</div>",
                    unsafe_allow_html=True)
        for title,sub,time,color in [
            ("Proliferative DR — PKR-0312","Urgent referral needed","2m","red"),
            ("Elevated BP — PKR-0678","BP: 170/105 mmHg","8m","amber"),
            ("ICU Alert — PKR-1023","SpO₂ dropped to 91%","15m","red"),
            ("ECG Normal — PKR-0561","NSR confirmed","41m","green")]:
            st.markdown(f"""
            <div class='alert-row'>
              <div class='alert-dot' style='background:var(--{color});box-shadow:0 0 6px var(--{color});'></div>
              <div style='flex:1;'>
                <div style='font-size:0.78rem;font-weight:600;'>{title}</div>
                <div style='font-size:0.67rem;color:#4a6fa5;margin-top:0.1rem;'>{sub}</div>
              </div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.6rem;color:#1a3058;'>{time}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div class='section-header' style='margin-top:0.8rem;'>Quick Actions</div>",
                    unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            st.button("📋 Prescription",use_container_width=True)
            st.button("🔬 Lab Order",use_container_width=True)
        with c2:
            st.button("📨 Refer",use_container_width=True)
            st.button("📄 Report",use_container_width=True)

# ─────────────────────────────────────────
# VIEW 2: RECEPTION
# ─────────────────────────────────────────
elif "Reception" in view:
    st.markdown("""
    <div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1.2rem;'>
      <div style='font-size:1.5rem'>🧾</div>
      <div><div style='font-family:"IBM Plex Mono",monospace;font-size:1.1rem;
                       color:#ffb700;font-weight:700;'>Reception & Admin</div>
           <div style='font-size:0.75rem;color:#4a6fa5;'>OPD Reception · Ground Floor</div>
      </div></div>""", unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("🎫 Tokens","47","+5 today")
    with c2: st.metric("⏳ In Queue","12","3 critical")
    with c3: st.metric("✅ Completed","31","66%")
    with c4: st.metric("🚨 Emergency","4","↑ 2 new")
    st.markdown("---")

    t1,t2,t3=st.tabs(["📋 Queue","➕ Register","📅 Schedule"])
    with t1:
        st.markdown("<div class='section-header'>Today's Appointment Queue</div>",unsafe_allow_html=True)
        sc={"Done":"badge-green","In Consult":"badge-cyan","Waiting":"badge-amber",
            "Critical":"badge-red","Scheduled":"badge-purple"}
        for apt in APPOINTMENTS:
            st.markdown(f"""
            <div class='mc-card' style='display:flex;align-items:center;gap:1rem;padding:0.85rem 1.2rem;'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:1rem;
                          font-weight:700;color:#00e5ff;min-width:50px;'>{apt["token"]}</div>
              <div style='flex:1;'>
                <div style='font-weight:600;font-size:0.88rem;'>{apt["name"]}</div>
                <div style='font-size:0.7rem;color:#4a6fa5;margin-top:0.1rem;'>
                  {apt["dept"]} · {apt["type"]}</div>
              </div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.78rem;color:#4a6fa5;'>{apt["time"]}</div>
              <span class='badge {sc.get(apt["status"],"badge-cyan")}'>{apt["status"]}</span>
            </div>""", unsafe_allow_html=True)

    with t2:
        st.markdown("<div class='section-header'>New Patient Registration</div>",unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            st.text_input("Full Name",placeholder="Patient full name")
            st.text_input("CNIC",placeholder="42101-XXXXXXX-X")
            st.selectbox("Gender",["Male","Female","Other"])
            st.text_input("Contact",placeholder="+92-3XX-XXXXXXX")
        with c2:
            st.number_input("Age",min_value=1,max_value=120,value=30)
            st.selectbox("Department",["Ophthalmology","Cardiology","General OPD","ICU","Surgery"])
            st.selectbox("Visit Type",["New Patient","Follow-up","Emergency","Screening"])
            st.text_input("Referred By",placeholder="Doctor name (optional)")
        st.text_input("Chief Complaint",placeholder="Brief symptoms")
        c1,c2,_=st.columns([1,1,2])
        with c1: st.button("✅ Register & Issue Token",use_container_width=True)
        with c2: st.button("🖨 Print Token",use_container_width=True)

    with t3:
        st.markdown("<div class='section-header'>Weekly Slot Utilization</div>",unsafe_allow_html=True)
        days7=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        fig_s=go.Figure()
        fig_s.add_trace(go.Bar(name='Booked',x=days7,y=[18,22,19,26,24,10],
            marker_color='#00e5ff',marker_opacity=0.8))
        fig_s.add_trace(go.Bar(name='Available',x=days7,y=[12,8,11,4,6,20],
            marker_color='#1a3058'))
        sl=dict(PL); sl['xaxis']=AXIS; sl['yaxis']=AXIS
        fig_s.update_layout(**sl,height=260,barmode='stack',
            legend=dict(font=dict(color='#4a6fa5',size=10),bgcolor='rgba(0,0,0,0)'),
            title=dict(text='Slot Utilization This Week',font=dict(color='#4a6fa5',size=11)))
        st.plotly_chart(fig_s,use_container_width=True,config={'displayModeBar':False})

# ─────────────────────────────────────────
# VIEW 3: MANAGEMENT — FULLY ENHANCED
# ─────────────────────────────────────────
elif "Management" in view:
    st.markdown("""
    <div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1.2rem;'>
      <div style='font-size:1.5rem'>📊</div>
      <div><div style='font-family:"IBM Plex Mono",monospace;font-size:1.1rem;
                       color:#a78bfa;font-weight:700;'>Management Dashboard</div>
           <div style='font-size:0.75rem;color:#4a6fa5;'>Hospital Director · Full Analytics</div>
      </div></div>""", unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6=st.columns(6)
    with c1: st.metric("💰 Revenue Apr","1.45M PKR","+15%")
    with c2: st.metric("👥 Patients Apr","1,950","+12%")
    with c3: st.metric("🛏 Bed Occ.","74%","+6%")
    with c4: st.metric("👨‍⚕️ Staff On","34","of 48")
    with c5: st.metric("🔪 Surgeries","95","+8 this month")
    with c6: st.metric("⭐ Rating","4.6/5","+0.2")
    st.markdown("---")

    t1,t2,t3,t4=st.tabs(["📈 Patient & Revenue","🏥 Departments","🦠 Disease Analytics","👥 Staff & Beds"])

    with t1:
        cl,cr=st.columns(2)
        with cl:
            st.markdown("<div class='section-header'>12-Month Patient Volume</div>",unsafe_allow_html=True)
            z=np.polyfit(range(12),MONTHLY_PATIENTS,1); p=np.poly1d(z)
            fig_pv=go.Figure()
            fig_pv.add_trace(go.Scatter(x=MONTHS,y=MONTHLY_PATIENTS,mode='lines+markers',
                name='Patients',line=dict(color='#00e5ff',width=2.5),marker=dict(size=7),
                fill='tozeroy',fillcolor='rgba(0,229,255,0.07)'))
            fig_pv.add_trace(go.Scatter(x=MONTHS,y=[int(p(i)) for i in range(12)],
                mode='lines',name='Trend',line=dict(color='#a78bfa',width=1.5,dash='dot')))
            pvl=dict(PL); pvl['xaxis']=AXIS; pvl['yaxis']=dict(**AXIS,title='Patients')
            fig_pv.update_layout(**pvl,height=230,
                legend=dict(font=dict(color='#4a6fa5',size=9),bgcolor='rgba(0,0,0,0)',orientation='h',y=1.12),
                title=dict(text='Monthly Patient Visits 2025/26',font=dict(color='#4a6fa5',size=11)))
            st.plotly_chart(fig_pv,use_container_width=True,config={'displayModeBar':False})

        with cr:
            st.markdown("<div class='section-header'>Revenue vs Cost vs Profit</div>",unsafe_allow_html=True)
            profit=[r-c for r,c in zip(MONTHLY_REVENUE,MONTHLY_COST)]
            fig_rv=go.Figure()
            fig_rv.add_trace(go.Bar(x=MONTHS,y=MONTHLY_REVENUE,name='Revenue',
                marker_color='rgba(0,255,157,0.75)',width=0.3))
            fig_rv.add_trace(go.Bar(x=MONTHS,y=MONTHLY_COST,name='Cost',
                marker_color='rgba(255,61,107,0.6)',width=0.3))
            fig_rv.add_trace(go.Scatter(x=MONTHS,y=profit,name='Profit',
                mode='lines+markers',line=dict(color='#ffb700',width=2,dash='dot'),marker=dict(size=6)))
            rvl=dict(PL); rvl['xaxis']=AXIS; rvl['yaxis']=dict(**AXIS,ticksuffix='K PKR')
            fig_rv.update_layout(**rvl,height=230,barmode='group',
                legend=dict(font=dict(color='#4a6fa5',size=9),bgcolor='rgba(0,0,0,0)',orientation='h',y=1.12),
                title=dict(text='Financial Performance 2025/26',font=dict(color='#4a6fa5',size=11)))
            st.plotly_chart(fig_rv,use_container_width=True,config={'displayModeBar':False})

        st.markdown("<div class='section-header'>Monthly Surgical Procedures</div>",unsafe_allow_html=True)
        fig_sg=go.Figure()
        fig_sg.add_trace(go.Bar(x=MONTHS,y=MONTHLY_SURGERIES,
            marker=dict(color=MONTHLY_SURGERIES,
                        colorscale=[[0,'#1a3058'],[0.5,'#00e5ff'],[1,'#00ff9d']],showscale=False),
            text=MONTHLY_SURGERIES,textposition='outside',
            textfont=dict(family='IBM Plex Mono',size=9,color='#4a6fa5')))
        sgl=dict(PL); sgl['xaxis']=AXIS; sgl['yaxis']=dict(**AXIS,title='Procedures')
        fig_sg.update_layout(**sgl,height=185,showlegend=False,
            title=dict(text='Surgical Volume Trend',font=dict(color='#4a6fa5',size=11)))
        st.plotly_chart(fig_sg,use_container_width=True,config={'displayModeBar':False})

    with t2:
        cl,cr=st.columns([1.2,1])
        with cl:
            st.markdown("<div class='section-header'>Patients by Department</div>",unsafe_allow_html=True)
            fig_dp=go.Figure()
            fig_dp.add_trace(go.Bar(x=DEPT_NAMES,y=DEPT_PTS,marker_color=DEPT_COLORS,
                marker_opacity=0.85,text=DEPT_PTS,textposition='outside',
                textfont=dict(family='IBM Plex Mono',size=9,color='#4a6fa5')))
            dpl=dict(PL); dpl['xaxis']=dict(**AXIS,tickangle=-20); dpl['yaxis']=dict(**AXIS,title='Patients')
            fig_dp.update_layout(**dpl,height=240,showlegend=False,
                title=dict(text='Department Patient Load — April 2026',font=dict(color='#4a6fa5',size=11)))
            st.plotly_chart(fig_dp,use_container_width=True,config={'displayModeBar':False})

            st.markdown("<div class='section-header'>Revenue by Department</div>",unsafe_allow_html=True)
            fig_dr2=go.Figure(go.Bar(x=DEPT_REV,y=DEPT_NAMES,orientation='h',
                marker=dict(color=DEPT_COLORS,opacity=0.8),
                text=[f"{v}K" for v in DEPT_REV],textposition='outside',
                textfont=dict(family='IBM Plex Mono',size=9,color='#4a6fa5')))
            # FIX: set margin inside dict to avoid duplicate keyword error
            drl=dict(PL)
            drl['margin']=dict(l=10,r=40,t=30,b=10)
            drl['xaxis']=dict(**AXIS,ticksuffix='K')
            drl['yaxis']=AXIS
            fig_dr2.update_layout(**drl,height=230,showlegend=False,
                title=dict(text='Revenue Contribution (000 PKR)',font=dict(color='#4a6fa5',size=11)))
            st.plotly_chart(fig_dr2,use_container_width=True,config={'displayModeBar':False})

        with cr:
            st.markdown("<div class='section-header'>Patient Share</div>",unsafe_allow_html=True)
            fig_pie=go.Figure(go.Pie(labels=DEPT_NAMES,values=DEPT_PTS,hole=0.55,
                marker=dict(colors=DEPT_COLORS),textfont=dict(family='IBM Plex Mono',size=9)))
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                showlegend=True,height=220,margin=dict(l=0,r=0,t=10,b=10),
                legend=dict(font=dict(color='#4a6fa5',size=9),bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fig_pie,use_container_width=True,config={'displayModeBar':False})

            st.markdown("<div class='section-header'>Patient Satisfaction</div>",unsafe_allow_html=True)
            for dept,score in zip(DEPT_NAMES,DEPT_SAT):
                pct=(score/5)*100
                sc='#00ff9d' if score>=4.5 else '#ffb700' if score>=4.0 else '#ff3d6b'
                st.markdown(f"""
                <div style='display:flex;align-items:center;gap:0.6rem;padding:0.35rem 0;border-bottom:1px solid #112240;'>
                  <div style='font-size:0.7rem;color:#4a6fa5;min-width:95px;'>{dept[:11]}</div>
                  <div style='flex:1;height:5px;background:#112240;border-radius:3px;overflow:hidden;'>
                    <div style='height:100%;width:{pct}%;background:linear-gradient(90deg,{sc}88,{sc});border-radius:3px;'></div>
                  </div>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.72rem;font-weight:700;color:{sc};min-width:30px;text-align:right;'>{score}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<div class='section-header' style='margin-top:0.8rem;'>KPIs</div>",unsafe_allow_html=True)
            for icon,label,val,status,sc in [
                ("🛏","Avg Stay","2.4 days","Normal","#00ff9d"),
                ("⏱","Avg Wait OPD","18 min","High","#ff3d6b"),
                ("💊","Rx Fulfillment","94%","Good","#00ff9d"),
                ("🔄","Readmission","6.2%","Watch","#ffb700"),
                ("🤖","AI Adoption","67%","Growing","#00e5ff")]:
                st.markdown(f"""
                <div class='vital-row'>
                  <div style='font-size:0.78rem;'>{icon} {label}</div>
                  <div style='text-align:right;'>
                    <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;font-weight:700;color:#ccd6f6;'>{val}</div>
                    <div style='font-size:0.6rem;color:{sc};'>{status}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

    with t3:
        cl,cr=st.columns([1.3,1])
        with cl:
            st.markdown("<div class='section-header'>Top 10 Diseases — April 2026</div>",unsafe_allow_html=True)
            sidx=np.argsort(DISEASE_CASES)[::-1]
            sdis=[DISEASE_CASES[i] for i in sidx]; sdnames=[DISEASES[i] for i in sidx]
            bcolors=['#ff3d6b' if c>200 else '#ffb700' if c>100 else '#00e5ff' for c in sdis]
            fig_dis=go.Figure(go.Bar(x=sdis,y=sdnames,orientation='h',
                marker_color=bcolors,marker_opacity=0.85,
                text=sdis,textposition='outside',
                textfont=dict(family='IBM Plex Mono',size=9,color='#4a6fa5')))
            # FIX: set margin inside dict
            disl=dict(PL)
            disl['margin']=dict(l=10,r=40,t=30,b=10)
            disl['xaxis']=dict(**AXIS,title='Cases')
            disl['yaxis']=AXIS
            fig_dis.update_layout(**disl,height=320,showlegend=False,
                title=dict(text='Case Frequency by Disease',font=dict(color='#4a6fa5',size=11)))
            st.plotly_chart(fig_dis,use_container_width=True,config={'displayModeBar':False})

        with cr:
            st.markdown("<div class='section-header'>Month-on-Month Trend</div>",unsafe_allow_html=True)
            for dis,trnd in zip(DISEASES,DISEASE_TREND):
                color='#00ff9d' if trnd<0 else '#ff3d6b' if trnd>8 else '#ffb700'
                arrow="↓" if trnd<0 else "↑"
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;align-items:center;
                            padding:0.42rem 0;border-bottom:1px solid #112240;'>
                  <div style='font-size:0.73rem;color:#4a6fa5;'>{dis[:22]}</div>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.8rem;
                              font-weight:700;color:{color};'>{arrow} {abs(trnd)}%</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("""
            <div style='margin-top:1rem;background:rgba(255,61,107,0.06);border:1px solid rgba(255,61,107,0.2);
                        border-radius:8px;padding:0.8rem;font-size:0.7rem;color:#ff3d6b;
                        font-family:"IBM Plex Mono",monospace;line-height:1.8;'>
            ⚠️ HIGH PRIORITY<br>Diabetic Retinopathy +12%<br>
            Diabetes Type 2 +7%<br>Glaucoma +8%<br>
            → Scale AI Screening immediately
            </div>""", unsafe_allow_html=True)

        st.markdown("<div class='section-header' style='margin-top:0.5rem;'>DR Cases — 12 Month Trend</div>",
                    unsafe_allow_html=True)
        dr_m=[18,22,19,28,32,29,25,35,41,48,52,58]
        fig_drt=go.Figure()
        fig_drt.add_trace(go.Scatter(x=MONTHS,y=dr_m,mode='lines+markers',
            line=dict(color='#ff3d6b',width=2.5),marker=dict(size=8,color='#ff3d6b'),
            fill='tozeroy',fillcolor='rgba(255,61,107,0.07)',name='DR Cases'))
        drtl=dict(PL); drtl['xaxis']=AXIS; drtl['yaxis']=dict(**AXIS,title='Cases')
        fig_drt.update_layout(**drtl,height=185,showlegend=False,
            title=dict(text='DR Cases Rising — Screening Scale-Up Needed',
                       font=dict(color='#ff3d6b',size=11)))
        st.plotly_chart(fig_drt,use_container_width=True,config={'displayModeBar':False})

    with t4:
        cl,cr=st.columns(2)
        with cl:
            st.markdown("<div class='section-header'>Bed Occupancy by Ward</div>",unsafe_allow_html=True)
            occ_pct=[o/t*100 for o,t in zip(BED_OCC,BED_TOTAL)]
            fig_bed=go.Figure()
            fig_bed.add_trace(go.Bar(name='Occupied',x=BED_WARDS,y=BED_OCC,
                marker_color=['#ff3d6b' if p>85 else '#ffb700' if p>70 else '#00ff9d' for p in occ_pct],
                marker_opacity=0.85,text=[f"{int(p)}%" for p in occ_pct],textposition='outside',
                textfont=dict(family='IBM Plex Mono',size=9,color='#4a6fa5')))
            fig_bed.add_trace(go.Bar(name='Available',x=BED_WARDS,
                y=[t-o for t,o in zip(BED_TOTAL,BED_OCC)],marker_color='#1a3058'))
            bl=dict(PL); bl['xaxis']=AXIS; bl['yaxis']=dict(**AXIS,title='Beds')
            fig_bed.update_layout(**bl,height=250,barmode='stack',
                legend=dict(font=dict(color='#4a6fa5',size=9),bgcolor='rgba(0,0,0,0)'),
                title=dict(text='Bed Occupancy — ICU at 90%',font=dict(color='#4a6fa5',size=11)))
            st.plotly_chart(fig_bed,use_container_width=True,config={'displayModeBar':False})

        with cr:
            st.markdown("<div class='section-header'>Staff Distribution</div>",unsafe_allow_html=True)
            fig_st=go.Figure()
            fig_st.add_trace(go.Bar(name='On Duty',x=STAFF_ROLES,y=STAFF_DUTY,
                marker_color='#00e5ff',marker_opacity=0.8))
            fig_st.add_trace(go.Bar(name='Off Duty',x=STAFF_ROLES,
                y=[t-o for t,o in zip(STAFF_TOTAL,STAFF_DUTY)],marker_color='#1a3058'))
            stl=dict(PL); stl['xaxis']=AXIS; stl['yaxis']=dict(**AXIS,title='Count')
            fig_st.update_layout(**stl,height=250,barmode='stack',
                legend=dict(font=dict(color='#4a6fa5',size=9),bgcolor='rgba(0,0,0,0)'),
                title=dict(text='Staff On Duty Today',font=dict(color='#4a6fa5',size=11)))
            st.plotly_chart(fig_st,use_container_width=True,config={'displayModeBar':False})

        st.markdown("---")
        k1,k2,k3,k4=st.columns(4)
        with k1: st.metric("🛏 Total Beds","115","12 available")
        with k2: st.metric("🚨 ICU","9/10","90% full")
        with k3: st.metric("👨‍⚕️ Doctors","18/24","on duty")
        with k4: st.metric("💉 Nurses","36/48","on duty")

        st.markdown("<div class='section-header' style='margin-top:0.8rem;'>Actions</div>",unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        with c1: st.button("📊 Export Report",use_container_width=True)
        with c2: st.button("📧 Send to Board",use_container_width=True)
        with c3: st.button("🖨 Print Summary",use_container_width=True)