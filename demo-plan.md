# Knowledge Base Demo Plan & Evaluation Questions

## Overview

This document outlines demo scenarios and evaluation questions designed to showcase:
1. **Semantic similarity functions** for testing answer accuracy
2. **LLM-as-judge** for interpreting agent responses
3. **Azure AI Foundry evaluations** for testing agents

The demo uses Meridian Strategic Consulting's knowledge base to demonstrate realistic business scenarios where users would query an internal knowledge system.

---

## Demo Scenario Categories

### 🎯 **Scenario 1: New Employee Onboarding**
*Target Audience*: HR managers, new employees  
*Use Case*: New consultant needs to understand company structure and processes

### 🎯 **Scenario 2: Proposal Development**
*Target Audience*: Sales teams, practice leaders  
*Use Case*: Preparing a competitive proposal for a client engagement

### 🎯 **Scenario 3: Expert Identification**
*Target Audience*: Project managers, resource planning  
*Use Case*: Finding the right consultant for a specific project

### 🎯 **Scenario 4: Client Research**
*Target Audience*: Business development, consultants  
*Use Case*: Understanding industry trends and competitive positioning

### 🎯 **Scenario 5: Project Execution**
*Target Audience*: Project teams, practice leaders  
*Use Case*: Following established methodologies and best practices

---

## Evaluation Questions & Reference Answers

### 📋 **Category 1: Company Information & Structure**

#### Question 1.1: Basic Company Information
**User Query**: "What is Meridian Strategic Consulting's mission statement and when was it founded?"

**Reference Answer**: 
```
Meridian Strategic Consulting was founded in 2018. Our mission is to empower organizations to achieve breakthrough performance through innovative strategies, data-driven insights, and collaborative partnerships that create lasting value for all stakeholders. We are a premier management consulting firm specializing in digital transformation, operational excellence, and strategic planning, partnering with Fortune 500 companies and emerging growth businesses.
```

**Evaluation Criteria**:
- Must include founding year (2018)
- Must include complete or paraphrased mission statement
- Should mention core service areas (digital transformation, operational excellence, strategic planning)

#### Question 1.2: Leadership Structure
**User Query**: "Who are the senior partners at Meridian and what are their areas of expertise?"

**Reference Answer**:
```
Meridian's senior leadership includes:
- Sarah Chen: Managing Partner & CEO, expertise in digital transformation strategy, technology leadership, and organizational scaling
- Michael Rodriguez: Senior Partner for Strategy Practice, specializing in strategic planning, M&A advisory, and market entry with focus on manufacturing, energy, and automotive industries
- Dr. Amanda Foster: Senior Partner for Digital Transformation, expert in AI/ML, cloud architecture, cybersecurity, with technical certifications in AWS, Azure, and Google Cloud
```

**Evaluation Criteria**:
- Must include all three senior partners with correct names and titles
- Must include their primary expertise areas
- Bonus points for specific industry focus or technical certifications

#### Question 1.3: Organizational Metrics
**User Query**: "How many employees does Meridian have and what is their client retention rate?"

**Reference Answer**:
```
Meridian Strategic Consulting has 450+ consultants and staff members. The company has served 200+ organizations across 15+ major sectors with a 94% client retention rate. They maintain an average project ROI of 340% and have office locations in Chicago (headquarters), New York, San Francisco, Austin, Atlanta, London, and Toronto.
```

**Evaluation Criteria**:
- Must include employee count (450+)
- Must include client retention rate (94%)
- Should include additional metrics like client count, ROI, or office locations

### 💼 **Category 2: Service Offerings & Capabilities**

#### Question 2.1: Service Portfolio
**User Query**: "What are the main practice areas at Meridian and what services do they offer?"

**Reference Answer**:
```
Meridian has five main practice areas:
1. Strategy & Planning: Strategic planning, market entry, M&A advisory, competitive positioning
2. Digital Transformation: Technology strategy, AI implementation, cloud migration, cybersecurity
3. Operations Excellence: Process optimization, supply chain management, lean manufacturing, cost reduction
4. People & Change: Organizational design, change management, leadership development, culture transformation
5. Data & Analytics: Business intelligence, predictive analytics, performance management systems

Each practice offers both consulting services and implementation support with typical project durations ranging from 8-24 weeks.
```

**Evaluation Criteria**:
- Must list all five practice areas correctly
- Must include 2-3 key services for each practice area
- Should mention implementation focus or project timelines

#### Question 2.2: Digital Transformation Capabilities
**User Query**: "What specific AI and automation services does Meridian offer, and what kind of ROI can clients expect?"

**Reference Answer**:
```
Meridian offers comprehensive AI & Automation Implementation services including AI opportunity assessment, solution design and architecture, implementation and testing, and change management support. These engagements typically last 16-28 weeks with teams of 5-10 consultants. Clients can expect a typical ROI of 400-600%, making this one of our highest-value service offerings. Dr. Amanda Foster leads this practice with expertise in machine learning, having 12 patents in ML and automation, and the team has delivered $500M+ in client value through AI implementations.
```

**Evaluation Criteria**:
- Must mention AI/automation services and components
- Must include ROI range (400-600%)
- Should include team size, duration, or leadership details
- Bonus for specific value delivered or credentials

#### Question 2.3: Industry Expertise
**User Query**: "What industries does Meridian specialize in and who leads each vertical?"

**Reference Answer**:
```
Meridian has deep expertise across six major industries:
- Healthcare & Life Sciences: Led by Dr. Amanda Foster, 35 consultants, serving 15 healthcare systems and 8 pharmaceutical companies
- Financial Services: Led by Sarah Chen, 42 consultants, serving 12 banks, 6 insurance companies, and 4 fintech firms
- Manufacturing & Industrial: Led by Michael Rodriguez, 38 consultants, serving 20 manufacturing companies and 8 automotive suppliers
- Technology & Software: Led by Dr. Amanda Foster, 45 consultants, serving 25 technology companies and 12 startups
- Energy & Utilities: Led by Michael Rodriguez, 28 consultants, serving 8 utilities and 6 energy companies
- Government & Public Sector: Led by Patricia Williams, 22 consultants, serving 5 federal agencies and 12 state/local governments
```

**Evaluation Criteria**:
- Must list major industries with correct vertical leads
- Should include team sizes and client counts
- Bonus for specific client types or sub-sectors

### 👥 **Category 3: People & Expertise**

#### Question 3.1: Expert Identification
**User Query**: "I need a consultant with AI/ML expertise and healthcare industry experience for a 6-month project. Who would be the best match?"

**Reference Answer**:
```
Dr. Amanda Foster would be the ideal match for this project. She is a Senior Partner with expertise in AI/ML and leads both the Digital Transformation practice and Healthcare vertical. She has a PhD in Computer Science from Carnegie Mellon, holds 12 patents in machine learning and automation, and has led AI implementations generating $500M+ in client value. She has specific healthcare experience with projects including AI-powered diagnostic tools, predictive analytics for patient outcomes, and clinical decision support systems. However, she is currently available starting February 2025, so timeline coordination would be needed.
```

**Evaluation Criteria**:
- Must identify Dr. Amanda Foster as the best match
- Must mention her AI/ML and healthcare expertise
- Should include relevant credentials or experience
- Bonus for mentioning availability constraints

#### Question 3.2: Team Composition
**User Query**: "What would be the typical team structure for a $1.5M digital transformation project?"

**Reference Answer**:
```
For a $1.5M digital transformation project, the typical team structure would include:
- 1 Partner for overall project leadership and client relationship management
- 1-2 Principals for day-to-day project management and delivery
- 2-3 Senior Managers for specific workstream leadership
- 4-6 additional consultants (Managers and Senior Consultants)

The project would likely run 16-24 weeks with the Partner at 60% utilization, Principals at 70%, and Senior Managers at 75%. Given the digital transformation focus, Dr. Amanda Foster would likely be the Partner lead, with Kevin Liu (Principal, Cloud & Infrastructure) as a key team member.
```

**Evaluation Criteria**:
- Must provide realistic team structure and sizing
- Should include utilization rates or timeline estimates
- Must identify appropriate expertise for digital transformation
- Bonus for specific individual recommendations

#### Question 3.3: Skills and Certifications
**User Query**: "What cloud certifications do Meridian consultants have, and who has the most technical expertise?"

**Reference Answer**:
```
Meridian has strong cloud certification coverage:
- AWS Solutions Architect Professional: Dr. Amanda Foster, Kevin Liu
- Microsoft Azure Solutions Architect: Dr. Amanda Foster, Kevin Liu  
- Google Cloud Professional Architect: Dr. Amanda Foster, Kevin Liu

Dr. Amanda Foster has the most comprehensive technical expertise with certifications across all three major cloud platforms, plus CISSP for cybersecurity. Kevin Liu is the Principal for Cloud & Infrastructure with 10 years of experience and specializes in multi-cloud architecture, Kubernetes, and DevOps. The firm also has additional consultants with intermediate-level cloud skills including Sarah Chen, David Kumar, and Maria Santos.
```

**Evaluation Criteria**:
- Must list specific cloud certifications and certified individuals
- Must identify Dr. Amanda Foster as having the most technical expertise
- Should mention Kevin Liu's role and specialization
- Bonus for additional context on other team members

### 📊 **Category 4: Market Intelligence & Strategy**

#### Question 4.1: Industry Trends
**User Query**: "What are the current trends in AI consulting and what growth rates is the market seeing?"

**Reference Answer**:
```
The AI consulting market is experiencing exceptional growth at 45% CAGR, with the global market reaching $47B in 2024 (+52% YoY). Key trends include enterprise AI adoption reaching 65% of large organizations, generative AI expanding beyond content creation, and AI governance becoming a board-level priority. Client demand patterns show high demand for AI strategy development and implementation roadmaps, emerging demand for AI risk management and algorithmic auditing, and future demand anticipated for quantum AI and autonomous business processes. Meridian is well-positioned with Dr. Amanda Foster's expertise and 15+ successful AI implementations.
```

**Evaluation Criteria**:
- Must include growth rate (45% CAGR) and market size ($47B)
- Must mention key trends in enterprise adoption and governance
- Should include demand patterns and Meridian's positioning
- Bonus for specific statistics or future trends

#### Question 4.2: Competitive Positioning
**User Query**: "How does Meridian position itself against the Big Four consulting firms?"

**Reference Answer**:
```
Meridian positions itself as providing better value and personalized service compared to the Big Four, with rates typically 10-20% lower than Big Four firms. Key differentiators include:
- Partner-level attention rather than junior consultants following rigid methodologies
- Boutique service model with customized solutions
- Implementation focus ensuring strategies become reality
- Superior expertise in specialized areas with proven methodology
- 94% client satisfaction vs. industry averages
- Average project ROI of 340% demonstrating measurable value

The value proposition emphasizes that while rates are competitive, clients receive senior-level expertise and outcomes-focused delivery.
```

**Evaluation Criteria**:
- Must mention rate comparison (10-20% lower)
- Must include key differentiators like partner attention and customization
- Should include performance metrics (94% satisfaction, 340% ROI)
- Bonus for specific value proposition messaging

#### Question 4.3: Market Opportunities
**User Query**: "What are the fastest-growing consulting segments and how is Meridian positioned for them?"

**Reference Answer**:
```
The fastest-growing consulting segments through 2027 are:
1. AI and automation consulting: 35-40% CAGR
2. Sustainability and ESG: 25-30% CAGR  
3. Cybersecurity transformation: 20-25% CAGR
4. Future of work: 18-22% CAGR

Meridian is well-positioned for AI/automation with Dr. Amanda Foster's leadership and proven track record. The firm is developing sustainability practice capabilities and has strong cybersecurity expertise. Strategic recommendations include expanding AI consulting capabilities through targeted hiring, developing sustainability practice with ESG focus, and creating outcome-based pricing pilot programs to capture value-based fees in high-growth segments.
```

**Evaluation Criteria**:
- Must list top growth segments with correct CAGR ranges
- Must assess Meridian's current positioning in each area
- Should include strategic recommendations for growth
- Bonus for specific capability gaps or investment priorities

### 🛠️ **Category 5: Methodologies & Project Execution**

#### Question 5.1: Project Methodology
**User Query**: "What is Meridian's standard project methodology and what are the key phases?"

**Reference Answer**:
```
Meridian uses the proprietary Meridian Strategic Methodology (MSM), a five-phase framework:

Phase 1: Discover & Diagnose (Weeks 1-3) - Understand current state and identify root causes
Phase 2: Design & Develop (Weeks 4-8) - Create future state vision and solution architecture  
Phase 3: Plan & Prepare (Weeks 9-12) - Develop detailed implementation plans and prepare for execution
Phase 4: Execute & Implement (Weeks 13-20) - Execute solution and manage transformation
Phase 5: Optimize & Sustain (Weeks 21-24) - Optimize performance and ensure sustainable results

Each phase has specific success criteria, quality gates, and deliverables. The methodology emphasizes fact-based decision making, collaborative partnership, implementation focus, and continuous learning.
```

**Evaluation Criteria**:
- Must list all five phases with correct names and week ranges
- Must include brief description of each phase objective
- Should mention core principles or quality gates
- Bonus for specific success criteria or methodology adaptations

#### Question 5.2: Best Practices
**User Query**: "What are Meridian's best practices for digital transformation projects?"

**Reference Answer**:
```
Meridian's digital transformation best practices include:

1. Prioritize User Experience: Design solutions with end-user needs as primary consideration, conduct user testing throughout development, create intuitive interfaces requiring minimal training (results in 70% higher user adoption rates)

2. Implement in Phases: Break large transformations into manageable phases, deliver value early and often, use lessons from each phase to improve subsequent ones (results in 45% faster time-to-value)

3. Data-Driven Decision Making: Establish baseline metrics before implementation, create real-time dashboards for monitoring, use A/B testing for optimization (results in 30% better performance outcomes)

4. Start with Leadership Alignment: Ensure visible and consistent leadership support, align leadership team on vision and messaging (results in 80% higher change success probability)
```

**Evaluation Criteria**:
- Must include multiple specific best practices with descriptions
- Must include quantified impact/results for each practice
- Should cover both technical and change management aspects
- Bonus for additional practices or implementation details

#### Question 5.3: Quality Standards
**User Query**: "What quality standards and success metrics does Meridian use for projects?"

**Reference Answer**:
```
Meridian maintains rigorous quality standards across all projects:

Quality Standards:
- Deliverable Quality: All deliverables must meet defined quality criteria
- Process Adherence: All processes must follow established methodologies  
- Client Satisfaction: Minimum 4.0/5.0 rating required at each gate
- Performance Achievement: Minimum 90% of projected benefits realized

Success Metrics:
- On-time Delivery: Target 95% of milestones delivered on schedule
- Budget Adherence: Target less than 5% variance from approved budget
- Client Satisfaction: Target average rating of 4.5/5.0 or higher
- Benefits Realization: Target 90% or more of projected benefits achieved

The firm maintains a 94% project success rate with 98% timeline adherence across all engagements.
```

**Evaluation Criteria**:
- Must include quality standards with specific criteria
- Must include success metrics with target percentages
- Should mention overall performance statistics
- Bonus for quality review processes or escalation procedures

### 💰 **Category 6: Pricing & Commercial Terms**

#### Question 6.1: Pricing Structure
**User Query**: "What are Meridian's standard consulting rates by level?"

**Reference Answer**:
```
Meridian's standard rates (effective October 2024) are:
- Senior Partner: $5,500/day ($27,500/week)
- Partner: $4,500/day ($22,500/week)  
- Principal: $3,200/day ($16,000/week)
- Senior Manager: $2,400/day ($12,000/week)
- Manager: $1,800/day ($9,000/week)
- Senior Consultant: $1,200/day ($6,000/week)
- Consultant: $800/day ($4,000/week)

Specialized roles command premium rates: Industry experts (+25%), Technology architects (+20%), Certified specialists (+15%), Former executives (+30%). The firm offers various pricing models including time & materials, fixed price, value-based pricing, and retainer arrangements.
```

**Evaluation Criteria**:
- Must include daily/weekly rates for multiple levels
- Should mention premium rates for specialized roles
- Must include different pricing model options
- Bonus for specific premium percentages or model descriptions

#### Question 6.2: Value Proposition
**User Query**: "How does Meridian justify its premium pricing compared to other consulting firms?"

**Reference Answer**:
```
Meridian justifies premium pricing through demonstrated value delivery:

- Average project ROI of 340% vs. industry averages
- 94% client satisfaction rating and 94% client retention rate
- Partner-level attention vs. junior consultant delivery at larger firms
- Specialized expertise with proven methodologies and 200+ successful projects
- Implementation focus ensuring strategies are executed, not just developed
- Boutique service model allowing customized solutions vs. rigid frameworks

Value-based pricing captures 8-15% of first-year benefits, with typical fees representing 120% of cost-based pricing but delivering 3x higher ROI than alternative approaches. The firm's track record shows 90% of clients achieve projected benefits within 12 months.
```

**Evaluation Criteria**:
- Must include quantified value metrics (ROI, satisfaction, retention)
- Must explain value differentiators vs. competitors
- Should mention value-based pricing approach
- Bonus for specific value capture rates or benefit realization statistics

---

## Evaluation Frameworks

### 🎯 **Semantic Similarity Testing**

**Purpose**: Measure how closely the agent's response matches the reference answer in meaning and content coverage.

**Implementation**:
```python
# Example semantic similarity evaluation
def evaluate_semantic_similarity(reference_answer, agent_response):
    # Use embedding models to compare semantic similarity
    similarity_score = cosine_similarity(
        embed_text(reference_answer),
        embed_text(agent_response)
    )
    
    # Define thresholds
    if similarity_score >= 0.85:
        return "Excellent"
    elif similarity_score >= 0.75:
        return "Good" 
    elif similarity_score >= 0.65:
        return "Satisfactory"
    else:
        return "Needs Improvement"
```

**Evaluation Criteria**:
- **Excellent (0.85+)**: Covers all key points with accurate details
- **Good (0.75-0.84)**: Covers most key points with minor omissions
- **Satisfactory (0.65-0.74)**: Covers basic information but lacks detail
- **Needs Improvement (<0.65)**: Missing key information or contains inaccuracies

### 🤖 **LLM-as-Judge Evaluation**

**Purpose**: Use an LLM to assess the quality, accuracy, and completeness of agent responses.

**Judge Prompt Template**:
```
You are an expert evaluator assessing the quality of responses from a knowledge base system. 

REFERENCE ANSWER:
{reference_answer}

AGENT RESPONSE:
{agent_response}

EVALUATION CRITERIA:
1. Accuracy: Are the facts and figures correct?
2. Completeness: Does it cover all key points from the reference?
3. Clarity: Is the response clear and well-structured?
4. Relevance: Does it directly answer the user's question?

Rate each criterion on a scale of 1-5 and provide an overall score with justification.

OUTPUT FORMAT:
Accuracy: X/5
Completeness: X/5  
Clarity: X/5
Relevance: X/5
Overall: X/5
Justification: [Detailed explanation]
```

**Scoring Rubric**:
- **5**: Exceptional - Exceeds expectations
- **4**: Good - Meets expectations with minor gaps
- **3**: Satisfactory - Adequate but room for improvement
- **2**: Poor - Significant issues or gaps
- **1**: Unacceptable - Major problems or inaccuracies

### 🏭 **Azure AI Foundry Evaluation**

**Purpose**: Leverage Azure AI Foundry's built-in evaluation capabilities for comprehensive testing.

**Evaluation Metrics**:
1. **Groundedness**: How well-grounded is the response in the source material?
2. **Relevance**: How relevant is the response to the user's query?
3. **Coherence**: How coherent and well-structured is the response?
4. **Fluency**: How fluent and natural is the language?
5. **Custom Metrics**: Business-specific metrics like compliance with company tone

**Evaluation Dataset Structure**:
```json
{
  "test_cases": [
    {
      "query": "What is Meridian Strategic Consulting's mission statement?",
      "reference_answer": "Meridian's mission is to empower organizations...",
      "context": ["company-overview.md", "core-business documents"],
      "expected_metrics": {
        "groundedness": 5,
        "relevance": 5,
        "coherence": 4,
        "fluency": 4
      }
    }
  ]
}
```

**Batch Evaluation Setup**:
- **Test Set Size**: 50+ questions across all categories
- **Evaluation Frequency**: Weekly automated runs
- **Success Thresholds**: Groundedness >4.0, Relevance >4.2, Overall >4.0
- **Regression Testing**: Compare against baseline performance

---

## Demo Execution Plan

### 🎬 **Demo Flow Structure**

**Phase 1: Knowledge Base Overview (5 minutes)**
- Show knowledge base structure and content variety
- Highlight realistic business scenarios
- Demonstrate search and retrieval capabilities

**Phase 2: Semantic Similarity Demo (10 minutes)**
- Execute 3-5 test questions from different categories
- Show similarity scoring in real-time
- Compare high vs. low similarity examples
- Demonstrate threshold tuning

**Phase 3: LLM-as-Judge Demo (10 minutes)**
- Use same questions with LLM evaluation
- Show detailed scoring breakdown
- Compare LLM assessment vs. semantic similarity
- Highlight qualitative insights from judge

**Phase 4: Azure AI Foundry Demo (15 minutes)**
- Upload evaluation dataset
- Run batch evaluation with multiple metrics
- Show comprehensive dashboard and analytics
- Demonstrate regression testing capabilities

**Phase 5: Business Impact Discussion (10 minutes)**
- Discuss evaluation insights and improvements
- Show ROI of evaluation-driven optimization
- Connect to business value and user satisfaction

### 🎯 **Success Metrics for Demo**

**Technical Metrics**:
- Semantic similarity scores >0.75 for 80%+ of questions
- LLM-as-judge overall scores >4.0 for 85%+ of questions  
- Azure AI Foundry groundedness >4.0 for 90%+ of questions

**Business Metrics**:
- Response accuracy improvement over time
- User satisfaction correlation with evaluation scores
- Cost reduction through automated evaluation vs. manual review

**Engagement Metrics**:
- Audience understanding of evaluation concepts
- Questions and discussion quality
- Interest in implementation and next steps

---

## Additional Demo Scenarios

### 🔍 **Complex Multi-Document Queries**

**Query**: "For a healthcare digital transformation project worth $2M, who should lead the team, what methodology should we use, and what ROI can the client expect?"

**Expected Response Integration**:
- Expert identification from people-expertise docs
- Methodology from methodologies docs  
- ROI data from service-offerings docs
- Healthcare-specific considerations from industry-expertise docs

### 🔄 **Conflicting Information Testing**

**Query**: "What's Meridian's employee count?" (testing consistency across documents)

**Expected Challenge**: Ensure consistent numbers across company-overview and organizational-structure docs

### 📈 **Trend Analysis Queries**  

**Query**: "How should Meridian position itself for the AI consulting boom based on current market trends and our capabilities?"

**Expected Integration**:
- Market trends from intelligence docs
- Current capabilities from expert profiles
- Strategic recommendations synthesis

---

This comprehensive demo plan provides realistic scenarios, measurable evaluation criteria, and clear business value demonstration for your knowledge base evaluation system.