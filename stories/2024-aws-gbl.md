## AWS: Game-Based Learning (Skill Builder)

### Unblocking Large-Scale Catalog Classification Under Cross-Team Dependencies

**Context**

Ahead of launching a new internal catalog, **100+ game-based learning courses** needed to be manually categorized with specific labels. The final classification depended on input from a product owner in a neighboring team, and repeated delays put the launch timeline at risk.

**Goal**

Ensure catalog data was ready on time despite a high-risk, manual dependency on a non-engineering stakeholder.

**Approach**  
- Built a script to collect and normalize metadata across all courses, generating a spreadsheet pre-filled with most required fields.
- Analyzed the dataset and identified **repeating patterns** across courses that made full manual classification unnecessary and error-prone.
- Aligned with my manager on defining **default classifications and shortcuts**, allowing labels to be suggested programmatically instead of filled manually.
- Reduced the remaining work from full data entry to **targeted review and adjustment**.
- When async follow-ups continued to stall progress, escalated early and switched to **short, synchronous working sessions**, staying available to unblock decisions in real time.

**Outcome**  
- Completed categorization within a few focused sessions, unblocking the catalog launch on schedule.
- Reduced manual effort across **100+ items** to a review-driven workflow.
- Minimized risk of inconsistent or incorrect labeling.
- Demonstrated effective ownership in navigating cross-team, non-engineering dependencies through automation and timely escalation.

---

### Delivering a New Public User Profile Page as a Full-Stack Owner

**Context**  
The team needed a new **public-facing user profile page** to showcase achievements across game-based learning courses. The existing UI was outdated, inconsistent, and not reusable, so the decision was made to replace it entirely.

**Goal**  
Deliver a production-ready profile page from **Figma design to deployment**, reusing existing APIs while adopting a modern frontend stack, within a tight timeline.

**Approach**  
- Took end-to-end ownership despite a primarily backend background.
- Reused existing backend APIs, focusing effort where the gap was largest: frontend implementation.
- Ramped up quickly on the team’s frontend stack and translated Figma designs into a **React + TypeScript** application styled with **Tailwind CSS**.
- Integrated the frontend with AWS infrastructure (Cognito, CloudFront, API Gateway, Lambda, DynamoDB) defined via **CDK**.
- Iterated closely with design and product to validate layout, data presentation, and usability.

**Outcome**  
- Delivered a new public profile experience that clearly visualized user progress across multiple courses.
- Replaced a legacy UI with a clean, maintainable frontend, improving usability and future extensibility.
- Expanded scope from backend-focused work to **full-stack delivery within 3 months**.
- Provided a reusable foundation for future Skill Builder profile enhancements.

---

### Enabling LinkedIn Sharing with Reliable Achievement Previews

**Context**  
Users wanted to share learning achievements on LinkedIn, including a **badge image preview**. The profile page used a micro-frontend architecture where data was composed client-side, which conflicted with how social media crawlers generate previews.

**Goal**  
Enable reliable LinkedIn previews (title, description, badge image) without introducing security risks or destabilizing the existing frontend architecture.

**Approach**  
- Investigated LinkedIn’s preview mechanism and confirmed it relies on **server-generated Open Graph meta tags**, not client-side JavaScript.
- Identified a core limitation: achievement data was only available **after page load**, making it invisible to crawlers.
- Evaluated an event-based data propagation approach across micro-frontends, but rejected it due to added complexity and security concerns.
- Proposed and aligned on a simpler solution:
  - Consolidate the profile view into a **single server-rendered structure** for this page.
- Implemented server-side generation of Open Graph meta tags, embedding:
  - Badge image URL  
  - Title  
  - Description  
  directly in the HTML response.

**Outcome**  
- Enabled users to successfully share achievements on LinkedIn with correct badge image previews.
- Improved visibility and engagement for shared learning achievements.
- Simplified a complex micro-frontend interaction into a secure, maintainable solution.
- Avoided fragile client-side workarounds and ensured consistent behavior across social platforms relying on server-side metadata.
