# CleanCity Waste Pickup Scheduler - Test Plan
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
- [x] Verify that installations exist:

  
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
- **Repository URL**: [https://github.com/PLP-Database-Design/wk-6-jackiecherotich-1.git](The repository we are using as members)
- **Access Level**: All team members have been granted contributor access
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

### 9.  Sign-off

### Phase 1 Completion
| Task |	Owner	| Status |	Date |
|:-----------:| :----------: | :---------:| :----:|
| Repository Setup|	Amobigold |	completed |	3/11/2025	|
| Jira Board	| Jackline | completd	|4/11/2025|
| Test Plan	| Magret | completed |	5/11/2025 |
| Final Review |	Team	| completed |	5/11/2025 |

### Phase 2 Completion
| Task |	Owner	| Status |	Date |
|:-----------:| :----------: | :---------:| :----:|
| Repository Setup|	Amobigold |	completed |	|
| Jira Board	| Jackline | completd	| |
| Test Plan	| Magret | completed |	 |
| Final Review |	Team	| completed |	|

### Final Sign-off
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Manager | Jackline |  |  |
| Test Executor | Amobigold |  |  |
| Risk Analyst | Magret Faith |  |  |

---
*This test plan will be updated as needed throughout the project lifecycle. Last updated: November 6, 2025*

