# Vocabularies by Domain

Complete listing of all controlled vocabulary groups across every application in the portfolio. For cross-cutting analysis of shared concepts, see [Shared Patterns](shared-patterns.md).

---

## Research Administration -- OpenERA

OpenERA has the largest vocabulary footprint, reflecting the complexity of sponsored-program administration. All AllowedValue codes use `snake_case` naming.

### DocumentType (11 codes)

Categorizes documents attached to proposals and RFAs.

`proposal_narrative`, `budget_justification`, `biosketch`, `current_pending`, `facilities`, `data_mgmt`, `letter_support`, `rfa_document`, `subaward_docs`, `coi_disclosure`, `other`

### ProjectRole (10 codes)

Defines the role a person holds on a research project. Aligns with federal sponsor role definitions (e.g., NSF Senior Personnel categories).

`pi`, `co_pi`, `co_i`, `key_person`, `senior_person`, `postdoc`, `grad_student`, `undergrad`, `technician`, `consultant`

### ProjectType (7 codes)

Classifies the type of funded project.

`research`, `instruction`, `public_service`, `fellowship`, `equipment`, `conference`, `other`

### ContactType (4 codes)

Classifies the contact method for a person or organization.

`email`, `phone`, `fax`, `address`

### COIRelationship (6 codes)

Classifies the nature of a conflict of interest relationship.

`equity`, `consulting`, `board`, `ip`, `travel`, `other`

### FundType (3 codes)

Classifies the source category of project funding.

`sponsored`, `institutional`, `cost_share`

### TransactionType (4 codes)

Classifies financial transactions (reserved for post-award modules).

`expenditure`, `encumbrance`, `revenue`, `transfer`

### DeliverableType (5 codes)

Categorizes project deliverables (reserved for post-award modules).

`progress_report`, `final_report`, `financial_report`, `invention_report`, `other`

### ModEventType (7 codes)

Classifies award modification events (reserved for post-award modules).

`no_cost_ext`, `supplemental`, `budget_realloc`, `pi_change`, `scope_change`, `reduction`, `termination`

### ProposalCategory (3 codes)

Classifies proposals by submission type.

`full`, `preliminary`, `subproject`

### ProposalActionType (7 codes)

Classifies the action type of a proposal submission.

`new`, `renewal`, `continuation`, `supplement`, `revision`, `resubmission`, `transfer_in`

### AgreementType (5 codes)

Classifies the type of funding agreement.

`grant`, `cooperative`, `contract`, `subaward`, `other`

### CampusType (4 codes)

Classifies the campus or facility type for F&A rate determination.

`on_campus`, `off_campus`, `ag_research`, `ag_non_research`

### CampusLocation (5 codes)

Identifies the University of Idaho campus location.

`moscow`, `boise`, `cda`, `if`, `tf`

### SponsorRegulatory (8 codes)

Identifies federal regulatory frameworks applicable to a sponsor.

`dod`, `nist_sp800`, `cmmc`, `cui`, `doe`, `nasa`, `nih`, `nsf`

### ExportControl (8 codes)

Classifies export control risk factors.

`foreign_involvement`, `military_defense`, `pub_restrictions`, `foreign_national_id`, `work_outside_us`, `intl_travel`, `controlled_tech`, `uas_drone`

### ResearchInstitute (9 codes)

Identifies University of Idaho research institute affiliations.

`iids`, `imci`, `ari`, `iwrri`, `igs`, `caes`, `ihhe`, `ics`, `na`

### RequirementCategory (8 codes)

Categorizes requirements extracted from RFAs.

`document`, `formatting`, `eligibility`, `review_criterion`, `budget_constraint`, `submission`, `deadline`, `compliance`

### ChecklistStatus (4 codes)

Tracks the completion status of proposal checklist items.

`not_started`, `in_progress`, `complete`, `not_applicable`

### AppointmentType (15 codes)

Classifies personnel appointment types, used for APM 45.22 PI/Co-PI eligibility evaluation.

`tenured`, `tenure_track`, `non_tenure_track`, `research_faculty`, `extension_faculty`, `librarian_faculty`, `clinical_faculty`, `visiting_faculty`, `emeritus`, `postdoctoral_fellow`, `research_scientist`, `staff`, `graduate_student`, `undergraduate_student`, `external_collaborator`

### FacultyRank (9 codes)

Classifies faculty rank levels.

`professor`, `assoc_professor`, `asst_professor`, `lecturer`, `senior_lecturer`, `clinical_professor`, `research_sci_i`, `research_sci_ii`, `research_sci_iii`

### Check-Constrained Enums (RFA Analysis)

The RFA Analysis tables use SQL CHECK constraints instead of the AllowedValue pattern. These values are enforced at the database level and documented here for completeness.

#### Analysis_Type (5 codes)

Classifies the type of AI analysis run against an RFA document.

`comprehensive_checklist`, `ffr_checklist`, `eligibility_review`, `budget_review`, `custom`

#### Analysis_Status (4 codes)

Tracks the execution state of an analysis run.

`pending`, `completed`, `failed`, `superseded`

#### Section_Type (5 codes)

Discriminates how items within an analysis section are structured.

`key_value`, `table`, `rule_list`, `narrative`, `mixed`

#### Item_Type (7 codes)

Classifies extracted items for typed parsing into Parsed_Date, Parsed_Number, or Parsed_Boolean columns.

`text`, `date`, `currency`, `integer`, `boolean`, `duration`, `rule`

---

## Communications -- UCM Daily Register

UCM Daily Register manages the University of Idaho's faculty/staff and student newsletters. Its vocabulary is focused on editorial workflow and content classification.

### Submission_Category (7 codes)

Classifies the type of content submitted for newsletter inclusion.

`announcement`, `event`, `deadline`, `achievement`, `grant`, `resource`, `other`

### Newsletter_Type (2 codes)

Distinguishes between the two newsletters produced by the system.

`daily_register`, `myui`

### Target_Newsletter (3 codes)

Specifies which newsletter(s) a submission is intended for.

`tdr`, `myui`, `both`

### Submission_Status (7 codes)

Tracks a submission through the editorial pipeline from intake to publication.

`new`, `ai_edited`, `in_review`, `revision_requested`, `approved`, `scheduled`, `published`

### Newsletter_Status (5 codes)

Tracks a newsletter edition through assembly and distribution.

`draft`, `assembling`, `ready`, `sent`, `archived`

### Version_Type (3 codes)

Identifies the stage of an edit version in the AI editing pipeline.

`original`, `ai_suggested`, `editor_final`

### Headline_Case (2 codes)

Specifies the capitalization style applied to headlines.

`title_case`, `sentence_case`

### Rule_Set (3 codes)

Groups style rules into named sets for different editorial contexts.

`ap_style`, `ucm_house`, `accessibility`

### Severity (3 codes)

Indicates the severity of a style-rule violation detected during AI editing.

`error`, `warning`, `info`

### Schedule_Mode (2 codes)

Controls how newsletter publication timing is determined.

`automatic`, `manual`

---

## Internal Audit -- Audit Dashboard

The Audit Dashboard supports the University of Idaho's internal audit function, tracking reports, observations, and corrective action items.

### ReportType (3 codes)

Classifies audit reports by their purpose and scope.

`ANNUAL`, `SPECIAL`, `FOLLOW_UP`

### ObservationStatus (4 codes)

Tracks an audit observation from initial documentation through resolution.

`DRAFT`, `OPEN`, `RESOLVED`, `CLOSED`

### ActionItemStatus (5 codes)

Tracks corrective action items assigned in response to audit observations.

`OPEN`, `IN_PROGRESS`, `COMPLETED`, `OVERDUE`, `CANCELLED`

### Severity (3 codes)

Rates the impact level of an audit finding.

`HIGH`, `MEDIUM`, `LOW`

### AssignmentRole (2 codes)

Defines the role of an auditor assigned to an engagement.

`LEAD`, `SUPPORT`

### Priority (3 codes)

Rates the urgency of addressing an audit finding, independent of severity.

`HIGH`, `MEDIUM`, `LOW`

### DocumentType (4 codes)

Classifies documents attached to audit engagements.

`REPORT`, `WORKPAPER`, `EVIDENCE`, `CORRESPONDENCE`

### ExtractionStatus (8 codes)

Tracks the AI-assisted extraction pipeline for processing audit documents via MindRouter OCR and LLM.

`PENDING`, `PROCESSING`, `EXTRACTED`, `REVIEWED`, `APPROVED`, `REJECTED`, `FAILED`, `ARCHIVED`

---

## Strategic Planning -- StratPlan Tactics

StratPlan Tactics is a JSON-file-backed application without a database. Its categorical values are defined inline rather than in an AllowedValue table. They are documented here for completeness.

!!! info "No AllowedValue table"
    These values are embedded in the application's JSON data files and React components. If StratPlan Tactics migrates to a database backend in the future, these should be formalized as AllowedValue groups.

### pillar_codes (5 codes)

Maps tactics to strategic plan pillars.

`access`, `engagement`, `discovery`, `community`, `culture`

### tactic_status (1 code)

Current implementation status of a tactic. Only one value is currently defined; additional statuses are expected as the application matures.

`on_track`

### alignment_level (3 codes)

Rates how strongly a tactic aligns with its parent strategic objective.

`high`, `medium`, `low`

### confidence (3 codes)

Rates the confidence level in a tactic's projected outcome.

`high`, `medium`, `low`

### roi_type (3 codes)

Classifies the expected return on investment for a tactic.

`cost_savings`, `revenue`, `efficiency`

### spigp_award_status (3 codes)

Tracks the status of SPIGP (Strategic Plan Implementation Grant Program) award applications.

`pending`, `awarded`, `declined`
