## Executive Summary

A Spanish language school in Dar es Salaam is implementing a GenAI-powered learning platform to enhance educational delivery and support growth objectives. This document outlines the business requirements, technical considerations, and implementation strategy for the platform.

## Business Requirements

### Current Operations

The platform must support 300 active students while maintaining high-quality educational delivery and system responsiveness. The infrastructure will be self-hosted to ensure data privacy and cost control, with an initial hardware investment of $25,000-$35,000.

### Growth Objectives

The school aims to expand its student base significantly while maintaining educational quality. This growth strategy requires an infrastructure design that can accommodate increased usage without compromising performance or user experience.

## Functional Requirements:

The platform must support several key features at launch:

- The AI-powered Spanish Sentence Constructor study activity will assist students in forming correct Spanish sentences, providing grammar corrections and suggestions while explaining sentence structure in an interactive manner.
- The system will utilize a self-hosted Open-Source LLM responsible for query processing, response generation, and interactive learning assistance.
- Context Construction using Agentic RAG will enhance LLM responses by structuring and retrieving relevant context dynamically.
- Web Search Integration, filtered specifically for educational content, will provide real-world examples of Spanish sentence usage and act as a fallback for missing context.
- A Context Cache will store frequently accessed educational content to reduce redundant retrievals and improve system response time, while a Response Cache will store previously generated responses for quick retrieval.
- The platform will implement comprehensive security and compliance measures, including role-based access control, encrypted storage, and compliance with GDPR & FERPA regulations.

## Non-functional Requirements:

### Performance

Performance requirements center on optimized model execution to ensure efficient inference speeds with GPU acceleration. The system must maintain low latency response times, with AI generating responses within 3 seconds for optimal learning experience. Service level requirements specify 99.9% uptime during school hours and maximum response times of 5 seconds for complex queries.

### Security & Compliance

Data encryption will be implemented for all stored and transmitted student interactions. User authentication and access control systems will ensure only authorized students and staff can access the system. The platform will maintain strict compliance with data privacy laws including GDPR and FERPA.

### Usability

The platform will feature a simple and intuitive UI to enhance student engagement. Multi-device accessibility will ensure the platform functions effectively on desktops, tablets, and mobile devices.

### Scalability

While auto-scaling and load balancing are not required initially, the system should be designed to allow future growth with minimal disruptions.

## Risks

| Risk | Impact | Mitigation Strategy |
| --- | --- | --- |
| LLM performance degradation | Slower response times and potential inaccuracies | Optimize model execution and ensure hardware meets requirements |
| Limited internet access | Web search fallback may be unreliable | Ensure the **context cache** stores frequently needed knowledge |
| Security vulnerabilities | Unauthorized access or data breaches | Implement **role-based access control and encryption** |
| Model biases | AI-generated content may not align with curriculum | Continuously **monitor and fine-tune** model outputs |
| Limited initial funding for upgrades | Constraints on computing resources | Optimize model execution within the $25k-$30k budget |

## Assumptions

- The self-hosted LLM will meet performance and accuracy expectations within the **allocated $25k-$30k hardware budget**.
- Open-source models like **Mixtral 8x7B and IBM Granite** provide sufficient language capabilities.
- Students and educators **will actively use AI-powered study activities** to enhance learning.
- **Agentic RAG will improve query response accuracy** by structuring context dynamically.
- A **hybrid approach (self-hosting + web search fallback)** will provide up-to-date knowledge without excessive reliance on external sources.

## Constraints

- **Hardware Limitations**: The system must operate efficiently within the available computing resources (GPUs, CPUs, RAM).
- **Open-Source Model Compatibility**: The selected LLMs must be **self-hosted and optimized** for educational use cases.
- **No reliance on proprietary APIs**: The platform must avoid dependency on external proprietary AI services to maintain control and cost efficiency.
- **Compliance Requirements**: The platform must adhere to **GDPR & FERPA regulations**, ensuring student data privacy.

## Data Strategy

Our data strategy implements a comprehensive approach to managing educational content and student interactions. The system utilizes a vector database for efficient storage and retrieval of educational materials, supported by a multi-tier caching system:

The prompt cache stores prompts and their corresponding model outputs. Our response cache stores common interactions, reducing latency for repeated queries. The context cache retains relevant educational materials and student interaction history, optimizing retrieval times for personalized learning experiences.

## Technical Considerations

### **LLM Implementation**

We have selected two primary candidates for the LLM implementation:

**Mixtral 8x7B** serves as our primary choice due to its efficient architecture and multilingual capabilities. The model demonstrates superior performance in educational contexts while operating within our hardware constraints. Its mixture-of-experts architecture enables efficient resource utilization, making it ideal for our self-hosted environment.

https://huggingface.co/mistralai

IBM Granite provides an alternative option, offering specialized educational features and robust safety controls. Its transparent training data and established support ecosystem make it particularly attractive for educational implementations.

https://huggingface.co/ibm-granite

### Context Construction

- **Agentic RAG over Traditional RAG**: Retrieves structured, relevant knowledge dynamically for **better response coherence**.
- **Query Preprocessing Enhancements**: Standardizing prompt formatting. Normalizing input queries. Keeping API parameters consistent to leverage built-in prompt caching (avoiding a separate cache investment).
- **Web Search Integration** (Filtered for educational content): Provides up-to-date relevant information such as **language examples** and acts as a fallback for missing context.

### **Context Cache**

- **Caches frequently accessed learning materials** to minimize redundant web searches.
- Reduces repeated retrievals
- **Invalidation Rules**: Refreshes when new educational content is added.

### Prompt Cache

For models with prompt caching (if available and suitable), we can start with the built-in cache. It's the most pragmatic choice for the budget and scale. Only move to a separate caching solution if performance or cost becomes prohibitive *after* real-world testing.

## Infrastructure Design

The platform will operate on a dedicated Multi-GPU server configuration. This setup includes high-performance computing resources, dedicated storage systems, and redundant networking components. The infrastructure design prioritizes reliability and performance while maintaining data security.

## Future Considerations

### **Scalability & Infrastructure Upgrades**

- **User Capacity Growth**: Scale infrastructure to support 400**+ students**.
- **Potential for hardware upgrades**: Adding GPUs, storage, and memory to handle increased demand.
- **Implementing Auto-Scaling & Load Balancing** once the platform requires handling a larger user base.
- As the user base grows, **migrating to a containerized infrastructure** (e.g., Docker, Kubernetes) will improve scalability.
- **Cloud-based deployment options** (AWS, Azure, or private cloud) may be explored for multi-tenant expansion.

### **Expanding Study Activities & Learning Modalities**

- **New study activities** (e.g., speech to learn, writing practice app, text adventure immersion game, visual flashcard vocab, etc.)
- **Audio-Based Learning:** AI-powered speech recognition to assist with pronunciation and conversation practice.
- **Adding personalized learning paths** through AI-driven recommendations.

### **AI Model Orchestration & Routing**

- **Model Router & Gateway**: Dynamically select the best AI model based on **task complexity. i.e.** **Mixtral 8x7B** for structured tasks, **IBM Granite** for conversational tasks.
- **AI Pipeline Orchestration & Analytics Tools**: Monitor **query accuracy, latency, and user engagement metrics**.

### **Feedback Loop & Continuous Improvement**

- **Feedback Loop Mechanism**: Students and teachers provide feedback to improve AI accuracy.
- **Adaptive Learning & Personalization**: AI dynamically adjusts difficulty levels based on student progress.
