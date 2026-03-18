import streamlit as st
import pandas as pd
import requests
import re
import io
import base64
from datetime import datetime, timedelta, timezone

st.set_page_config(
    page_title="EdWise | Vendor Certification",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #f8fafc;
    --bg-secondary: #ffffff;
    --text-primary: #1e293b;
    --border-color: #e2e8f0;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --text-primary: #f1f5f9;
        --border-color: #334155;
    }
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.main { 
    background: var(--bg-primary) !important; 
    color: var(--text-primary) !important;
}
.block-container {
    padding-top: 1rem !important;
    padding-left: 1.8rem !important;
    padding-right: 1.8rem !important;
    padding-bottom: 3rem !important;
    max-width: 100% !important;
}
header[data-testid="stHeader"]                        { display: none !important; }
[data-testid="collapsedControl"]                      { display: none !important; }
[data-testid="stSidebarCollapsedControl"]             { display: none !important; }
button[data-testid="baseButton-headerNoPadding"]      { display: none !important; }
[data-testid="stIconMaterial"]                        { display: none !important; }

section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-color) !important;
    min-width: 340px !important;
    max-width: 340px !important;
    width: 340px !important;
    transform: translateX(0) !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }
section[data-testid="stSidebar"] * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
section[data-testid="stSidebar"] .stButton { margin: 0 !important; padding: 0 !important; }
section[data-testid="stSidebar"] [data-testid="element-container"] { margin: 0 !important; padding: 0 !important; }
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important; text-align: left !important;
    justify-content: flex-start !important; background: transparent !important;
    border: none !important; border-left: 3px solid transparent !important;
    border-radius: 0 !important; padding: 7px 14px !important;
    font-size: 12px !important; font-weight: 500 !important; color: #475569 !important;
    box-shadow: none !important; white-space: nowrap !important;
    overflow: visible !important; text-overflow: clip !important;
    height: auto !important; min-height: 34px !important; line-height: 1.4 !important;
    display: flex !important; align-items: center !important; transition: background 0.12s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #eff6ff !important; color: #1a6fd4 !important;
    border-left-color: #93c5fd !important; transform: none !important; box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button:focus { box-shadow: none !important; outline: none !important; }

[data-testid="stBaseButton-primary"] {
    background: #1a6fd4 !important; color: #ffffff !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important; font-size: 14px !important;
    white-space: nowrap !important; padding: 10px 20px !important;
    box-shadow: 0 2px 8px rgba(26,111,212,0.28) !important; justify-content: center !important;
}
[data-testid="stBaseButton-primary"]:hover { background: #1558b0 !important; transform: translateY(-1px) !important; }

.stDownloadButton > button {
    background: #ffffff !important; color: #1a6fd4 !important;
    border: 1.5px solid #1a6fd4 !important; border-radius: 8px !important;
    font-weight: 600 !important; white-space: nowrap !important;
}
.stDownloadButton > button:hover { background: #eff6ff !important; }

.stTextInput input {
    background: #ffffff !important; border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important; color: #1e293b !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 13px !important; padding: 10px 14px !important;
}
.stTextInput input:focus { border-color: #1a6fd4 !important; box-shadow: 0 0 0 3px rgba(26,111,212,0.1) !important; }
.stTextInput label { font-size: 12px !important; font-weight: 600 !important; color: #64748b !important; }

.stTabs [data-baseweb="tab-list"] { background: #f1f5f9 !important; border-radius: 8px !important; padding: 3px !important; gap: 2px !important; }
.stTabs [data-baseweb="tab"] { border-radius: 6px !important; font-size: 13px !important; font-weight: 500 !important; color: #64748b !important; padding: 7px 14px !important; }
.stTabs [aria-selected="true"] { background: #ffffff !important; color: #1a6fd4 !important; font-weight: 700 !important; box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important; }
[data-testid="stDataFrame"] { border: 1px solid #e2e8f0 !important; border-radius: 8px !important; }
.streamlit-expanderHeader { background: #f8fafc !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; font-size: 13px !important; font-weight: 600 !important; }
hr { border-color: #e2e8f0 !important; margin: 14px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── JS: kill keyboard_double_arrow permanently ──
st.markdown("""<script>
(function(){
    function kill(){
        ['collapsedControl','stSidebarCollapsedControl'].forEach(function(tid){
            document.querySelectorAll('[data-testid="'+tid+'"]').forEach(function(el){ el.parentNode&&el.parentNode.removeChild(el); });
        });
        document.querySelectorAll('button').forEach(function(btn){
            if(btn.textContent.indexOf('keyboard_double_arrow')!==-1){ btn.parentNode&&btn.parentNode.removeChild(btn); }
        });
        document.querySelectorAll('span').forEach(function(sp){
            if(sp.textContent.trim()==='keyboard_double_arrow_left'||sp.textContent.trim()==='keyboard_double_arrow_right'){
                sp.style.cssText='display:none!important;font-size:0!important;';
                var btn=sp.closest('button'); if(btn) btn.style.cssText='display:none!important;';
            }
        });
    }
    kill();
    new MutationObserver(kill).observe(document.body||document.documentElement,{childList:true,subtree:true});
    setInterval(kill,500);
})();
</script>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# API CONFIG
# ─────────────────────────────────────────────────────────────────
TOKEN_URL    = st.secrets["ods_api"]["token_url"]
API_KEY      = st.secrets["ods_api"]["api_key"]
API_SECRET   = st.secrets["ods_api"]["api_secret"]
BASE_API_URL = "https://doe-edfiods-a-c-v2026-ca.grayisland-7cb4ec7b.eastus.azurecontainerapps.io/2026/data/v3/ed-fi"

# ─────────────────────────────────────────────────────────────────
# 17 RESOURCES
# ─────────────────────────────────────────────────────────────────
RESOURCES = [
    ("📋", "AssessmentAccommodation",     "AssessmentAccommodation"),
    ("📅", "Calendar",                    "Calendar"),
    ("🔗", "CohortAssociation",           "CohortAssociation"),
    ("🏫", "EdOrgOther",                  "EdOrgOther"),
    ("📆", "MasterSchedule",              "MasterSchedule"),
    ("👨‍🏫", "Staff",                       "Staff"),
    ("🎓", "StudentAltEdProgram",         "StudentAltEdProgram"),
    ("📊", "StudentAttendance",           "StudentAttendance"),
    ("👤", "StudentDemographics",         "StudentDemographics"),
    ("⚖️",  "StudentDiscipline",           "StudentDiscipline"),
    ("🏫", "StudentEnrollment",           "StudentEnrollment"),
    ("📚", "StudentPrograms",             "StudentPrograms"),
    ("🎯", "StudentSchoolGraduationPlan", "StudentSchoolGraduationPlan"),
    ("♿", "StudentSpecEdProgram",        "StudentSpecEdProgram"),
    ("📝", "StudentTitleIProgram",        "StudentTitleIProgram"),
    ("📜", "StudentTranscript",           "StudentTranscript"),
    ("🎓", "Student",                     "Student"),
]

# ─────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────
if "active_script"  not in st.session_state: st.session_state.active_script  = "Student"
if "num_records"    not in st.session_state: st.session_state.num_records    = 3
if "record_data"    not in st.session_state:
    st.session_state.record_data = [
        {"sid": "127013241", "cid": "103781017300000"},
        {"sid": "", "cid": ""},
        {"sid": "", "cid": ""},
    ]

# Default sample rows
if "sample_student_rows" not in st.session_state:
    st.session_state.sample_student_rows = [{"StudentUniqueId":"","FirstName":"LILY","MiddleName":"SOFVIA","LastSurname":"ACRA","BirthSexDescriptor":"Female","BirthDate":"2008-03-24","BirthCountryDescriptor":"USA"}]
if "sample_contact_rows" not in st.session_state:
    st.session_state.sample_contact_rows = [{"ContactUniqueId":"","FirstName":"TODD","LastSurname":"ACRA","ElectronicMailTypeDescriptor":"Home/Personal","ElectronicMailAddress":"todd.acra@example.com"}]
if "sample_assoc_rows" not in st.session_state:
    st.session_state.sample_assoc_rows   = [{"StudentUniqueId":"","ContactUniqueId":"","LegalDesignee":"true"}]

# Descriptor cache
if "descriptor_cache" not in st.session_state: st.session_state.descriptor_cache = {}

# Editable API endpoints — SIMPLIFIED (StudentContact removed, only Student/Contact/Association)
if "api_endpoints" not in st.session_state:
    st.session_state.api_endpoints = [
        {"id": "ep_1", "label":"students","url":f"{BASE_API_URL}/students?totalCount=true&studentUniqueId={{StudentUniqueId}}","active":True,"entity":"Student"},
        {"id": "ep_2", "label":"contacts","url":f"{BASE_API_URL}/contacts?totalCount=true&contactUniqueId={{ContactUniqueId}}","active":True,"entity":"Contact"},
        {"id": "ep_3", "label":"studentContactAssociations","url":f"{BASE_API_URL}/studentContactAssociations?totalCount=true&studentUniqueId={{StudentUniqueId}}&contactUniqueId={{ContactUniqueId}}","active":True,"entity":"Association"},
    ]

MANDATORY_FIELDS = {
    "StudentUniqueId","FirstName","LastSurname",
    "BirthSexDescriptor","BirthDate","BirthCountryDescriptor",
    "ContactUniqueId","ElectronicMailTypeDescriptor","ElectronicMailAddress",
    "LegalDesignee",
}

# ─────────────────────────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────────────────────────
def get_bearer_token():
    if "token_info" in st.session_state:
        ti = st.session_state["token_info"]
        if datetime.now(timezone.utc) < ti["expiry"]:
            return ti["access_token"]
    enc = base64.b64encode(f"{API_KEY}:{API_SECRET}".encode()).decode()
    r = requests.post(TOKEN_URL,
        headers={"Authorization":f"Basic {enc}","Content-Type":"application/x-www-form-urlencoded"},
        data={"grant_type":"client_credentials"})
    r.raise_for_status()
    d = r.json()
    st.session_state["token_info"] = {
        "access_token": d["access_token"],
        "expiry": datetime.now(timezone.utc) + timedelta(seconds=d["expires_in"]),
    }
    return d["access_token"]

def api_get(url):
    try:
        token = get_bearer_token()
        r = requests.get(url, headers={"Authorization":f"Bearer {token}"}, timeout=10)
        r.raise_for_status()
        return r
    except requests.exceptions.RequestException as e:
        st.warning(f"⚠️ API Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def extract_nested(record, path):
    parts = path.replace("[",".").replace("]","").split(".")
    val = record
    for p in parts:
        if val is None: return None
        if p.isdigit() and isinstance(val, list): val = val[int(p)] if len(val)>int(p) else None
        elif isinstance(val, dict): val = val.get(p)
        else: val = None
    return val

def strip_descriptor_uri(v):
    return v.split("#")[-1] if isinstance(v, str) and "#" in v else v

def convert_boolean(v):
    if isinstance(v, bool): return "true" if v else "false"
    if isinstance(v, str):
        lv = v.strip().lower()
        if lv in ("true","1"): return "true"
        if lv in ("false","0"): return "false"
    if isinstance(v,(int,float)): return "true" if v else "false"
    return v

def null_df(cols, rec_num, status="NOT_FOUND"):
    row = {c:"NULL" for c in cols}
    row["_api_status"] = status
    row["_record_num"] = rec_num
    return pd.DataFrame([row])

def fetch_api_single(url, cols, nested=None, desc_cols=None, bool_cols=None, show_debug=True, debug_label=None):
    token = get_bearer_token()
    debug_label_text = debug_label if debug_label else url
    if show_debug:
        with st.expander(f"🔍 API Debug — {debug_label_text}", expanded=False):
            r = requests.get(url, headers={"Authorization":f"Bearer {token}"})
            st.caption(f"Status: {r.status_code}")
            try: st.json(r.json())
            except: st.write(r.text)
    else:
        r = requests.get(url, headers={"Authorization":f"Bearer {token}"})

    if r.status_code != 200:
        return None, "NOT_FOUND"
    try: data = r.json()
    except: return None, "NOT_FOUND"
    recs = data if isinstance(data,list) else data.get("value",[])
    if not recs: return None, "NOT_FOUND"

    rows = []
    for rec in recs:
        row = {}
        if nested:
            for tc,path in nested.items(): row[tc] = extract_nested(rec, path)
        flat = pd.json_normalize(rec).to_dict(orient="records")[0]
        for col in cols:
            if col not in row:
                row[col] = flat.get(col, flat.get(col[0].lower()+col[1:], None))
        row["_api_status"] = "FOUND"
        rows.append(row)
    df = pd.DataFrame(rows)
    for c in cols:
        if c not in df.columns: df[c] = None
    if "_api_status" not in df.columns: df["_api_status"] = "FOUND"
    if desc_cols:
        for c in desc_cols:
            if c in df.columns: df[c] = df[c].apply(strip_descriptor_uri)
    if bool_cols:
        for c in bool_cols:
            if c in df.columns: df[c] = df[c].apply(convert_boolean)
    return df, "FOUND"

# ─────────────────────────────────────────────────────────────────
# DESCRIPTOR VALIDATION — Dynamic API Checks
# ─────────────────────────────────────────────────────────────────
DESCRIPTOR_API_MAP = {
    "BirthSexDescriptor": f"{BASE_API_URL}/sexDescriptors",
    "BirthCountryDescriptor": f"{BASE_API_URL}/countryDescriptors",
    "ElectronicMailTypeDescriptor": f"{BASE_API_URL}/electronicMailTypeDescriptors",
}

def check_descriptor_via_api(descriptor_type, code_value, show_debug=True):
    """
    Check if a codeValue exists in the descriptor API.
    Returns (is_valid, reason_message)
    
    UPDATED: Show API response in expander with better error handling
    """
    api_url = DESCRIPTOR_API_MAP.get(descriptor_type)
    if not api_url:
        return True, f"No API validation available for {descriptor_type}"
    
    # Build query URL with codeValue parameter
    query_url = f"{api_url}?offset=0&totalCount=true&codeValue={code_value}"
    
    try:
        token = get_bearer_token()
        if not token:
            return False, "Failed to get authentication token"
            
        r = requests.get(query_url, headers={"Authorization": f"Bearer {token}"}, timeout=10)
        
        # Show debug output for descriptors (like Student/Contact)
        if show_debug:
            with st.expander(f"🔍 API Debug — {descriptor_type} Validation (codeValue={code_value})", expanded=False):
                st.caption(f"Status: {r.status_code}")
                try: 
                    st.json(r.json())
                except: 
                    st.write(r.text)
        
        if r.status_code != 200:
            return False, f"API error {r.status_code} — unable to validate '{code_value}'"
        
        try:
            data = r.json()
            items = data if isinstance(data, list) else data.get("value", [])
            
            # If we get results, the codeValue is valid
            if items and len(items) > 0:
                return True, f"✓ Valid descriptor: '{code_value}' found in {descriptor_type} API"
            else:
                return False, f"✗ Invalid descriptor: '{code_value}' NOT found in {descriptor_type} API"
        except ValueError as je:
            return False, f"Invalid JSON response: {str(je)}"
            
    except requests.exceptions.Timeout:
        return False, f"API timeout — {descriptor_type} validation failed"
    except requests.exceptions.ConnectionError:
        return False, f"Connection error — cannot reach {descriptor_type} API"
    except Exception as e:
        return False, f"API validation error: {str(e)}"

# ─────────────────────────────────────────────────────────────────
# FIELD VALIDATION — with dynamic descriptor checking
# ─────────────────────────────────────────────────────────────────
def infer_field_type(value):
    """Infer field type from value for dynamic validation"""
    if value is None or str(value).strip() in ("", "None", "nan", "null", "NULL"):
        return "empty"
    
    val_str = str(value).strip()
    
    # Check if numeric
    try:
        float(val_str)
        return "numeric"
    except ValueError:
        pass
    
    # Check if date
    if re.match(r"^\d{4}-\d{2}-\d{2}$", val_str):
        try:
            datetime.strptime(val_str, "%Y-%m-%d")
            return "date"
        except ValueError:
            pass
    
    # Check if email
    if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", val_str):
        return "email"
    
    # Check if boolean
    if val_str.lower() in ("true", "false", "1", "0"):
        return "boolean"
    
    # Default to text
    return "text"

def validate_field(field_name, value, sample_value=None, show_debug=False):
    val = value
    is_empty = (val is None or str(val).strip()==""
                or str(val).strip().lower() in ("none","nan","null"))

    if is_empty:
        sample_empty = (sample_value is None or str(sample_value).strip()==""
                        or str(sample_value).strip().lower() in ("none","nan"))
        if not sample_empty and field_name in MANDATORY_FIELDS:
            return False, "❗ Mandatory field — value required but not posted by vendor"
        return False, "Missing — no value posted"

    # Known field validations
    if field_name in ("StudentUniqueId","ContactUniqueId"):
        return True, "Value present (alphanumeric accepted)"

    if field_name in ("FirstName","MiddleName","LastSurname"):
        if not re.match(r"^[A-Za-z\s\-'\.]+$", str(val).strip()):
            return False, f"Invalid — non-character value: '{val}'"
        return True, "Valid character value"

    # DYNAMIC DESCRIPTOR VALIDATION via API
    if field_name in DESCRIPTOR_API_MAP:
        clean_val = str(val).strip()
        is_valid, reason = check_descriptor_via_api(field_name, clean_val, show_debug=show_debug)
        return is_valid, reason

    if field_name == "BirthDate":
        clean = str(val).strip()
        if re.match(r"^\d{4}-\d{2}-\d{2}$", clean):
            try:
                datetime.strptime(clean, "%Y-%m-%d")
                return True, f"Valid date format: '{clean}'"
            except ValueError:
                return False, f"Invalid date: '{clean}'"
        return False, f"Invalid date format: '{clean}' — expected YYYY-MM-DD"

    if field_name == "ElectronicMailAddress":
        clean = str(val).strip()
        if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", clean):
            return True, "Valid email format"
        return False, f"Invalid email format: '{clean}'"

    if field_name == "LegalDesignee":
        clean = str(val).strip().lower()
        if clean in ("true","false","1","0"):
            return True, f"Valid boolean: '{val}'"
        return False, f"Invalid — expected true/false or 1/0, got: '{val}'"

    # DYNAMIC VALIDATION for new/unknown fields
    field_type = infer_field_type(val)
    
    if field_type == "numeric":
        return True, f"Valid numeric value: '{val}'"
    elif field_type == "date":
        return True, f"Valid date value: '{val}'"
    elif field_type == "email":
        return True, f"Valid email format: '{val}'"
    elif field_type == "boolean":
        return True, f"Valid boolean value: '{val}'"
    elif field_type == "text":
        return True, f"Valid text value: '{val}'"
    
    return True, "Value present"

def run_field_validation(target_df, sample_df, show_descriptor_debug=False):
    rows = []
    
    # Collect descriptor debug info for display at the end
    descriptor_debug_info = []
    
    for rec_idx, row in target_df.iterrows():
        api_status = row.get("_api_status","FOUND") if "_api_status" in target_df.columns else "FOUND"
        rec_num    = row.get("_record_num", rec_idx+1) if "_record_num" in target_df.columns else rec_idx+1
        
        for col in target_df.columns:
            if col.startswith("_"): continue
            val = row[col]
            
            # Store ALL descriptor fields that need debug display (including duplicates for different records)
            if col in DESCRIPTOR_API_MAP and val is not None and str(val).strip() != "":
                if api_status != "NOT_FOUND" and api_status != "SKIPPED":
                    # Add unique descriptor-value combinations
                    desc_tuple = (col, str(val).strip())
                    if desc_tuple not in descriptor_debug_info:
                        descriptor_debug_info.append(desc_tuple)
            
            if api_status == "NOT_FOUND":
                rows.append({"Record #":rec_num,"Field":col,"Value":"NULL","Status":"❌ Invalid","Reason":"🔴 Record NOT FOUND — vendor did not post this record to API"})
                continue
            if api_status == "SKIPPED":
                rows.append({"Record #":rec_num,"Field":col,"Value":"—","Status":"⏭ Skipped","Reason":"ID not provided — entity not fetched"})
                continue
            sample_val = (sample_df[col].iloc[0] if (sample_df is not None and col in sample_df.columns) else None)
            is_valid, reason = validate_field(col, val, sample_val, show_debug=False)
            rows.append({"Record #":rec_num,"Field":col,"Value":str(val) if val is not None else "","Status":"✅ Valid" if is_valid else "❌ Invalid","Reason":reason})
    
    # Store ALL descriptor debug info in session state for display
    if descriptor_debug_info:
        # Merge with existing descriptor info
        if "descriptor_debug_info" not in st.session_state:
            st.session_state["descriptor_debug_info"] = descriptor_debug_info
        else:
            # Merge lists, avoiding duplicates
            existing = st.session_state["descriptor_debug_info"]
            for item in descriptor_debug_info:
                if item not in existing:
                    existing.append(item)
    
    return pd.DataFrame(rows)

def style_validation_df(df):
    def color_row(row):
        color = "#f0fdf4" if row["Status"]=="✅ Valid" else "#fef2f2"
        return [f"background-color: {color}"]*len(row)
    return df.style.apply(color_row, axis=1)

# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='padding:14px 12px 10px;border-bottom:1px solid #e2e8f0;margin-bottom:4px;'>"
        "<div style='font-size:15px;font-weight:800;color:#0d2d5e;'>🎓&nbsp; EdWise Group</div>"
        "<div style='font-size:10px;font-weight:600;color:#94a3b8;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;'>Vendor Certification</div>"
        "</div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='padding:7px 12px 3px;font-size:10px;font-weight:700;color:#94a3b8;letter-spacing:2px;text-transform:uppercase;'>Resources List</div>",
        unsafe_allow_html=True)
    for icon, short, name in RESOURCES:
        label     = f"{icon}  {name}"
        is_active = (st.session_state.active_script == short)
        if is_active:
            st.markdown("<div style='background:#eff6ff;border-left:3px solid #1a6fd4;margin:0;padding:0;'>", unsafe_allow_html=True)
        if st.button(label, key=f"nav_{short}", width='stretch'):
            st.session_state.active_script = short
            st.rerun()
        if is_active:
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:10px;padding:8px 12px;border-top:1px solid #e2e8f0;font-size:11px;color:#94a3b8;'>v3.0.0 · Ed-Fi ODS 2026 · Indiana DOE</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# ACTIVE SCRIPT INFO + HEADER
# ─────────────────────────────────────────────────────────────────
active = st.session_state.active_script
sel_icon = sel_name = sel_short = ""
for icon, short, name in RESOURCES:
    if short == active:
        sel_icon=icon; sel_short=short; sel_name=name; break
sel_full = f"{sel_name} Verification"

st.markdown(
    f"<div style='background:#ffffff;border:1.5px solid #cbd5e1;border-radius:10px;"
    f"padding:11px 18px;margin-bottom:16px;display:flex;align-items:center;"
    f"justify-content:space-between;gap:14px;box-shadow:0 1px 4px rgba(0,0,0,0.06);box-sizing:border-box;'>"
    f"<div style='display:flex;align-items:center;gap:9px;flex-shrink:0;'>"
    f"<div style='width:34px;height:34px;flex-shrink:0;background:#1558b0;border-radius:7px;"
    f"display:flex;align-items:center;justify-content:center;font-size:17px;'>🎓</div>"
    f"<div><div style='font-size:14px;font-weight:800;color:#0d2d5e;white-space:nowrap;'>EdWise Group</div>"
    f"<div style='font-size:9px;color:#94a3b8;letter-spacing:1.4px;text-transform:uppercase;white-space:nowrap;'>Vendor Certification Portal</div></div></div>"
    f"<div style='text-align:center;flex:1;min-width:0;'>"
    f"<div style='font-size:13px;font-weight:700;color:#0d2d5e;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{sel_icon}&nbsp; {sel_full}</div>"
    f"<div style='font-size:9px;color:#94a3b8;letter-spacing:1px;text-transform:uppercase;margin-top:1px;white-space:nowrap;'>Ed-Fi ODS 2026 · Indiana DOE</div></div>"
    f"<div style='text-align:right;flex-shrink:0;'>"
    f"<div style='font-size:12px;font-weight:600;color:#1e293b;white-space:nowrap;'>Demo User&nbsp;"
    f"<span style='background:#fef3c7;color:#d97706;font-size:10px;font-weight:700;padding:2px 8px;border-radius:50px;'>DEMO</span></div>"
    f"<div style='font-size:10px;color:#94a3b8;margin-top:2px;white-space:nowrap;'>🔒 Login coming soon</div></div>"
    f"</div>", unsafe_allow_html=True)

# COMING SOON
if active != "Student":
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown(f"## {sel_icon} {sel_name} Verification")
        st.info("🚧 This verification module is under development.\n\nCurrently active: **Student Verification**")
    st.stop()

# ═══════════════════════════════════════════════════════════════
# STUDENT VERIFICATION MAIN
# ═══════════════════════════════════════════════════════════════

# ── Query Parameters ─────────────────────────────────────────────
hdr_l, hdr_r = st.columns([3,1])
with hdr_l:
    st.subheader("🔑 Query Parameters")
    st.caption("Enter Student / Contact ID pairs — click + Add New Record to add more")
with hdr_r:
    st.markdown("<div style='padding-top:18px;'>", unsafe_allow_html=True)
    if st.button("+ Add New Record", key="add_record", type="primary"):
        st.session_state.num_records += 1
        st.session_state.record_data.append({"sid":"","cid":""})
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

id_pairs = []
n = st.session_state.num_records
for row_start in range(0, n, 3):
    row_end  = min(row_start+3, n)
    row_cols = st.columns(row_end-row_start)
    for j, col in enumerate(row_cols):
        i = row_start+j
        with col:
            st.markdown(f"<div style='font-size:11px;font-weight:700;color:#1a6fd4;letter-spacing:.5px;margin-bottom:4px;background:#eff6ff;padding:4px 8px;border-radius:4px;display:inline-block;'>RECORD {i+1}</div>", unsafe_allow_html=True)
            sv = st.session_state.record_data[i]["sid"] if i<len(st.session_state.record_data) else ""
            cv = st.session_state.record_data[i]["cid"] if i<len(st.session_state.record_data) else ""
            sid = st.text_input(f"Student Unique ID {i+1}", value=sv, key=f"sid_{i}")
            cid = st.text_input(f"Contact Unique ID {i+1}", value=cv, key=f"cid_{i}")
            if i < len(st.session_state.record_data):
                st.session_state.record_data[i]["sid"] = sid
                st.session_state.record_data[i]["cid"] = cid
            if sid.strip() or cid.strip():
                id_pairs.append((sid.strip(), cid.strip(), i+1))

st.divider()

# ── Sample Data (EDITABLE ONLY) ─────────────────────────
# UPDATED: Removed Add/Remove Column functionality
st.subheader("📋 Sample Data")
st.caption("Editable — update values as needed.")

sid1 = id_pairs[0][0] if id_pairs and id_pairs[0][0] else "127013241"
cid1 = id_pairs[0][1] if id_pairs and id_pairs[0][1] else "103781017300000"

# Sync first row IDs from query params
if st.session_state.sample_student_rows:
    st.session_state.sample_student_rows[0]["StudentUniqueId"] = sid1
if st.session_state.sample_contact_rows:
    st.session_state.sample_contact_rows[0]["ContactUniqueId"] = cid1
if st.session_state.sample_assoc_rows:
    st.session_state.sample_assoc_rows[0]["StudentUniqueId"] = sid1
    st.session_state.sample_assoc_rows[0]["ContactUniqueId"] = cid1

def render_editable_sample(entity_key, rows_key):
    """
    Render editable sample data table.
    UPDATED: Removed Add/Remove Column functionality - keep only editable table
    """
    rows = st.session_state[rows_key]
    
    # Editable dataframe only
    edited = st.data_editor(
        pd.DataFrame(rows),
        key=f"editor_{entity_key}",
        width='stretch',
        num_rows="dynamic",
        hide_index=True,
    )
    # Save edits back
    st.session_state[rows_key] = edited.to_dict(orient="records")
    return edited

sample_tabs = st.tabs(["👤 Student", "📞 Contact", "🔗 StudentContactAssociation"])
with sample_tabs[0]: sample_student_df = render_editable_sample("student", "sample_student_rows")
with sample_tabs[1]: sample_contact_df = render_editable_sample("contact", "sample_contact_rows")
with sample_tabs[2]: sample_assoc_df   = render_editable_sample("assoc",   "sample_assoc_rows")

st.divider()

# ── API Endpoints Manager (COMPACT & PROFESSIONAL) ─────────────────────────────────────────
# UPDATED: Compact layout, Add button in corner, minimal spacing, professional alignment
with st.expander("⚙️ API Endpoints Manager", expanded=False):
    # Header with Add Endpoint button (right corner) - COMPACT
    hdr_c1, hdr_c2 = st.columns([0.85, 0.15], gap="small")
    with hdr_c1:
        st.caption("Edit URLs and manage endpoints")
    with hdr_c2:
        if st.button("+ Add", key="ep_add_top", type="primary", use_container_width=True):
            new_id = f"ep_{max([int(e.get('id', 'ep_0').split('_')[1]) for e in st.session_state.api_endpoints] + [3]) + 1}"
            st.session_state.api_endpoints.append({
                "id": new_id,
                "label": "new_endpoint",
                "url": f"{BASE_API_URL}/",
                "active": True,
                "entity": "Student"
            })
            st.rerun()
    
    st.markdown("<div style='margin: 6px 0;'></div>", unsafe_allow_html=True)
    
    # Display all endpoints - COMPACT with minimal spacing and fetch button
    to_delete_ids = []
    
    # Create a copy for display to avoid modification during iteration
    endpoints_copy = [ep.copy() for ep in st.session_state.api_endpoints]
    
    for idx, ep in enumerate(endpoints_copy):
        col1, col2, col3 = st.columns([0.85, 0.08, 0.07], gap="small")
        with col1:
            # Get actual endpoint from session state
            actual_ep = None
            for e in st.session_state.api_endpoints:
                if e.get('id') == ep.get('id'):
                    actual_ep = e
                    break
            
            if actual_ep:
                # Only URL text box - compact (with proper label)
                actual_ep["url"] = st.text_input(
                    label=f"endpoint_{idx}",  # Required non-empty label
                    value=actual_ep["url"], 
                    key=f"ep_url_{ep.get('id', idx)}", 
                    label_visibility="collapsed", 
                    placeholder="https://..."
                )
        with col2:
            # Fetch Target Data button (without title parameter)
            if st.button(
                "📊", 
                key=f"ep_fetch_{ep.get('id', idx)}", 
                use_container_width=True,
                help="Fetch Target Data for this endpoint"
            ):
                # Trigger fetch for this specific endpoint
                st.session_state[f"fetch_endpoint_{ep.get('id', idx)}"] = True
        with col3:
            # Delete button - compact
            if st.button("🗑️", key=f"ep_del_{ep.get('id', idx)}", use_container_width=True):
                to_delete_ids.append(ep.get('id', idx))
    
    # Apply deletions by ID AFTER iteration completes
    if to_delete_ids:
        st.session_state.api_endpoints = [
            ep for ep in st.session_state.api_endpoints 
            if ep.get('id') not in to_delete_ids
        ]
        st.rerun()
    
    # ── INDIVIDUAL ENDPOINT FETCH - INSIDE EXPANDER ─────────────────────────────────────
    # Check if any endpoint's "Fetch Target Data" button was clicked
    individual_fetch_endpoint_id = None
    for idx, ep in enumerate(st.session_state.api_endpoints):
        if st.session_state.get(f"fetch_endpoint_{ep.get('id', idx)}", False):
            individual_fetch_endpoint_id = ep.get('id', idx)
            st.session_state[f"fetch_endpoint_{ep.get('id', idx)}"] = False  # Reset flag
            break
    
    # If individual endpoint fetch was triggered, show inside expandable section (INSIDE expander)
    if individual_fetch_endpoint_id:
        st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)
        st.divider()
        st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)
        
        # Find the endpoint
        endpoint_to_fetch = None
        for ep in st.session_state.api_endpoints:
            if ep.get('id') == individual_fetch_endpoint_id:
                endpoint_to_fetch = ep
                break
        
        if endpoint_to_fetch:
            # Create expandable section INSIDE API Endpoints Manager
            with st.expander(f"📊 Fetched Data: {endpoint_to_fetch.get('label', 'Custom Endpoint')}", expanded=True):
                st.caption(f"Endpoint URL: {endpoint_to_fetch.get('url', 'N/A')}")
                
                try:
                    token = get_bearer_token()
                    r = requests.get(endpoint_to_fetch.get('url'), headers={"Authorization": f"Bearer {token}"}, timeout=10)
                    
                    st.caption(f"Status: {r.status_code}")
                    try:
                        response_data = r.json()
                        st.json(response_data)
                    except:
                        st.write(r.text)
                        
                    st.success("✅ Endpoint data fetched successfully")
                except Exception as e:
                    st.error(f"❌ Error fetching endpoint data: {str(e)}")

# Add custom CSS for red delete button
st.markdown("""
<style>
button[kind="secondary"]:has(div:contains("🗑️")) {
    background-color: #fee2e2 !important;
    color: #dc2626 !important;
    border: 1.5px solid #dc2626 !important;
}
button[kind="secondary"]:has(div:contains("🗑️")):hover {
    background-color: #fecaca !important;
    border-color: #b91c1c !important;
}
</style>
""", unsafe_allow_html=True)

# ── Fetch Button ──────────────────────────────────────────────────
btn_c, _sp2 = st.columns([2,3])
with btn_c:
    run = st.button("🚀 Fetch Target & Run Validation", type="primary", width='stretch')

if run:
    if not id_pairs:
        st.error("❌ Please enter at least one Student Unique ID or Contact Unique ID.")
    else:
        STUDENT_COLS = [c for c in sample_student_df.columns if not c.startswith("_")]
        CONTACT_COLS = [c for c in sample_contact_df.columns if not c.startswith("_")]
        ASSOC_COLS   = [c for c in sample_assoc_df.columns   if not c.startswith("_")]

        all_students, all_contacts, all_assocs = [], [], []

        def make_null(cols, rec_num, status="SKIPPED"):
            row = {c:"NULL" for c in cols}
            row["_api_status"] = status; row["_record_num"] = rec_num
            return pd.DataFrame([row])

        with st.spinner(f"Fetching {len(id_pairs)} record pair(s)…"):
            for sid, cid, rec_num in id_pairs:
                # ── Student ──
                if sid:
                    student_eps = [e for e in st.session_state.api_endpoints if e["active"] and e.get("entity") == "Student"]
                    if student_eps:
                        student_ep = student_eps[0]
                        s_url = student_ep["url"].replace("{StudentUniqueId}", sid).replace("{ContactUniqueId}", cid)
                        df_s, _ = fetch_api_single(s_url, STUDENT_COLS,
                            nested={"StudentUniqueId":"studentUniqueId","FirstName":"firstName","MiddleName":"middleName","LastSurname":"lastSurname","BirthSexDescriptor":"birthSexDescriptor","BirthDate":"birthDate","BirthCountryDescriptor":"birthCountryDescriptor"},
                            desc_cols=["BirthSexDescriptor","BirthCountryDescriptor"])
                        if df_s is None:
                            df_s = make_null(STUDENT_COLS, rec_num, "NOT_FOUND")
                        else:
                            df_s["_record_num"] = rec_num; df_s["_student_id"] = sid
                    else:
                        df_s = make_null(STUDENT_COLS, rec_num, "SKIPPED")
                else:
                    df_s = make_null(STUDENT_COLS, rec_num, "SKIPPED")

                # ── Contact ──
                if cid:
                    contact_eps = [e for e in st.session_state.api_endpoints if e["active"] and e.get("entity") == "Contact"]
                    if contact_eps:
                        contact_ep = contact_eps[0]
                        c_url = contact_ep["url"].replace("{StudentUniqueId}", sid).replace("{ContactUniqueId}", cid)
                        df_c, _ = fetch_api_single(c_url, CONTACT_COLS,
                            nested={"ContactUniqueId":"contactUniqueId","FirstName":"firstName","LastSurname":"lastSurname","ElectronicMailAddress":"electronicMails[0].electronicMailAddress","ElectronicMailTypeDescriptor":"electronicMails[0].electronicMailTypeDescriptor"},
                            desc_cols=["ElectronicMailTypeDescriptor"])
                        if df_c is None:
                            df_c = make_null(CONTACT_COLS, rec_num, "NOT_FOUND")
                        else:
                            df_c["_record_num"] = rec_num; df_c["_contact_id"] = cid
                    else:
                        df_c = make_null(CONTACT_COLS, rec_num, "SKIPPED")
                else:
                    df_c = make_null(CONTACT_COLS, rec_num, "SKIPPED")

                # ── Association ──
                if sid and cid:
                    assoc_eps = [e for e in st.session_state.api_endpoints if e["active"] and e.get("entity") == "Association"]
                    if assoc_eps:
                        assoc_ep = assoc_eps[0]
                        a_url = assoc_ep["url"].replace("{StudentUniqueId}", sid).replace("{ContactUniqueId}", cid)
                        df_a, _ = fetch_api_single(a_url, ASSOC_COLS,
                            nested={"StudentUniqueId":"studentReference.studentUniqueId","ContactUniqueId":"contactReference.contactUniqueId","LegalDesignee":"_ext.idoe.legalDesignee"},
                            bool_cols=["LegalDesignee"])
                        if df_a is None:
                            df_a = make_null(ASSOC_COLS, rec_num, "NOT_FOUND")
                        else:
                            df_a["_record_num"] = rec_num
                    else:
                        df_a = make_null(ASSOC_COLS, rec_num, "SKIPPED")
                else:
                    df_a = make_null(ASSOC_COLS, rec_num, "SKIPPED")

                all_students.append(df_s); all_contacts.append(df_c); all_assocs.append(df_a)

        st.session_state["ts"] = pd.concat(all_students, ignore_index=True)
        st.session_state["tc"] = pd.concat(all_contacts, ignore_index=True)
        st.session_state["ta"] = pd.concat(all_assocs,   ignore_index=True)
        st.success(f"✅ Fetched {len(id_pairs)} record pair(s) successfully.")

# ── Results ───────────────────────────────────────────────────────
if "ts" in st.session_state:
    target_student = st.session_state["ts"]
    target_contact = st.session_state["tc"]
    target_assoc   = st.session_state["ta"]

    # Target Data Preview
    st.subheader("📡 Target Data (API Fetched)")
    st.caption("Data posted by vendor — 🔴 NOT FOUND = vendor did not post this record")

    def highlight_not_found(df):
        def row_style(row):
            if row.get("_api_status","FOUND") == "NOT_FOUND":
                return ["background-color:#fee2e2;color:#dc2626;font-weight:600"]*len(row)
            return [""]*len(row)
        return df.style.apply(row_style, axis=1)

    not_found_recs = []
    for df, label in [(target_student,"Student"),(target_contact,"Contact"),(target_assoc,"Association")]:
        if "_api_status" in df.columns:
            nf = df[df["_api_status"]=="NOT_FOUND"]
            if not nf.empty and "_record_num" in nf.columns:
                for rn in sorted(nf["_record_num"].unique()):
                    not_found_recs.append(f"Record {rn} — {label}")
    if not_found_recs:
        st.error("🔴 NOT FOUND: " + "  |  ".join(not_found_recs) + " — Vendor did not post these records to API")

    tt1, tt2, tt3 = st.tabs(["👤 Student","📞 Contact","🔗 StudentContactAssociation"])
    def show_target(df):
        display_cols = [c for c in df.columns if not c.startswith("_")]
        show_df = df[display_cols + ["_api_status"]].copy() if "_api_status" in df.columns else df[display_cols]
        st.dataframe(highlight_not_found(show_df), width='stretch', hide_index=True)
    with tt1: show_target(target_student)
    with tt2: show_target(target_contact)
    with tt3: show_target(target_assoc)

    st.divider()

    # Clear previous descriptor debug info
    st.session_state["descriptor_debug_info"] = []
    
    # Validation
    st.subheader("✅ Field Validation Results")
    st.caption("Each field validated against rules — descriptors checked via actual API calls")

    sample_s = pd.DataFrame(st.session_state.sample_student_rows)
    sample_c = pd.DataFrame(st.session_state.sample_contact_rows)
    sample_a = pd.DataFrame(st.session_state.sample_assoc_rows)

    sv_df = run_field_validation(target_student, sample_s, show_descriptor_debug=True)
    cv_df = run_field_validation(target_contact, sample_c, show_descriptor_debug=True)
    av_df = run_field_validation(target_assoc,   sample_a, show_descriptor_debug=True)

    def entity_status(vdf):
        if vdf.empty: return "❌ FAIL — No records"
        n = int((vdf["Status"]=="❌ Invalid").sum())
        return "✅ PASS" if n==0 else f"❌ FAIL — {n} invalid field(s)"

    ss = entity_status(sv_df); cs = entity_status(cv_df); as_ = entity_status(av_df)

    vc1, vc2, vc3 = st.columns(3)
    for ui_col, entity, status, vdf in [(vc1,"Student",ss,sv_df),(vc2,"Contact",cs,cv_df),(vc3,"StudentContactAssociation",as_,av_df)]:
        is_pass = status.startswith("✅")
        top_c = "#16a34a" if is_pass else "#dc2626"
        bg_c  = "#f0fdf4" if is_pass else "#fef2f2"
        pill_bg = "#dcfce7" if is_pass else "#fee2e2"
        pill_fg = "#16a34a" if is_pass else "#dc2626"
        total = len(vdf)
        valid   = int((vdf["Status"]=="✅ Valid").sum())   if not vdf.empty else 0
        invalid = int((vdf["Status"]=="❌ Invalid").sum()) if not vdf.empty else 0
        with ui_col:
            st.markdown(
                f"<div style='background:{bg_c};border:1px solid #e2e8f0;border-top:3px solid {top_c};border-radius:10px;padding:18px;'>"
                f"<div style='font-size:12px;font-weight:700;color:#64748b;margin-bottom:12px;'>{entity}</div>"
                f"<div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='font-size:12px;color:#94a3b8;'>Total Fields</span><span style='font-size:20px;font-weight:800;color:#0d2d5e;'>{total}</span></div>"
                f"<div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='font-size:12px;color:#16a34a;'>✅ Valid</span><span style='font-size:16px;font-weight:700;color:#16a34a;'>{valid}</span></div>"
                f"<div style='display:flex;justify-content:space-between;margin-bottom:14px;'><span style='font-size:12px;color:#dc2626;'>❌ Invalid</span><span style='font-size:16px;font-weight:700;color:#dc2626;'>{invalid}</span></div>"
                f"<span style='background:{pill_bg};color:{pill_fg};font-size:12px;font-weight:700;padding:4px 14px;border-radius:50px;'>{status}</span>"
                f"</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    vt1, vt2, vt3 = st.tabs(["👤 Student Fields","📞 Contact Fields","🔗 Association Fields"])
    with vt1:
        if sv_df.empty: st.warning("No student data returned from API.")
        else: st.dataframe(style_validation_df(sv_df), width='stretch', hide_index=True)
    with vt2:
        if cv_df.empty: st.warning("No contact data returned from API.")
        else: st.dataframe(style_validation_df(cv_df), width='stretch', hide_index=True)
    with vt3:
        if av_df.empty: st.warning("No association data returned from API.")
        else: st.dataframe(style_validation_df(av_df), width='stretch', hide_index=True)

    st.divider()

    # ── API DEBUG SECTION - DESCRIPTOR VALIDATIONS ONLY ──────────────────────────────
    # UPDATED: Show ONLY descriptor API validations, no entity responses
    with st.expander("🔍 API Debug Outputs — Descriptor Validations", expanded=False):
        st.caption("Descriptor API validation logs")
        
        # ── DESCRIPTOR VALIDATIONS ONLY ──────────────────────────────────────────
        if "descriptor_debug_info" in st.session_state and st.session_state["descriptor_debug_info"]:
            for desc_type, code_value in st.session_state["descriptor_debug_info"]:
                with st.expander(f"📊 {desc_type}: {code_value}", expanded=False):
                    check_descriptor_via_api(desc_type, code_value, show_debug=True)
        else:
            st.info("ℹ️ No descriptor validations to display")
    
    st.divider()

    # Download
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        pd.DataFrame([{"Entity":ent,"Total Fields":len(vdf),"Valid":int((vdf["Status"]=="✅ Valid").sum()) if not vdf.empty else 0,"Invalid":int((vdf["Status"]=="❌ Invalid").sum()) if not vdf.empty else 0,"Overall Status":stat}
            for ent,vdf,stat in [("Student",sv_df,ss),("Contact",cv_df,cs),("StudentContactAssociation",av_df,as_)]
        ]).to_excel(writer, sheet_name="Summary", index=False)
        target_student.to_excel(writer, sheet_name="Target_Student", index=False)
        target_contact.to_excel(writer, sheet_name="Target_Contact", index=False)
        target_assoc.to_excel(  writer, sheet_name="Target_Assoc",   index=False)
        if not sv_df.empty: sv_df.to_excel(writer, sheet_name="Validation_Student", index=False)
        if not cv_df.empty: cv_df.to_excel(writer, sheet_name="Validation_Contact", index=False)
        if not av_df.empty: av_df.to_excel(writer, sheet_name="Validation_Assoc",   index=False)
        all_parts = [df.assign(Entity=e) for df,e in [(sv_df,"Student"),(cv_df,"Contact"),(av_df,"StudentContactAssociation")] if not df.empty]
        if all_parts:
            combined = pd.concat(all_parts, ignore_index=True)
            inv = combined[combined["Status"]=="❌ Invalid"]
            if not inv.empty: inv.to_excel(writer, sheet_name="All_Invalid_Fields", index=False)

    dl_c, _sp3 = st.columns([2,3])
    with dl_c:
        st.download_button(
            label="📥 Download Full Validation Report",
            data=output.getvalue(),
            file_name=f"EdWise_Validation_Student_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch'
        )
