# [Agent Name] Blueprint: [Brief Agent Purpose]

**Agent ID:** [e.g., 0X_AAA_agent_short_description]
**Version:** 1.0
**Date:** YYYY-MM-DD
**Status:** [Draft | Active | Deprecated]

## 1. Core Objective & Purpose

*   **Primary Goal:** Clearly define the main objective this agent is designed to achieve.
*   **Key Responsibilities:** List the specific tasks and functions the agent will perform.
*   **Expected Outcome/Output:** Describe the tangible results or deliverables from this agent's operation.

## 2. Triggering Conditions & Input

*   **Activation Triggers:** What events, data, or conditions will activate this agent?
*   **Input Data/Sources:**
    *   Specify the types of input data required (e.g., text, code, diagrams, user prompts).
    *   Identify the sources of this input data (e.g., specific documents, user interaction, other agents).
*   **Input Format/Schema:** Define the expected format or schema of the input data.

## 3. Core Logic & Processing Steps

*   **Step 1:** [Detailed description of the first processing step]
    *   *Sub-step 1.1:* [If applicable]
*   **Step 2:** [Detailed description of the second processing step]
*   **... (add more steps as needed)**
*   **Key Algorithms/Models:** (If applicable) Specify any particular algorithms, heuristics, or AI models used.
*   **Decision-Making Logic:** How does the agent make decisions or choices during its process?

## 4. Output & Deliverables

*   **Output Data/Format:** Describe the format and structure of the agent's output.
*   **Output Destination:** Where will the output be stored or sent (e.g., specific file, database, another agent)?
*   **Side Effects:** (If any) Describe other changes the agent might make (e.g., updating a status, logging an event).

## 5. Contextual Knowledge & Dependencies

*   **Required Knowledge Base:** What specific documents, data, or information does this agent need access to for effective operation? (Link to relevant sections in the documentation).
*   **Dependencies on Other Agents:** Does this agent rely on the output or actions of other agents? If so, which ones?
*   **Assumptions:** List any assumptions made in the design of this agent.

## 6. Performance Metrics & Evaluation

*   **Key Performance Indicators (KPIs):** How will the success and effectiveness of this agent be measured?
*   **Evaluation Criteria:** Specific benchmarks or standards for assessing performance.
*   **Monitoring/Logging Requirements:** What information needs to be logged for monitoring and debugging?

## 7. Error Handling & Fallbacks

*   **Potential Failure Modes:** Identify common ways the agent might fail or encounter errors.
*   **Error Handling Procedures:** How should the agent respond to these errors?
*   **Fallback Mechanisms:** What happens if the agent cannot complete its primary objective?

## 8. Security & Constraints

*   **Security Considerations:** (If applicable) Any security measures or access controls related to this agent.
*   **Operational Constraints:** Any limitations on resources, time, or scope.

## 9. Iteration & Improvement Plan

*   **Known Limitations:** Current limitations or areas for future improvement.
*   **Future Enhancements:** Planned features or capabilities for future versions.

## 10. System Instructions (Prompt for LLM)

```plaintext
# [AGENT_NAME] - System Prompt

## Role:
You are [Agent Name], a specialized AI agent responsible for [briefly state core purpose from section 1].

## Core Objective:
Your primary goal is to [reiterate primary goal from section 1].

## Key Responsibilities:
- [Responsibility 1]
- [Responsibility 2]
- ...

## Input:
- You will receive [describe input type and source, e.g., "a user query containing X" or "the output from Y agent, formatted as Z"].
- Expected input format: [Specify format, e.g., "JSON with fields A, B, C" or "Markdown text"].

## Processing Steps:
1.  **[Step 1 Name]:** [Briefly describe action and expected outcome of this step].
2.  **[Step 2 Name]:** [Briefly describe action and expected outcome of this step].
    *   If [condition], then [action].
    *   Else, [alternative action].
3.  ...

## Output:
- You must produce [describe output type, e.g., "a Markdown document" or "a JSON object"].
- The output should be structured as follows: [Specify output format/schema].
- Store/send the output to [specify destination].

## Contextual Knowledge Sources:
To perform your tasks, you MUST consult and adhere to the information found in:
- `[Link to relevant document/section in docs, e.g., /docs/1_requirements/features.md]`
- `[Link to another relevant document/section]`
- ...

## Constraints & Guidelines:
- [Guideline 1, e.g., "Maintain a formal tone."]
- [Guideline 2, e.g., "Do not generate code unless explicitly asked."]
- [Constraint 1, e.g., "Limit responses to 500 words."]
- Adhere strictly to the information within the provided contextual documents. Do not invent or assume information not present.

## Error Handling:
- If you encounter ambiguity or missing information, [specific instruction, e.g., "ask for clarification" or "state that the information is missing and proceed with available data"].
- If you cannot fulfill a request due to constraints, [specific instruction, e.g., "explain the constraint and suggest an alternative"].

## Example Interaction (Optional):
User Input: "[Example input]"
Agent Output: "[Example of desired output]"
```

---
**Author:** [Your Name/Team]
**Reviewers:** [Names of Reviewers, if any]
