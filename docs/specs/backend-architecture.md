# Project Architecture Overview: .NET Clean Architecture

## 1. High-Level Dependency Rule
The solution follows **Clean Architecture** principles. Dependencies flow **inward**.
* **Domain** has no dependencies.
* **Application** depends only on Domain.
* **Infrastructure** depends on Application and Domain.
* **API** (Presentation) depends on Application and Infrastructure (for DI registration).

---

## 2. Project & Folder Definitions

### **Project 1: Domain**
*The core of the system. Contains business rules and fundamental objects.*
* **`/Entities`**: Data models that represent database tables (e.g., `User.cs`).
* **`/Common`**: Logic/Base classes shared across entities (e.g., `AuditableEntity.cs`).
* **`/Exceptions`**: Domain-specific custom exceptions.
* **`/Interfaces`**: Abstractions for data access (e.g., `IRepository<T>`).

### **Project 2: API.Application**
*The "Brains" of the app. Orchestrates business logic and use cases.*
* **`/Interfaces`**: Abstractions for all services and external integrations.
* **`/Services`**: Implementations of business logic.
* **`/DTOs`**: Data Transfer Objects for API requests and responses.
* **`/Mappings`**: Configurations for object-to-object mapping (e.g., AutoMapper).
* **`/Validators`**: Input validation logic (e.g., FluentValidation).

### **Project 3: API.Infrastructure**
*The "Plumbing." Implements interfaces using specific technologies or libraries.*
* **`/Persistence/Context`**: Entity Framework `DbContext` and DB configurations.
* **`/Persistence/Repositories`**: Concrete implementations of Domain repository interfaces.
* **`/Services/External`**: Implementations for third-party integrations (Email, SMS, Cloud Storage).
* **`/Wrappers`**: (Crucial) This is where **External Libraries** (NuGet packages) are isolated. They are wrapped in classes that implement Application interfaces to ensure the core remains library-agnostic.
* **`DependencyInjection.cs`**: Static class to register all infrastructure services.

### **Project 4: API.Presentation**
*The Entry Point. Handles HTTP requests and response formatting.*
* **`/Controllers`**: Thin endpoints that delegate work to the Application layer.
* **`/Middlewares`**: Global logic for error handling, logging, and security.
* **`/Extensions`**: Helper methods to keep `Program.cs` clean.
* **`/Properties`**: Environment and launch settings.

---

## 3. Integration Patterns
* **External Libraries:** Never used directly in Application/Domain. They are wrapped in **Infrastructure** and accessed via an interface in **Application**.
* **Database:** Accessed via the Repository Pattern.
* **Dependency Injection:** Configured in Infrastructure but triggered in the API's `Program.cs` via extension methods.

## 4. Test Projects Definition

### **Project 5: Tests.Unit**
*The fastest tests. No external dependencies.*
* **Target:** **Domain** & **Application**.
* **Focus:** Logic, math, validation, and mapping.
* **Dependencies:** Only on `Application` and `Domain`.
* **Tools:** xUnit, Moq/NSubstitute, FluentAssertions.

### **Project 6: Tests.Integration**
*Verifying the "Plumbing."*
* **Target:** **Infrastructure**.
* **Focus:** Database repositories, file system access, and external service wrappers.
* **Dependencies:** `Infrastructure`, `Application`, and `Domain`.
* **Tools:** xUnit, **Testcontainers** (for real Postgres in Docker).

### **Project 7: Tests.Functional (or Tests.Acceptance)**
*The "Black Box" test.*
* **Target:** **API (Presentation)**.
* **Focus:** The full HTTP pipeline (CORS, Auth, Routing, Controllers).
* **Dependencies:** `API`, `Infrastructure`, `Application`, and `Domain`.
* **Tools:** `WebApplicationFactory<Program>`, HttpClient, In-Memory DB (or Testcontainers).

@import "Backend-Architecture.mermaid"
