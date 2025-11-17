# IDSR API

- IDSR API is an integrated disease surveillance response api which is based on the IDSR World health organisation form. It contains all the categories of the IDSR WHO form as separate services.

---

## List of Services
- [IDSR API](#idsr-api)
  - [List of Services](#list-of-services)
  - [IDSR API Categories/Services](#idsr-api-categoriesservices)
    - [Demographics / Patient Details](#demographics--patient-details)
    - [Lab](#lab)
    - [Clinical Details](#clinical-details)
    - [Epidemiological Details](#epidemiological-details)
    - [Facility Details](#facility-details)
    - [Surveillance Information](#surveillance-information)
    - [Treatment](#treatment)
    - [Outcome](#outcome)
    - [Maintainer](#maintainer)

---

## IDSR API Categories/Services
    
### Demographics / Patient Details

- Patient demographic details    

| Field | Data Type | Description |
|-------|-----------|-------------|
|Patient_id | Int   | Patient unique identity |
|Full name| String | Patients full name |
|Age | Int | Patients age |
|Sex | String | Patients sex or gender i.e Male or Female |
|Date of birth | Date | Patients date of birth |
|National Id | String | Patients national identity number|
|Village | String | Patients village|
|Traditional authority| String | Patient's area T/A|
|Health facility| String | Name of the health facility |
|District| String | Districts name |
|Region| String | Regions name |
|Date first seen| Date | Date the patient was first seen|
|Date of death|  Date | Date of death     |
|Date results received| Date| Date results received |
|Vaccination status| String|  Patients vaccination status |
|Date last vaccination| Date | Date patient was last vaccinated|


### Lab

-Lab details

| Field | Data Type | Description |
|-------|-----------|-------------|
|Patient_id | Int   | Patient unique identity |
|Full name| String | Patients full name |
|Specimen Collected| String | Specimen collected |
|Date Specimen Collected | Date | The date specimen was collected from patient|
|Specimen Type | String | Type of specimen i.e blood, stool, urine etc |
|Lab name| String | The name of the lab|
|Specimen sent to lab| String | Whether Specimen was sent to lab or not|
|Lab result| String | Lab result i.e Positive or Negative |
|Lab tests ordered| String | Lab tests ordered|

### Clinical Details

- Patient clinical details

| Field | Data Type | Description |
|-------|-----------|-------------|
|Disease | String | Disease name i.e Malaria etc |
|Date of onset| Date| Date of onset |
|Case classification| String | Whether case is probable or confirmed etc|
|Symptoms | String| Patient symptoms i.e headache etc|
|Triage level | String | Triage level i.e|
|Diagnosis type | String | Diagnosis type  i.e|
|Final case classification | String | final case classification i.e |
|Admission status | String | admission status i.e |
|Contact with confirmed case | String | contact with confirmed case i.e |
|Recent travel history | String | If patient travelled or not i.e |
|Travel destination| String | Patients/case travel destination i.e |

### Epidemiological Details

- Epidemiological details    

| Field | Data Type | Description |
|-------|-----------|-------------|
|Environmental risk factors | String | Environmental risk factors i.e |   
|Exposure source| String | Exposure source i.e |
|Cluster related| String | Cluster related i.e |

### Facility Details

- Health facility details    

| Field | Data Type | Description |
|-------|-----------|-------------|
|Designation | String | Type of the health personel  i.e Clinician or health surveillance officer |   
|Date reported| String | The date the case was reported i.e |
|Form completed by| String | Name of the person who completed the form i.e |
|Health facility code| String | health facility code i.e |
|Case source| String | case source i.e |
|Reporting method| String | reporting method i.e Form or SMS or Electronic form |


### Surveillance Information

- Health surveillance information     

| Field | Data Type | Description |
|-------|-----------|-------------|
|Reporting week number | Int | The week case was reported|   
|Year| Date | The year case was reported |
|Date reported| Date | The actual date case was reported  |
|Notifier signature| String | Notifiers signature |
|Reviewed by| String | Name of the form reviewer |
|Supervisor comments| String | Comments made by the supervisor |


### Treatment

- Treatment details       

| Field | Data Type | Description |
|-------|-----------|-------------|
|Treatment given | Int | The type of treatment given to a patient .i.e|   
|Procedures done| String | Name of procedure|
|Follow up plan| String | The follow up plan |
|Referral facility| String| Name of the referral facility |


### Outcome

- Outcome details      

| Field | Data Type | Description |
|-------|-----------|-------------|
|Outcome | String | Outcome name|   
|Date of outcome| Date | Outcome date|       



[IDSR API](
https://idsr-backend.onrender.com/api/cases/)

---

### Maintainer

Tuntufye Mwanyongo     



