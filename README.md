# IDSR API

- IDSR API is an integrated disease surveillance response api which is based on the IDSR World health organisation form. It contains all the categories of the IDSR WHO form as separate services.

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

[IDSR API](
https://idsr-backend.onrender.com/api/cases/)



