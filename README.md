# 🎓 EdWise Group — Vendor Certification Portal

> **Student Verification Module** · Ed-Fi ODS 2026 · Indiana DOE  
> A Streamlit-based web application that fetches live student data from the Ed-Fi ODS API and runs **fully automated certification validation** across Students, Contacts, and StudentContactAssociations.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Supported Resources](#supported-resources)
- [Validation Rules](#validation-rules)
- [API Endpoints](#api-endpoints)
- [Export & Reporting](#export--reporting)
- [Status Indicators](#status-indicators)

---

## Overview

The **EdWise Vendor Certification Portal** is a multi-module web application built for **Indiana Department of Education (DOE)** vendors to certify their student data submissions against the **Ed-Fi ODS 2026** API. The portal fetches live data in real time, validates every field against mandatory rules, format checks, and descriptor API lookups, and produces a downloadable Excel certification report — all in a single click.

The portal supports **two modules**:
- 🎓 **Student Verification** — this module (active)
- 💰 **School Finance Verification** — separate module

---

## Features

- ✅ **Live API Fetch** — Pulls real-time data from Ed-Fi ODS with OAuth2 Bearer Token authentication
- ✅ **Multi-Record Support** — Validate multiple Student/Contact ID pairs simultaneously in a single run
- ✅ **Three Entity Coverage** — Student, Contact, and StudentContactAssociation all validated together
- ✅ **Field-Level Validation** — Every field checked for format, mandatory value, and type
- ✅ **Descriptor API Validation** — BirthSexDescriptor, BirthCountryDescriptor, and ElectronicMailTypeDescriptor verified live against ODS descriptor APIs
- ✅ **NOT FOUND Detection** — Clearly flags records the vendor failed to post to the API
- ✅ **Editable Sample Data** — Interactive data tables let reviewers edit expected values on the fly
- ✅ **Custom API Endpoint Manager** — Add, edit, or remove ODS endpoints directly in the UI
- ✅ **Excel Export** — Full certification report with per-entity sheets and a combined invalid-fields sheet
- ✅ **Professional UI** — Custom-styled Streamlit interface with 17 resource navigation items and consistent stat cards
- ✅ **Token Caching** — Bearer tokens cached in session state and auto-refreshed on expiry

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend / App Framework | [Streamlit](https://streamlit.io/) |
| Language | Python 3.10+ |
| Data Processing | Pandas |
| HTTP Client | Requests |
| Authentication | OAuth2 Client Credentials (Bearer Token) |
| API Standard | Ed-Fi ODS REST API v3 (2026) |
| Export | openpyxl (Excel .xlsx) |
| Styling | Custom CSS + Google Fonts (Plus Jakarta Sans, JetBrains Mono) |

---

## Project Structure

```
edwise/
├── pages/
│   ├── 1_Student_Verification.py       # This file — Student module
│   └── 2_School_Finance_Verification.py  # Finance module (separate)
├── .streamlit/
│   └── secrets.toml                    # API credentials (never committed)
├── README.md
└── requirements.txt
```

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/edwise.git
cd edwise
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
streamlit>=1.32.0
pandas>=2.0.0
requests>=2.31.0
openpyxl>=3.1.0
```

### 3. Configure Secrets

Create `.streamlit/secrets.toml`:

```toml
[ods_api]
token_url    = "https://your-ods-host/oauth/token"
api_key      = "YOUR_CLIENT_ID"
api_secret   = "YOUR_CLIENT_SECRET"
base_api_url = "https://your-ods-host/2026/data/v3/ed-fi"
```

> ⚠️ **Never commit `secrets.toml` to version control.** Add it to `.gitignore`.

### 4. Run the Application

```bash
streamlit run pages/1_Student_Verification.py
```

Or from the multi-page app root:
```bash
streamlit run Home.py
```

---

## Configuration

### API Base URL

| Namespace | Base URL |
|-----------|----------|
| Ed-Fi Standard | `https://<host>/2026/data/v3/ed-fi` |

### Token Caching

Bearer tokens are cached in Streamlit `session_state` and auto-refreshed when expired, based on the `expires_in` value returned by the OAuth token endpoint. No manual token management is required.

### Default API Endpoints

| Entity | Default Endpoint |
|--------|----------------|
| Student | `GET /students?totalCount=true&studentUniqueId={StudentUniqueId}` |
| Contact | `GET /contacts?totalCount=true&contactUniqueId={ContactUniqueId}` |
| Association | `GET /studentContactAssociations?totalCount=true&studentUniqueId={StudentUniqueId}&contactUniqueId={ContactUniqueId}` |

All endpoints are user-editable in the **API Endpoint Configuration** expander panel within the app.

---

## How It Works

```
Step 1  →  Enter Student Unique ID(s) and Contact Unique ID(s)
           (up to N pairs; click "+ Add New Record" for more)
           ↓
Step 2  →  Review / edit vendor sample data in editable tables
           (Student, Contact, StudentContactAssociation)
           ↓
Step 3  →  Click "▶ Run Certification Validation"
           ↓
           Authenticate to Ed-Fi ODS API (OAuth2)
           ↓
           Fetch live records for each entity per ID pair
           ↓
           Run field-level validations and descriptor API checks
           ↓
Result 1 — Vendor-Submitted Data (API Response)
Result 2 — Field-Level Validation with pass/fail counts
           ↓
Download Excel certification report
```

---

## Supported Resources

The portal sidebar lists **17 Ed-Fi resources**. Currently, Student Verification is the active module:

| Icon | Resource |
|------|---------|
| 👤 | Student ✅ Active |
| 📋 | AssessmentAccommodation |
| 📅 | Calendar |
| 🔗 | CohortAssociation |
| 🏫 | EdOrgOther |
| 📆 | MasterSchedule |
| 👨‍🏫 | Staff |
| 🎓 | StudentAltEdProgram |
| 📊 | StudentAttendance |
| ⚖️ | StudentDiscipline |
| 🏫 | StudentEnrollment |
| 📚 | StudentPrograms |
| 🎯 | StudentSchoolGraduationPlan |
| ♿ | StudentSpecEdProgram |
| 📝 | StudentTitleIProgram |
| 📜 | StudentTranscript |

Remaining modules are marked "Coming Soon" in the UI.

---

## Validation Rules

### Student Entity

| Field | Rule |
|-------|------|
| StudentUniqueId | Mandatory; alphanumeric accepted |
| FirstName | Mandatory; letters, spaces, hyphens, apostrophes only |
| MiddleName | Optional; character format check |
| LastSurname | Mandatory; character format check |
| BirthSexDescriptor | Mandatory; validated live against `/sexDescriptors` API |
| BirthDate | Mandatory; must be `YYYY-MM-DD` format |
| BirthCountryDescriptor | Mandatory; validated live against `/countryDescriptors` API |

### Contact Entity

| Field | Rule |
|-------|------|
| ContactUniqueId | Mandatory; alphanumeric accepted |
| FirstName | Mandatory; character format check |
| LastSurname | Mandatory; character format check |
| ElectronicMailTypeDescriptor | Mandatory; validated live against `/electronicMailTypeDescriptors` API |
| ElectronicMailAddress | Mandatory; must be valid email format |

### StudentContactAssociation Entity

| Field | Rule |
|-------|------|
| StudentUniqueId | Synced from Student entity |
| ContactUniqueId | Synced from Contact entity |
| LegalDesignee | Must be `true` or `false` (boolean) |

---

## API Endpoints

### Data Fetch Endpoints

| Entity | Endpoint |
|--------|---------|
| Student | `GET /students?totalCount=true&studentUniqueId={id}` |
| Contact | `GET /contacts?totalCount=true&contactUniqueId={id}` |
| StudentContactAssociation | `GET /studentContactAssociations?totalCount=true&studentUniqueId={sid}&contactUniqueId={cid}` |

### Descriptor Validation Endpoints

| Descriptor | Endpoint |
|-----------|---------|
| BirthSexDescriptor | `GET /sexDescriptors?codeValue={value}` |
| BirthCountryDescriptor | `GET /countryDescriptors?codeValue={value}` |
| ElectronicMailTypeDescriptor | `GET /electronicMailTypeDescriptors?codeValue={value}` |

---

## Export & Reporting

Clicking **"📥 Export Certification Report"** downloads an Excel workbook.

| Sheet Name | Contents |
|-----------|---------|
| `Summary` | Pass/Fail counts per entity (Student, Contact, Association) |
| `Target_Student` | Raw API response — Student records |
| `Target_Contact` | Raw API response — Contact records |
| `Target_Assoc` | Raw API response — Association records |
| `Validation_Student` | Field-level validation results for Students |
| `Validation_Contact` | Field-level validation results for Contacts |
| `Validation_Assoc` | Field-level validation results for Associations |
| `All_Invalid_Fields` | Combined list of all failed field validations across all entities |

**Filename format:** `EdWise_CertReport_Student_YYYYMMDD_HHMM.xlsx`

---

## Status Indicators

| Icon | Meaning |
|------|---------|
| ✅ Valid / Pass | Field is correct, rule satisfied |
| ❌ Invalid / Fail | Field has an error or rule violated |
| ⏭ Skipped | ID not provided — entity not fetched |
| 🔴 NOT FOUND | Vendor did not post this record to the API |

---

## Version

| Property | Value |
|----------|-------|
| App Version | v3.0.0 |
| Ed-Fi ODS Version | 2026 |
| Target State | Indiana DOE |

---

*Built by EdWise Group — Vendor Certification Portal · Ed-Fi ODS 2026 · Indiana DOE*
