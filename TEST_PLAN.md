# CleanCity Waste Pickup Scheduler - Test Plan

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Testing Approach](#2-testing-approach)
- [3. Test Environment](#3-test-environment)
- [4. Project Phases](#4-project-phases)
  - [Phase 1: Planning & Setup](#phase-1-planning--setup)
  - [Phase 2: Test Design & Early Execution](#phase-2-test-design--early-execution)
  - [Phase 3: Final Execution & Reporting](#phase-3-final-execution--reporting)
- [5. Team Setup](#5-team-setup)
  - [5.1 Roles & Responsibilities](#51-roles--responsibilities)
  - [5.2 Communication Plan](#52-communication-plan)
- [6. Jira Integration](#6-jira-integration)
  - [6.1 Setup](#61-setup)
  - [6.2 Access](#62-access)
- [7. Repository Access Instructions](#7-repository-access-instructions)
  - [7.1 Access Details](#71-access-details)
  - [7.2 Team Members with Access](#72-team-members-with-access)
- [8. Check Test Results](#8-check-test-results)
  - [8.1 Phase 1 Timeline](#81-phase-1-timeline)
- [9. Initial Guidelines](#9-initial-guidelines)
  - [Defect Management Framework](#defect-management-framework)
  - [Risk Identification](#risk-identification)
- [10. Sign-off](#10-sign-off)
- [Final Sign-off](#final-sign-off)

---

## 1. Introduction
This test plan outlines the testing strategy by team Sniffer for the CleanCity Waste Pickup Scheduler web application. The application is designed to help manage waste collection in African cities.


## 2. Testing Approach
- **Black-box Testing**: We are going to test without accessing the internal code to see how the app behaves
- **UI Testing**: Verify that the app is working well on all user interfaces 
- **Functional Testing**: Test all features and functions, see if they are working properly and as expected
- **Accessibility Testing**: Check for Web Content Accessibility Guidelines compliance and ensure they are well met for all users
- **Compatibility Testing**: Test across different browsers and devices

## 3. Test Environment
- **Browsers**: Chrome, Firefox, Edge
- **Devices**: Desktop (primary), Tablet, Mobile
- **Testing Tools**:
  - Selenium (for automated UI testing)
  - Jest (for unit and integration testing)
- **Code Quality**: SonarQube
- **Accessibility**: Windows Accessibility Tools
- **Version Control**: Git, GitHub
- **Project Management**: Jira
  
## 4. Project Phases
### Phase 1: Planning & Setup 

#### Objectives
- Set up local testing environment
- Create project board
- Complete test plan documentation
- Define team roles and communication plan
- Set up Jira integration

##### 1. Phase 1 Deliverables

**1.1 Repository Setup**

- [x]  Fork the main repository to team's GitHub account
- [x]  Ensure that each team member has cloned the  repository locally on their machine
- [x]  Verify repository structure from:
  - index.html
  - styles.css
  - script.js
  - src/ directory (for React version)
  - package.json
- [x]  Document repository access instructions

**1.2 Local Environment Setup**

- [x] Install all the required software:
  - Node.js v18+
  - npm or yarn
  - Git
- [x] Verify that installations exist

  
**1.3 Application Verification**

*HTML Version:*
- Open index.html in browser
- Verify home page loads without errors
- Check navigation between pages

*React Version:*
- Verify app runs on http://localhost:3000
- Check all pages load correctly
- Document any setup issues

**1.4 Project Board Setup**
- [x] Create Jira board
- [x] Configure columns:
- Backlog → To Do → In Progress → Code Review → Testing → Done
- [x] Create initial tasks for Phase 1
- [x] Invite team members
- [x] Set up labels and components

**1.5 Test Plan Documentation**
- [x] Complete this test plan
- [x] Include all required sections
- [x] Get team approval
- [x] Upload to repository
- [x] Team Double check and make final changes

### 5. Team Setup

#### 5.1 Roles & Responsibilities

| Role |	Name	| Responsibilities |
|:--------:|:-----:|:-------:|
| Test Manager	| Jackline|	Oversee testing, track progress |
| Risk Analyst	| Magret	| Identify and manage risks |
| Test Executor | Amobigold	| Execute tests, report issues |

#### 5.2 Communication Plan
| Tool| Purpose| Timeline| Notes| 
|----------|-------------|-------------| -------------|
| WhatsApp group |Daily updates | Anytime |Immediate issue reporting |
| Jira | Task tracking,bug reporting, progress monitoring | As needed|
|	Google Meet |	Weekly sync | Fridays, Sundays, Tuesdays 5:00 PM EAT/2:00 PM WAT | Quick standups|

### 6. Jira Integration

#### 6.1 Setup
- [x] Create Jira project
- [x] Configure issue types and workflow
- [x] Set up GitHub integration
- [x] Configure notification schemes
  
#### 6.2 Access

- [x] Add team members
- [x] Set permissions
- [x] Verify all members can access and use Jira

### 7. Repository Access Instructions

#### 7.1 Access Details
- **Repository**: [CleanCity Waste Scheduler repo for the members](https://github.com/PLP-Database-Design/wk-6-jackiecherotich-1.git)
- **Type**: Forked GitHub repository from the main one
- **Access**: Team members only (contributor access required)
- **Access Level**: All team members have been granted full access
- **Branching Strategy**:
  - `main` - Production-ready code
  - `develop` - Development branch
  - `feature/*` - Feature branches
  - `bugfix/*` - Bug fix branches

#### 7.2 Team Members with Access
1. Jackline (Test Manager)
2. Amobigold (Test Executor)
3. Magret (Risk Analyst)

### 8. Check test results
  
Phase 1 is complete when:
1.	 Repository is forked and cloned
2.	Project board is created and shared
3.	 Test plan is completed
4.	Team roles are defined
5.	Communication plan is set
6.	 Jira integration works

#### 8.1 Phase 1 Timeline

- November 3 , 2025 Repository and environment setup
- November 4 , 2025 Jira board and test plan documentation
- November 5, 2025 Final verification and submission

### 9. Initial Guidelines

#### Defect Management Framework
- **Severity Levels**:
  - Critical: Blocks testing or causes system crash
  - High: Major functionality broken
  - Medium: Minor functionality issues
  - Low: Cosmetic or minor UI issues

- **Priority Levels**:
  - P1: Must fix immediately
  - P2: Should be fixed in current release
  - P3: Can be fixed in next release
  - P4: Enhancement for future consideration

#### Risk Identification
1. **Incomplete Requirements**
   - Impact: May lead to incomplete test coverage
   - Mitigation: Document assumptions, seek clarifications

2. **Environment Issues**
   - Impact: Delays in testing
   - Mitigation: Set up environments early, document configurations

3. **Test Data Limitations**
   - Impact: Incomplete test coverage
   - Mitigation: Create comprehensive test data sets

4. **Time Constraints**
   - Impact: Rushed testing
   - Mitigation: Prioritize test cases, focus on critical paths

### 10. Sign-off

### Phase 1 Completion
| Task |	Owner	| Status |	Date |	Initials |
|:-----------:| :----------: | :---------:| :----:|
| Repository Setup|	Amobigold |	completed |	3/11/2025	|
| Jira Board	| Jackline | completd	|4/11/2025|
| Test Plan	| Team | completed |	5/11/2025 |
| Final Review |	Team	| completed |	5/11/2025 |

### Phase 2: Test Design & Early Execution 

#### Key Activities:
- [x] Draft test cases and checklists
- [x] Develop early manual/automated test scripts
- [x] Create initial defect log

#### Defect Management
- [x] Implement defect logging process in Jira
- [x] Log initial defects with severity levels
- [x] Begin tracking defect metrics

#### Risk Monitoring
- [x] Review initial risks
- [x] Update mitigation strategies
- [x] Identify any new risks

#### Phase 2 Timeline
- **November 6-8, 2025**: Draft test cases and checklists
- **November 9-10, 2025**: Develop test scripts
- **November 11, 2025**: Complete initial defect log and review

#### Phase 2 Completion:
| Task | Owner | Status | Date | Initials |
|:----|:-----:|:------:|:----:| :-----:|
| Test Cases & Checklists | Amobigold Sikirat | Completed | 11/11/2025 | AS |
| Test Scripts | Jackline Cherotich | Completed | 11/11/2025 | JC |
| Initial Defect Log | Magret Faith | Completed | 11/11/2025 | MF |
| Review & Approval | Team Members | Completed | 11/11/2025 | Team |

### Phase 2 is complete when:
1. Test cases and checklists are drafted and reviewed by the team
2. Initial test scripts (manual/automated) are developed and validated
3. Defect logging process is implemented in Jira
4. Initial defects are logged with proper severity levels
5. All team members have completed their assigned Phase 2 tasks
6. Phase 2 review meeting is conducted and signed off by all team members

### Phase 3: Final Execution & Reporting

#### Key Activities:
- [ ] Complete test execution with evidence
- [ ] Update defect log with severity/priority
- [ ] Prepare final report with executive summary

#### Final Defect Management
- [ ] Verify all defects are properly categorized
- [ ] Ensure all critical/high severity issues are resolved
- [ ] Document any remaining known issues

#### Risk Assessment
- [ ] Final review of all identified risks
- [ ] Document effectiveness of mitigation strategies
- [ ] Update risk register for future reference

#### Phase 3 Timeline 
- **November 12-14, 2025**: Execute all test cases and gather evidence
- **November 15, 2025**: Finalize defect management and risk assessment
- **November 16, 2025**: Complete final report and obtain sign-off

#### Phase 3 Completion:
| Task | Owner | Status | Date | Initials |
|:----|:-----:|:------:|:----:| :-----:|
| Test Execution | Amobigold Sikirat | | | |
| Defect Management | Magret Faith | | | |
| Final Report | Jackline Cherotich | | | |
| Sign-off | Team Members | | | |

### Phase 3 is complete when:
1. All test cases have been executed and evidence is properly documented
2. Defect log is fully updated with severity and priority for all issues
3. Final test report with executive summary is prepared and reviewed
4. All critical and high severity defects are resolved or have mitigation plans
5. Final risk assessment is completed and documented
6. All team members have completed their assigned Phase 3 tasks
7. Final review meeting is conducted and project is signed off by all stakeholders

### Final Sign-off
| Role | Name | Signature | Date | Initials |
|------|------|-----------|------| :-----:|
| Test Manager | Jackline Cherotich |  |  |  |
| Test Executor | Amobigold Sikirat |  |  |  |
| Risk Analyst | Magret Faith |  |  |  |

---
*This test plan will be updated as needed throughout the project lifecycle. Last updated: November 6, 2025*

