# AItinerary: Comprehensive Technical Blueprint

**Version:** 1.0  
**Last Updated:** April 2026  
**Project Type:** Agentic Travel Intelligence Platform  
**Status:** Alpha (MVP in Development)

---

## 1. Executive Summary

**AItinerary** is an intelligent, data-driven travel planning platform that leverages agentic AI capabilities to curate personalized, multi-day itineraries with integrated booking options. The platform synthesizes user preferences, budgetary constraints, and travel behavior patterns to generate optimized travel experiences across flights, accommodations, vehicle rentals, and activity recommendations.

### Key Value Propositions
- **Hyper-personalized AI-driven itineraries** using temporal and behavioral context
- **Unified booking orchestration** across fragmented travel provider ecosystems
- **Real-time budget optimization** with predictive cost modeling
- **Multi-variant recommendation engine** with preference-weighted filtering
- **Persistent traveler profiles** enabling longitudinal preference learning
- **Seamless multi-day itinerary synthesis** with activity recommendations

---

## 2. Detailed Product Requirements Specification

### 2.1 Problem Statement & Market Context

#### Current Market Pain Points
The travel planning ecosystem suffers from fundamental fragmentation and inefficiency:
- **Fragmentation:** Travelers must navigate 15+ independent platforms (Expedia, Booking.com, Kayak, Airbnb, Viator, etc.)
- **Decision Paralysis:** Average trip planning takes 8-12 hours across multiple sessions with incomplete information synthesis
- **Budget Opacity:** No unified cost modeling across flights, hotels, activities, and ground transport
- **Generic Recommendations:** OTA (Online Travel Agencies) recommendations are commodity-based, not preference-driven
- **Lack of Continuity:** No longitudinal learning—each trip is planned de novo without context from previous journeys
- **Hidden Costs:** Alternative accommodations, activity bundles, and time-of-day pricing variations create post-booking surprises

#### AItinerary's Competitive Positioning
AItinerary resolves these by functioning as an **intelligent travel concierge layer** that:
- Unifies fractured booking ecosystems into a single discovery interface
- Applies agentic AI to synthesize cohesive multi-day experiences (not just room/flight/car independently)
- Provides transparent, component-level budget modeling with variant optimization
- Learns from historical traveler behavior to improve future recommendations
- Integrates real-time contextual factors (weather, local events, crowding, currency fluctuation)

### 2.2 Target User Personas

#### Persona 1: **Time-Constrained Professionals (TCPs)**
- **Demographics:** 28-45 years old, $120K+ annual income, careers in tech/finance/consulting
- **Behaviors:** Books trips last-minute (1-3 weeks advance), values efficiency over cost
- **Pain Point:** Cannot dedicate 10+ hours to trip planning; needs decision-quality recommendations in <15 minutes
- **Value Drivers:** Time savings, peace-of-mind, seamless experience
- **Usage Pattern:** 4-6 trips/year, primarily business with occasional leisure
- **Willingness to Pay:** High ($50-100/year subscription or 5-8% booking commission)

#### Persona 2: **Budget-Conscious Adventure Seekers (BCAS)**
- **Demographics:** 22-35 years old, $40K-90K annual income, variable employment
- **Behaviors:** Plans extensively (6-12 weeks advance), optimizes heavily on cost, seeks experiences over luxury
- **Pain Point:** Hours spent comparing micro-variants to stay within budget; fears overpaying or missing discount opportunities
- **Value Drivers:** Cost optimization, confidence in value, authentic local experiences
- **Usage Pattern:** 6-12 trips/year, predominantly leisure, diverse destinations
- **Willingness to Pay:** Medium ($20-40/year subscription) or commission-based

#### Persona 3: **Family Vacation Planners (FVPs)**
- **Demographics:** 35-55 years old, $80K-150K+ annual income, multi-generational travel
- **Behaviors:** Plans extensively, requires multiple accommodation types, concerned with logistics/accessibility
- **Pain Points:** Managing family preferences, child-friendly ratings, accessibility requirements, group budget coordination
- **Value Drivers:** Accessibility info, family-specific recommendations, group coordination tools
- **Usage Pattern:** 1-4 family trips/year, 7-14 day duration, often includes relatives
- **Willingness to Pay:** High ($50-80/year, premium for group features)

#### Persona 4: **Growth-Stage Travel Agencies (GTAs)**
- **Demographics:** B2B customers, 2-15 person teams, $200K-2M revenue
- **Behaviors:** Currently manual itinerary building, scaling operations
- **Pain Points:** Itinerary generation is bottleneck; client customization requests manual intervention; limited competitive differentiation
- **Value Drivers:** Efficiency gains (10x faster itinerary generation), white-label capability, commission revenue
- **Usage Pattern:** 20-100 itineraries/month per agency
- **Willingness to Pay:** High (10-15% booking commission, $500-2K/month licensing)

### 2.3 Market & Business Objectives

#### Business Goals (18-month horizon)
1. **Acquire 50K active users** by end of Year 1 (sign-ups → repeat usage)
2. **$2M GMV (Gross Merchandise Value)** through commission-based affiliate revenue
3. **Establish category leadership** in AI-powered travel planning
4. **Licensing revenue** by Q4 ($100K+ from travel agencies/TMCs)
5. **80% positive NPS score** among active users

#### Product Goals
1. **90%+ user satisfaction** on itinerary quality (vs. handcrafted competitors)
2. **Sub-5-second generation time** for itineraries (including AI synthesis)
3. **95%+ accuracy** in cost estimation (within ±$50 per component)
4. **Reduce planning time** from 8-12 hours to <20 minutes average
5. **Establish data moat** through 1M+ anonymized itinerary data points for model fine-tuning

### 2.4 Functional Requirements (Detailed)

#### 2.4.1 Core Itinerary Planning Capability

**Requirement FR.01: Multi-Constraint Trip Generation**
- System MUST accept simultaneous constraints: destination, date range, traveler count, per-person budget, trip intensity
- System MUST resolve conflicting constraints (e.g., 3-star hotel + $30/night budget) with graceful fallback messaging
- System MUST generate itineraries within 5 seconds excluding AI synthesis (critical for UX)
- System MUST normalize dates to ISO8601 format; handle month names, relative dates ("next summer")
- System MUST calculate trip duration as (end_date - start_date) and cap at 30 days for MVP

**Requirement FR.02: Component-Level Filtering & Matching**
- **Flights:** Match on [airline ∩ time_window ∩ budget], return ranked by user-weighted preference (price, duration, schedule convenience)
- **Hotels:** Match on [star_rating ≥ minimum ∩ rooms_available ≥ requested ∩ nightly_price ≤ budget], return ranked by rating then price
- **Cars:** Match on [vehicle_type ∈ preferred_types ∪ Any ∩ daily_rate ≤ budget], return ranked by price then passenger reviews
- **Activities:** Match on [intensity ∈ selected_level ∩ estimated_cost ≤ remaining_daily_budget], return ranked by popularity + recency

**Requirement FR.03: AI-Powered Daily Activity Synthesis**
- System MUST call OpenAI API with structured prompt including destination, duration, traveler count, intensity, budget constraints
- System MUST parse returned JSON strictly to extract: day_number, title, activities[], guidelines, estimated_cost
- System MUST validate that response contains exactly N days matching trip duration; reject malformed responses
- System MUST fall back to template-based activity plan within 100ms if API fails
- System MUST limit token usage to 450 tokens/request for cost efficiency and latency (<3s response time)

**Requirement FR.04: Real-Time Budget Transparency**
- System MUST calculate per-component costs: flight × 1, hotel × (nightly_rate × rooms × nights), car × daily_rate × days, activities × sum(daily_costs)
- System MUST compute grand_total = flight + hotel + car + activities
- System MUST flag budget_status as "Within budget" or "Over budget" based on comparison to (per_person_budget × travelers)
- System MUST display cost breakdown at component level + itemized daily activities with line-item costs
- System MUST identify "savings opportunities" (e.g., "Upgrade to 4-star hotel for only +$30/night" or "Bundle activities for 15% discount")

#### 2.4.2 User Authentication & Session Management

**Requirement FR.05: Dual-Mode Authentication**
- System MUST support two modes: Sign-in (existing users) and Sign-up (new users)
- Sign-up MUST validate: username not already registered, password ≥8 characters, username ≥3 characters
- Sign-up MUST encrypt passwords using bcrypt with salt rounds ≥12 before persistence (production requirement)
- Sign-in MUST validate credentials against persistent user registry with constant-time comparison to resist timing attacks
- System MUST enforce max 5 failed sign-in attempts per IP per 15 minutes to prevent brute force (future implementation)

**Requirement FR.06: Persistent Session Management**
- System MUST create server-side session upon successful authentication, valid for 30 days of inactivity
- Session MUST include: username, last_login_timestamp, preferred_settings (optional)
- System MUST regenerate session ID post-login to prevent session fixation
- System MUST inject authenticated user context globally in templates (username, is_logged_in flags)
- System MUST redirect unauthenticated access to protected routes (/saved, /save) to sign-in with `next` parameter for post-auth redirect

#### 2.4.3 Itinerary Persistence & Lifecycle

**Requirement FR.07: Multi-State Itinerary Management**
- System MUST support itinerary states: draft (in-progress), saved (user-persisted), completed (post-trip), archived (user-deleted)
- Draft itineraries MUST expire from session after 24 hours inactivity
- Saved itineraries MUST include: uuid, creation_timestamp, source_values (form inputs), full itinerary data, metadata
- System MUST enable user to save unlimited itineraries (quota TBD per tier)
- System MUST track save_count, view_count, re_optimize_count per itinerary for analytics

**Requirement FR.08: Itinerary Retrieval & Re-Optimization**
- System MUST retrieve saved itineraries by user_id + itinerary_uuid with sub-100ms latency (cached)
- System MUST reconstruct original filter form values from saved record to enable re-optimization
- System MUST support "Generate Variants" (5 variations on same parameters with randomized AI temperature)
- System MUST compare variant costs side-by-side with incumbent recommendation for A/B decision support
- System MUST support user notes/annotations per itinerary (text field, max 500 chars, persisted)

#### 2.4.4 User Profile & Preference Learning

**Requirement FR.09: Preference Profile Capture**
- System MUST collect on first sign-in: primary_travel_style, accommodation_preference, airline_preference, altitude_tolerance_for_activities, dietary_requirements, accessibility_needs
- System MUST infer preferences from behavior: frequency of destination types, budget distribution, activity type clicks, chosen intensity levels
- System MUST store preference profile in user record with version tracking (enables historical analysis)
- System MUST enable user to edit preferences in /profile page with immediate application to future recommendations

**Requirement FR.10: Longitudinal Learning & Personalization**
- System MUST track user's historical itinerary choices: booked components, user satisfaction ratings (post-trip feedback form)
- System MUST apply collaborative filtering: if User A + User B have similar profiles and A likes destination X more than aggregate, recommend X to B
- System MUST personalize AI prompts with historical preferences: "User usually prefers 4-star hotels; recommend 4-5 star options"
- System MUST build user-specific recommendation boost factors (e.g., weight Paris +1.5x if user has visited 5 Europe trips)

#### 2.4.5 Multi-Provider Integration Strategy

**Requirement FR.11: Provider Abstraction Layer**
- System MUST define provider-agnostic data model: Flight, Hotel, Car, Activity (not tied to specific API schemas)
- System MUST implement provider-specific connectors (Amadeus, Booking.com, Kayak adapters) with schema translation
- System MUST support fallback rotation: if Amadeus API fails, query Google Flights; if both fail, return cached mock data with deprecation warning
- System MUST log all provider API calls with: timestamp, request_hash, response_time, error_status for SLA monitoring
- System MUST enforce per-provider rate limiting (e.g., 100 reqs/second to Amadeus, 50 to Booking.com) with queue buffering

**Requirement FR.12: Real-Time Data Integration**
- System MUST fetch prices with <30-minute staleness for flights, <1-hour for hotels, activities from multiple sources
- System MUST aggregate prices from ≥3 sources per component, flag data recency ("Updated 5 mins ago")
- System MUST detect price volatility: flag if component price increased >10% in past 24h, suggest "book now" or "monitor"
- System MUST provide booking URLs with affiliate tracking parameters (for commission revenue attribution)

### 2.5 Non-Functional Requirements

#### 2.5.1 Performance Requirements

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Itinerary generation (no AI)** | <1s | Form validation + filter matching should be instantaneous |
| **Itinerary generation (with AI)** | <5s | Users expect response within 5s for web interaction |
| **Database query latency** | <100ms p99 | Ensure UI responsiveness for listing/detail views |
| **Page load time** | <2s (first paint) | Competitive baseline for travel booking UIs |
| **API endpoint latency** | <500ms p95 | For mobile clients on 3G networks |

#### 2.5.2 Availability & Reliability

| Requirement | Target | Implementation |
|-------------|--------|-----------------|
| **System Uptime** | 99.5% (MVP) → 99.9% (production) | Blue-green deployment, automated failover |
| **Data Durability** | RPO = 15 mins | Daily snapshots + hourly incremental backups |
| **Recovery Time** | RTO = 1 hour | Automated recovery from AWS S3 snapshots |
| **API Availability** | 99% (upstream providers) | Circuit breaker pattern, graceful degradation |

#### 2.5.3 Scalability Requirements

| Dimension | MVP Target | Year-1 Target | Scaling Strategy |
|-----------|-----------|--------------|------------------|
| **QPS (Queries/sec)** | 10 | 500 | Horizontal + caching layer |
| **Concurrent Users** | 100 | 5,000 | Load balancing, session store sharding |
| **Storage (Itineraries)** | 5GB | 500GB | Migrate JSON → PostgreSQL + archival |
| **AI API Spend** | $500/mo | $15K/mo | Fine-tuning → reduced token usage |

#### 2.5.4 Security & Compliance

| Requirement | Implementation |
|-------------|-----------------|
| **Data Encryption (Transit)** | TLS 1.3 for all HTTP endpoints |
| **Data Encryption (Rest)** | AES-256 for sensitive fields (password, payment info) |
| **Authentication** | Bcrypt hashing, 2FA optional in Phase 2 |
| **Access Control** | Role-based (Admin, User, Guest) with JWT tokens |
| **Compliance** | GDPR (right to export/delete), CCPA (California residents) |
| **Audit Logging** | All user actions logged (sign-in, save, delete) for 90 days |

### 2.6 Constraints & Assumptions

#### Technical Constraints
- **Backend:** Flask monolith initially (no Docker/K8s for MVP)
- **Database:** File-based JSON for MVP, SQLite in Phase 1 (no production-grade DB)
- **AI Model:** OpenAI API only (no fine-tuned models until sufficient training data)
- **Frontend:** Server-side rendering with Jinja2 (no React/Vue for MVP)
- **Geographic:** English language only for MVP (international expansion Phase 2)

#### Business Constraints
- **Budget:** $50K for MVP development + $5K/month for OpenAI API credits
- **Timeline:** MVP launch in Q3 2026 (4 months)
- **Team:** 2 engineers (backend), 1 PM, 1 designer (outsourced)
- **Revenue:** No direct monetization for first 6 months (affiliate commission model pending partnerships)

#### Regulatory Assumptions
- Assume no payment processing in MVP (users book directly via provider redirect)
- Assume affiliate partnerships are pre-negotiated (do not include partnership negotiation in launch)
- Assume no user-generated content requiring moderation (first phase: only system-generated itineraries)

### 2.7 Success Metrics & KPIs

#### Product Metrics

| KPI | MVP Target | Year-1 Target | Method |
|-----|-----------|---------------|--------|
| **User Acquisition** | 500 beta testers | 50,000 active users | Referral + organic |
| **Sign-up → Itinerary Generation Rate** | 60% | 75% | Google Analytics funnel |
| **Itinerary Save Rate** | 25% of generated | 40% of generated | Database query |
| **Repeat User Rate (30-day)** | 20% | 35% | Cohort analysis |
| **Average Session Duration** | 12 minutes | 18 minutes | Analytics instrumentation |
| **User Satisfaction NPS** | 40 | 60+ | Post-itinerary survey |

#### Business Metrics

| KPI | MVP Target | Year-1 Target | Method |
|-----|-----------|---------------|--------|
| **GMV (Gross Merchandise Value)** | $10K | $2M | Affiliate commission tracking |
| **Average Booking Value** | $1,500 | $1,800 | Commission reports from partners |
| **Commission Revenue** | $300 (at 3%) | $60K (at 3%) | Financial tracking |
| **Customer Acquisition Cost** | $5-10 | <$5 | Marketing spend / new users |
| **Lifetime Value** | $50-100 | $500+ | Historical spending per user |

#### Technical Metrics

| KPI | Target | Purpose |
|-----|--------|---------|
| **Error Rate** | <0.5% | Monitor system reliability |
| **API Success Rate** | >99% | Upstream provider health |
| **Cache Hit Ratio** | >70% | Caching effectiveness |
| **Average AI Generation Cost/itinerary** | <$0.01 | OpenAI spend optimization |

---

## 3. System Architecture Overview

### 3.1 Architectural Paradigm

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  (Flask Templates, Bootstrap UI, Client-side State Mgmt)    │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                         │
│  (Route Handlers, Session Management, Business Logic)       │
├─────────────────────────────────────────────────────────────┤
│                    Service Layer                             │
│  (Itinerary Builder, Filter Engine, AI Orchestrator)        │
├─────────────────────────────────────────────────────────────┤
│                 Integration Bridge Layer                      │
│  (Flight API Connector, Hotel Aggregator, Car Rental API)   │
├─────────────────────────────────────────────────────────────┤
│                    Persistence Layer                         │
│  (JSON-based Itinerary Store, User Registry, Session Cache) │
└─────────────────────────────────────────────────────────────┘
```

**Pattern:** Layered monolithic architecture with service orientation, designed for mid-scale deployment with clear separation of concerns.

### 3.2 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Framework** | Flask | ≥2.2.0 | Lightweight HTTP routing, request handling |
| **Backend Runtime** | Python | 3.8+ | Application logic, API integration |
| **Frontend** | Jinja2 Templates | Built-in | Server-side templating |
| **UI Framework** | Bootstrap | 5.3.0 | Responsive layout, component library |
| **Styling** | Custom CSS | Via `/static/styles.css` | Brand customization |
| **Session Management** | Flask Sessions | Built-in | Secure user state persistence |
| **Data Persistence** | JSON (File-based) | Native | Itinerary & user data storage |
| **AI Integration** | OpenAI API | ≥1.0.0 | GPT-4o-mini for activity synthesis |

---

## 4. Data Model & Information Architecture

### 4.1 Core Entities

#### 4.1.1 **User** Entity
```json
{
  "id": "string (implicit via username)",
  "username": "string",
  "password": "string (plaintext - requires hashing in prod)",
  "created_at": "ISO8601 timestamp (optional)",
  "preference_profile": {
    "travel_style": "enum[Relaxed|Moderate|Active]",
    "avg_budget_per_trip": "number",
    "preferred_airlines": ["string"],
    "accommodation_preferences": ["Hotel"|"Apartment"|"Resort"],
    "accessibility_requirements": "string"
  }
}
```

#### 4.1.2 **Itinerary** Entity (Core)
```json
{
  "id": "uuid",
  "destination": "string",
  "dates": "string (format: 'YYYY-MM-DD to YYYY-MM-DD')",
  "travelers": "number (1+)",
  "budget_per_person": "number (USD)",
  "total_budget": "number (USD)",
  "nights": "number",
  "intensity": "enum[Relaxed|Moderate|Active]",
  "created_at": "ISO8601 timestamp",
  "user_id": "string (for persistence association)",
  "status": "enum[draft|saved|completed|archived]"
}
```

#### 4.1.3 **Itinerary Extended** (Full Data Structure)
```json
{
  "destination": "string",
  "dates": "string",
  "travelers": "number",
  "budget_per_person": "number",
  "total_budget": "number",
  "nights": "number",
  "flight": {
    "airline": "string",
    "route": "string",
    "time": "string",
    "price": "number (USD)",
    "booking_url": "URL"
  },
  "hotel": {
    "name": "string",
    "price_per_night": "number",
    "rating": "number (1-5 stars)",
    "rooms_available": "number",
    "type": "enum[Hotel|Apartment|Resort]",
    "booking_url": "URL"
  },
  "car": {
    "name": "string",
    "daily_price": "number",
    "type": "enum[Sedan|SUV|Compact]",
    "provider": "string",
    "booking_url": "URL"
  },
  "daily_plan": [
    {
      "day_number": "number (1-N)",
      "title": "string",
      "activities": ["string"],
      "guidelines": "string",
      "estimated_cost": "number (USD)"
    }
  ],
  "preferences": {
    "preferred_airlines": "string (comma-delimited)",
    "flight_time_range": "string (HH:MM-HH:MM)",
    "intensity": "enum[Relaxed|Moderate|Active]",
    "hotel_star": "number (1-5)",
    "hotel_rooms": "number"
  },
  "totals": {
    "flight": "number (USD)",
    "hotel": "number (USD)",
    "car": "number (USD)",
    "activities": "number (USD)",
    "grand_total": "number (USD)",
    "budget_match": "enum[Within budget|Over budget]"
  }
}
```

#### 4.1.4 **Saved Itinerary Record** (Persistence)
```json
{
  "id": "uuid (unique record identifier)",
  "created_at": "ISO8601 timestamp",
  "destination": "string",
  "dates": "string",
  "travelers": "number",
  "total_budget": "number",
  "grand_total": "number",
  "intensity": "string",
  "values": {
    "destination": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "travelers": "number",
    "budget_per_person": "number",
    "preferred_airlines": "string",
    "flight_time_range": "string",
    "flight_budget": "number",
    "hotel_star": "number",
    "hotel_rooms": "number",
    "hotel_budget": "number",
    "car_type": "string",
    "car_budget": "number",
    "intensity": "string"
  },
  "data": "Itinerary (full structure)"
}
```

### 4.2 Storage Architecture

| Entity | Storage Medium | Format | Persistence Strategy |
|--------|----------------|--------|----------------------|
| Users | `users.json` | Plain JSON | In-memory load, file sync on write |
| Itineraries | `saved_itineraries.json` | Array of JSON objects | Append-on-save, atomic file writes |
| Session State | Flask Session (server-side) | Encrypted cookies | Built-in Flask session handler |

---

## 5. Feature Specification & Functional Requirements

### 5.1 Core Features

#### **5.1.1 Intelligent Trip Planning Engine**
- **Input:** Destination, travel dates, number of travelers, overall budget
- **Processing Pipeline:**
  1. Parse temporal constraints & calculate trip duration
  2. Segment budget across travel components (flight, accommodation, activities, transport)
  3. Load user preference profile (if authenticated)
  4. Apply filters via parametric constraints
  5. Invoke AI agent for activity synthesis
  6. Aggregate companion services (hotels, flights, car rental)
  7. Calculate total trip cost and budget variance
- **Output:** Comprehensive itinerary object with bookable components

#### **5.1.2 Multi-Dimensional Filtering Engine**

**Flight Filtering:**
- Airline preference matching (comma-delimited list, case-insensitive)
- Departure/arrival time window filtering (HH:MM – HH:MM format)
- Price ceiling filtering (budget-aware selection)
- Fallback to best available option if no exact matches

**Accommodation Filtering:**
- Star rating threshold filtering (1-5 scale)
- Room availability validation
- Nightly rate cap enforcement
- Type-based segmentation (Hotel, Apartment, Resort)

**Vehicle Rental Filtering:**
- Vehicle type preference (Sedan, SUV, Compact, Any)
- Daily rental rate ceiling
- Provider-agnostic matching

**Activity Intensity Modulation:**
- Dynamic activity plan generation based on intensity level
- Budget allocation adjustment per travel style
- Guidelines customization per activity type

#### **5.1.3 AI-Powered Activity Recommendation System**
- **Model:** GPT-4o-mini via OpenAI API
- **Input Prompt Template:**
  ```
  "Generate a {nights}-night itinerary for {travelers} guests in {destination}
   with a {intensity} pace and ${budget_per_person} per-person budget.
   Return JSON with days array containing: day_number, title, activities, 
   guidelines, estimated_cost."
  ```
- **Output Validation:** Strict JSON schema validation with fallback to default plan
- **Token Efficiency:** Max 450 tokens per request, temperature 0.8 for variability
- **Graceful Degradation:** Template-based default activity plan if API fails/unavailable

#### **5.1.4 Budget Orchestration & Cost Modeling**
- **Component-level Cost Breakdown:**
  - Flight: Single airline cost
  - Hotel: (nightly_rate × rooms × nights)
  - Car: (daily_rate × trip_duration)
  - Activities: Sum of daily estimated costs
- **Aggregation:** grand_total = flight + hotel + car + activities
- **Budget Variance Analysis:** Comparison against (budget_per_person × travelers)
- **Status Flag:** "Within budget" or "Over budget"

#### **5.1.5 User Authentication & Session Management**
- **Sign-up:** Username uniqueness validation, plaintext password storage (⚠️ security concern)
- **Sign-in:** Credential validation against persisted registry
- **Session Binding:** Flask session cookie with server-side user context
- **Logout:** Explicit session termination
- **Protected Routes:** Redirect unauthenticated users to sign-in with `next` parameter

#### **5.1.6 Itinerary Persistence & Retrieval**
- **Save Operation:**
  - Authenticate user (redirect to sign-in if needed)
  - Generate UUID for record identity
  - Serialize full itinerary + filter values
  - Append to `saved_itineraries.json`
  - Redirect user to saved list with success flag
- **Retrieval:** Lookup by UUID with fallback handling
- **Detail View:** Reconstructs form state for potential re-optimization

#### **5.1.7 Multi-page Navigation Architecture**
- **Home (/):** Itinerary builder form + results display
- **Sign In/Sign Up (/signin):** Dual-mode authentication interface
- **Saved (/saved):** List of user's saved itineraries
- **Saved Detail (/saved/<uuid>):** Review & re-optimize individual itinerary
- **Partners (/partners):** Integration showcase (placeholder)
- **About (/about):** Company/product information (placeholder)
- **Contact (/contact):** Feedback collection (placeholder)
- **Sign Out (/signout):** Session termination

---

## 6. API Reference & Route Specification

### 6.1 Public Routes

#### **GET / | POST /**
- **Purpose:** Main itinerary builder interface
- **Method:** GET displays form with cached values; POST triggers itinerary generation
- **Parameters (Form):**
  - `destination` (required, text)
  - `start_date` (required, YYYY-MM-DD)
  - `end_date` (required, YYYY-MM-DD)
  - `travelers` (number, default: 1)
  - `budget_per_person` (number, default: 0)
  - `preferred_airlines` (text, comma-delimited)
  - `flight_time_range` (text, HH:MM-HH:MM)
  - `flight_budget` (number)
  - `hotel_star` (number, 1-5, default: 0)
  - `hotel_rooms` (number, default: 1)
  - `hotel_budget` (number)
  - `car_type` (select: Any|Sedan|SUV|Compact)
  - `car_budget` (number)
  - `intensity` (select: Any|Relaxed|Moderate|Active)
- **Response:** HTML with populated form + itinerary results (if POST)

#### **GET /signin | POST /signin**
- **Purpose:** Authentication gateway (sign-up or sign-in modes)
- **Method:** GET shows form; POST handles credential validation
- **Parameters (Form):**
  - `mode` (select: signin|signup)
  - `username` (required, text)
  - `password` (required, text)
  - `next` (optional, redirect target)
- **Response:** 
  - Success: Redirect to `next` URL (default: home)
  - Failure: Re-render form with error message

#### **GET /signout**
- **Purpose:** User session termination
- **Response:** Redirect to home

#### **GET /partners**
- **Purpose:** Integration partners showcase
- **Response:** Static HTML template (placeholder)

#### **GET /about**
- **Purpose:** Product/company information
- **Response:** Static HTML template (placeholder)

#### **GET /contact | POST /contact**
- **Purpose:** User feedback collection
- **Method:** GET shows form; POST marks as submitted
- **Response:** Template with confirmation state

### 6.2 Protected Routes (Authentication Required)

#### **POST /save**
- **Purpose:** Persist generated itinerary to user's saved collection
- **Authentication:** Enforced (redirects to sign-in if unauthenticated)
- **Parameters (Form):**
  - `itinerary_json` (JSON stringified itinerary object)
  - `values_json` (JSON stringified filter form values)
- **Response:** Redirect to `/saved?saved=true` on success

#### **GET /saved**
- **Purpose:** Display user's saved itinerary collection
- **Authentication:** Enforced
- **Query Parameters:**
  - `saved` (optional, "true" shows success banner)
- **Response:** HTML list of saved itineraries with metadata

#### **GET /saved/<itinerary_id>**
- **Purpose:** Review/re-optimize individual saved itinerary
- **Authentication:** Enforced
- **Path Parameters:**
  - `itinerary_id` (UUID)
- **Response:** 
  - If found: HTML form pre-populated with original filter values + results
  - If not found: Redirect to `/saved`

---

## 7. Service Layer Functions & Business Logic

### 7.1 Data Access Functions

| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| `load_users()` | Fetch user registry | None | Dictionary {username: password} |
| `write_users(users)` | Persist user registry | {username: password} | void |
| `load_saved_itineraries()` | Fetch all saved itineraries | None | List[SavedItinerary] |
| `write_saved_itineraries(saved_list)` | Persist itinerary collection | List[SavedItinerary] | void |
| `get_current_user()` | Extract authenticated username | None | str \| None |
| `find_saved_itinerary(id)` | Lookup itinerary by UUID | UUID (str) | SavedItinerary \| None |

### 7.2 Business Logic Functions

#### **Filtering Engine**
- `fetch_flight_options(destination, airlines, time_range, budget)` → List[Flight]
- `fetch_hotel_options(destination, star_rating, rooms, budget_per_night)` → List[Hotel]
- `fetch_car_rental_options(destination, car_type, budget_per_day)` → List[Car]

#### **Activity Synthesis**
- `default_activity_plan(intensity, nights)` → List[DayPlan]
  - Template-based fallback with intensity-aware modulation
- `ai_recommend_daily_plan(destination, intensity, nights, travelers, budget)` → List[DayPlan]
  - Primary: OpenAI-powered (400–450 tokens)
  - Fallback: `default_activity_plan()` on API failure

#### **Itinerary Orchestration**
- `build_itinerary(form_data)` → Itinerary
  - Orchestrates entire pipeline: date parsing → filtering → AI synthesis → cost aggregation
  - Returns comprehensive itinerary with booking URLs

#### **Context Management**
- `common_context()` → Dict
  - Provides filter options (accommodation types, car types, intensity levels) for template rendering
- `inject_user_context()` → Dict
  - Jinja2 context processor injecting user authentication state globally

### 7.3 Persistence Functions

- `save_itinerary_data(itinerary, values)` → SavedRecord
  - Generates UUID, timestamps, serializes to JSON, appends to file
- `build_values_from_itinerary(itinerary)` → Dict
  - Reconstructs filter form values from saved itinerary for re-optimization

---

## 8. User Experience Flows

### 8.1 Primary Flow: Generate Personalized Itinerary

```
1. User accesses home ("/")
2. Completes trip planning form:
   - Core: destination, dates, travelers, budget
   - Flight preferences: airlines, time window, budget cap
   - Hotel preferences: star rating, room count, nightly budget
   - Car preferences: vehicle type, daily budget
   - Activity style: intensity level (Relaxed|Moderate|Active)
3. Submits form (POST /)
4. Server processes:
   - Validates inputs & calculates trip duration
   - Fetches filtered options from each provider (flights, hotels, cars)
   - Invokes AI to generate personalized daily activities
   - Aggregates costs & budget variance analysis
5. Server renders index.html with:
   - Pre-populated form (values cached in session)
   - Comprehensive itinerary display (hotel, flight, car, daily plan)
   - Cost breakdown & budget status
   - "Save Itinerary" button (if interested)
```

### 8.2 Secondary Flow: Save & Review Itinerary

```
1. User clicks "Save Itinerary" button on results page
2. Redirect check: if not authenticated → redirect to sign-in (with next=/index)
3. If authenticated:
   - POST to /save with serialized itinerary + filter values
   - Server generates UUID, timestamps record
   - Appends to saved_itineraries.json
   - Redirect to /saved?saved=true
4. Saved list page displays:
   - All user's saved itineraries with metadata (destination, dates, total cost)
   - Links to view/review each itinerary detail
5. User clicks on itinerary → /saved/<uuid>
   - Pre-populates original filter values in form
   - Displays original itinerary results for review
   - User can modify filters & regenerate if desired
```

### 8.3 Authentication Flow

```
Sign-up Path:
1. User clicks "Sign in/Sign up" → GET /signin
2. Selects "Sign up" mode in form
3. Enters username + password → POST /signin
4. Server validates:
   - Username not already registered
5. If valid:
   - Stores {username: password} in users.json
   - Starts session with username
   - Redirects to next URL (default: home)
6. If invalid: Re-renders form with error message

Sign-in Path:
1. User enters credentials → POST /signin with mode="signin"
2. Server validates:
   - Username exists in users.json
   - Password matches stored value
3. If valid: Session created, redirect to next URL
4. If invalid: Error message re-displayed
```

---

## 9. External Integration Architecture

### 9.1 Flight Booking Integration

**Current State:** Mock data connector  
**Production Requirements:**
- Partner with Amadeus, Skyscanner, Kayak, or Google Flights API
- Endpoint: `GET /flight_search?origin=JFK&destination={destination}&date={date}`
- Response: Real-time flight options with availability, pricing, seat inventory
- Authentication: API key or OAuth2 token
- Booking URL: Dynamic generation with affiliate tracking parameters

**Expected Connector Function:**
```python
def fetch_flight_options(destination, preferred_airlines, time_range, budget):
    # Replace mock with actual API call
    # response = amadeus_client.flight_search(destination, filters)
    # return response.formatted_results()
```

### 9.2 Hotel/Accommodation Integration

**Current State:** Mock data connector  
**Production Requirements:**
- Partner with Booking.com, Expedia, Hotels.com, or Airbnb API
- Endpoint: `GET /property_search?location={destination}&checkIn={date}&checkOut={date}&rooms={n}`
- Response: Properties with real-time rates, availability, reviews, imagery
- Authentication: API credentials or OAuth2
- Booking flow: Direct redirect to partner booking page

**Expected Connector Function:**
```python
def fetch_hotel_options(destination, star_rating, rooms, budget_per_night):
    # booking_api = Booking.com(api_key)
    # results = booking_api.search(destination, filters)
    # return results.properties
```

### 9.3 Car Rental Integration

**Current State:** Mock data connector  
**Production Requirements:**
- Partner with Enterprise, Hertz, Avis, Kayak Car Rental, or Rentalcars.com
- Endpoint: `GET /car_search?location={destination}&pickupDate={date}&dropoffDate={date}&carType={type}`
- Response: Available vehicles with daily rates, insurance options, policies
- Booking: Affiliate transaction tracking
- Authentication: API key-based

### 9.4 AI Activity Recommendation Integration

**Current Implementation:** OpenAI GPT-4o-mini  
**Key Properties:**
- Model: `gpt-4o-mini` (cost-optimized, fast inference)
- Max tokens: 450 (strict budget to maintain latency < 3s)
- Temperature: 0.8 (balances creativity with consistency)
- Fallback: Template-based default plan if API unavailable

**Enhancement Opportunities:**
- Batch multiple destinations for A/B testing
- Fine-tune model on past itinerary feedback data
- Implement caching of activity recommendations per destination + intensity
- Integrate real-time activity availability from Viator, Klook, GetYourGuide APIs

### 9.5 Future Integration Recommendations

| Partner Type | Recommended Provider | Integration Level |
|--------------|---------------------|-------------------|
| **Flights** | Amadeus / Google Flights | Real-time API |
| **Hotels** | Booking.com / Expedia | Real-time API |
| **Car Rental** | Rentalcars.com / Kayak | Real-time API |
| **Activities** | Viator / Klook | Real-time API + Caching |
| **Weather** | OpenWeather / Weather API | Daily cache |
| **Currency Exchange** | XE.com / OANDA | Daily cache |
| **Maps/Navigation** | Google Maps / Mapbox | Client-side SDK |
| **Payment** | Stripe / PayPal | Transaction gateway |

---

## 10. Security Considerations & Compliance

### 10.1 Current Security Issues (MVP Stage)

⚠️ **CRITICAL VULNERABILITIES:**
- Plaintext password storage (users.json) → Requires bcrypt/argon2 hashing immediately
- No HTTPS/TLS enforcement → Deploy with SSL certificates in production
- Flask secret key hardcoded in code → Use environment variables
- No CSRF protection on forms → Add Flask-WTF with token validation
- No input sanitization → Vulnerable to XSS/injection attacks
- Session cookies not marked Secure/HttpOnly → Flask auto-defaults prevent XSS, but add flags explicitly

### 10.2 Recommended Security Hardening

1. **Authentication:**
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   users[username] = generate_password_hash(password)
   ```

2. **CSRF Protection:**
   ```python
   from flask_wtf.csrf import CSRFProtect
   csrf = CSRFProtect(app)
   ```

3. **Input Validation:**
   ```python
   from marshmallow import Schema, fields, validate
   # Define schemas for all form inputs
   ```

4. **Environment Variables:**
   ```python
   app.secret_key = os.getenv("FLASK_SECRET_KEY")
   # Never hardcode secrets
   ```

5. **HTTPS Enforcement:**
   ```python
   SESSION_COOKIE_SECURE = True
   SESSION_COOKIE_HTTPONLY = True
   SESSION_COOKIE_SAMESITE = 'Lax'
   ```

### 10.3 Compliance Considerations

- **GDPR:** User data retention policies, export/deletion mechanisms
- **PCI-DSS:** If processing payments, comply with card data standards
- **Terms of Service:** Clarify API integration partnerships, affiliate disclosures
- **Privacy Policy:** Detail data usage, third-party sharing

---

## 11. Performance & Scalability Architecture

### 11.1 Current Performance Profile

| Operation | Latency | Bottleneck |
|-----------|---------|-----------|
| Itinerary generation (no AI) | ~200ms | Filter logic, JSON serialization |
| Itinerary with AI activities | ~2-4s | OpenAI API call + token streaming |
| User authentication | ~50ms | File I/O (users.json) |
| Saved itinerary retrieval | ~100ms | Linear search in JSON array |

### 11.2 Scalability Limitations (Current Architecture)

**Monolithic JSON Storage Issues:**
- All users' itineraries in single file → O(n) lookup time
- No indexing → Full-file scan per query
- Concurrent write conflicts → Race conditions possible
- No query optimization → Inefficient filtering

**Solutions for Scale:**

#### **Phase 1: Mid-Scale (10K–100K users)**
- Migrate to SQLite with indexing on (user_id, created_at)
- Implement query pagination
- Add Redis cache layer for saved itineraries

#### **Phase 2: Large-Scale (100K–1M+ users)**
- PostreSQL as primary database
- Elasticsearch for full-text search on destinations/activities
- Redis for session management + activity caching
- Memcached for filtering results (flight/hotel/car)
- Microservices: Flight Service, Hotel Service, Activity Service (independent scaling)

#### **Phase 3: Enterprise-Scale (1M+ users)**
- Distributed database (PostgreSQL + replication)
- Message queue (Kafka) for async itinerary generation
- CDN for static assets (Bootstrap, CSS)
- API Gateway with rate limiting
- GraphQL layer for flexible data queries

### 11.3 Caching Strategy

**Short-term (1 hour):**
- Activity recommendations per (destination, intensity) tuple
- Flight/hotel/car filtering results
- User preference profiles

**Medium-term (24 hours):**
- Weather forecasts per destination
- Currency exchange rates
- Popular activity lists

**Long-term (indefinite):**
- User profiles & historical preferences
- Static content (Partners, About Us pages)

---

## 12. Monitoring, Logging & Operational Readiness

### 12.1 Key Metrics to Track

1. **Availability:**
   - App uptime % (target: 99.9%)
   - API endpoint response times (target: <2s p95)

2. **Business Metrics:**
   - Itineraries generated per day
   - Save rate (saved / generated ratio)
   - AI activity generation success rate

3. **Technical Metrics:**
   - OpenAI API error rate
   - Database query latency (p50, p95, p99)
   - Cache hit ratio (target: >80%)

4. **User Metrics:**
   - Sign-up completion rate
   - Session duration
   - Saved itinerary re-access frequency

### 12.2 Logging Strategy

**Error Logging:**
```python
import logging
logger = logging.getLogger(__name__)
logger.error(f"AI synthesis failed for {destination}: {exception}")
```

**Event Logging:**
```
[2026-04-04 10:23:45] user_signup | username=john_doe
[2026-04-04 10:24:12] itinerary_generated | destination=Paris | duration=2.3s
[2026-04-04 10:24:30] itinerary_saved | saved_id=uuid | user=john_doe
```

**Integration Logging:**
```python
logger.info(f"OpenAI API call: destination={destination}, tokens_used=340")
```

### 12.3 Deployment Checklist

- [ ] Environment variables configured (API keys, secret, database URL)
- [ ] HTTPS/SSL certificates installed
- [ ] Password hashing implemented
- [ ] CSRF protection enabled
- [ ] Database migrations run
- [ ] Caching layer initialized
- [ ] Monitoring/alerting configured
- [ ] Error tracking (Sentry/similar) set up
- [ ] Rate limiting configured
- [ ] Backup strategy implemented
- [ ] Load testing passed (target: 1000 req/s)

---

## 13. Future Enhancements & Product Roadmap

### Phase 2 (6-month horizon)

1. **User Profiles & Preferences:**
   - Persistent preference learning (favorite airlines, accommodation types)
   - Travel history tracking
   - Personalized recommendations based on past itineraries

2. **Advanced Filtering:**
   - Visa requirement automation
   - Flight duration preferences
   - Airport proximity filtering
   - Airline loyalty program integration

3. **Booking Integration:**
   - One-click booking via affiliate links (commission tracking)
   - Payment processing (Stripe integration)
   - Booking confirmation management

4. **Real-time Pricing:**
   - Live flight/hotel price updates
   - Price drop alerts
   - Predictive pricing recommendations ("best time to book")

### Phase 3 (12-month horizon)

1. **Social Features:**
   - Itinerary sharing & collaboration
   - Group travel planning
   - Social media integration (Pinterest for mood boards)

2. **Enhanced AI:**
   - Multi-modal recommendations (image-based destination discovery)
   - Sentiment-aware activity suggestions ("energize me" vs. "calm me down")
   - Real-time context adaptation (weather, events, crowding data)

3. **Mobile Native:**
   - iOS/Android native app
   - Offline access for downloaded itineraries
   - Push notifications for price alerts

4. **Advanced Analytics:**
   - Itinerary performance dashboard (popularity, completion rates)
   - A/B testing framework for activity variations
   - Predictive churn modeling

### Phase 4 (18-month horizon)

1. **AI Agents:**
   - Autonomous rebooking for flight cancellations
   - Real-time budget reallocation suggestions
   - Proactive activity recommendations during trip

2. **Marketplace:**
   - Creator platform for custom activity guides
   - Review aggregation across Airbnb, Google, TripAdvisor
   - Community recommendations
   
3. **Enterprise Solutions:**
   - Corporate travel management
   - Bulk itinerary generation for travel agencies
   - White-label platform offering

---

## 14. Development Best Practices & Code Standards

### 14.1 Code Organization

```
/aitinerary
  /app.py (main Flask application)
  /requirements.txt (dependencies)
  /static
    /styles.css (brand styling)
    /img (logos, icons)
  /templates
    /base.html (shared layout)
    /index.html (itinerary builder)
    /saved.html (saved collection)
    /signin.html (authentication)
    /partners.html (partner showcase)
    /about.html (product info)
    /contact.html (feedback)
  /services (future extraction layer)
    /itinerary_builder.py
    /filter_engine.py
    /ai_orchestrator.py
  /models (future ORM models)
    /user.py
    /itinerary.py
  /tests (unit & integration tests)
  /docs (API docs, blueprints)
  BLUEPRINT.md (this file)
  README.md (project overview)
```

### 14.2 Testing Strategy

**Unit Tests:**
- Filtering logic (flight, hotel, car)
- Cost aggregation
- Date parsing & duration calculation

**Integration Tests:**
- Form submission → itinerary generation
- User sign-up/sign-in flows
- Itinerary save/retrieve

**End-to-End Tests:**
- Full user journey from planning to saved state
- UI interactions (form filling, button clicks)

```python
# Example test
def test_build_itinerary_calculates_correct_nights():
    form = {
        'start_date': '2026-05-01',
        'end_date': '2026-05-04',
        # ... other fields
    }
    result = build_itinerary(form)
    assert result['nights'] == 3
```

### 14.3 Git Workflow

- **Branch Strategy:** Git Flow (main, develop, feature/*, release/*)
- **Commit Messages:** Conventional Commits (feat:, fix:, docs:, etc.)
- **Code Review:** Pull request review with 2 approvals before merge
- **Release Versioning:** Semantic versioning (MAJOR.MINOR.PATCH)

---

## 15. Appendix

### 15.1 Glossary

| Term | Definition |
|------|-----------|
| **Itinerary** | Complete multi-day travel plan including flights, accommodations, vehicle, activities, and costs |
| **Agentic AI** | Autonomous AI system capable of planning, decision-making, and executing multi-step workflows |
| **Budget Variance** | Difference between planned trip cost and user's specified budget per person |
| **Intensity Level** | User preference for activity pace (Relaxed, Moderate, Active) affecting daily itinerary structure |
| **Provider** | External booking service (Booking.com, Amadeus, Hertz, etc.) |
| **Affiliate Link** | Tracking URL that earns commission on user bookings (future feature) |

### 15.2 API Response Examples

**Successful Itinerary Generation:**
```json
{
  "destination": "Paris",
  "dates": "2026-05-01 to 2026-05-04",
  "travelers": 2,
  "nights": 3,
  "budget_per_person": 2000,
  "total_budget": 4000,
  "totals": {
    "flight": 640,
    "hotel": 1260,
    "car": 228,
    "activities": 750,
    "grand_total": 2878,
    "budget_match": "Within budget"
  }
}
```

**Error Response (missing required field):**
```json
{
  "error": "Missing required field: destination",
  "status": 400
}
```

### 15.3 Environment Variables Reference

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_SECRET_KEY=<random-64-char-string>
DEBUG=False

# OpenAI Integration
OPENAI_API_KEY=sk-<your-api-key>
OPENAI_MODEL=gpt-4o-mini

# Database (future)
DATABASE_URL=postgresql://user:pass@localhost/aitinerary

# Redis Cache (future)
REDIS_URL=redis://localhost:6379/0

# Third-party APIs (future)
AMADEUS_API_KEY=<key>
BOOKING_AFFILIATE_ID=<id>
GOOGLE_MAPS_API_KEY=<key>
```

---

## 16. Open Questions & Decision Points

1. **Monetization Model:**
   - Affiliate commissions on bookings vs. subscription fee?
   - Freemium tier with premium AI recommendations?

2. **Data Privacy:**
   - How long to retain user itineraries post-deletion?
   - Third-party sharing for analytics/ML improvement?

3. **AI Model Strategy:**
   - Fine-tune proprietary model vs. use GPT-4o-mini as-is?
   - Multimodal AI for destination imagery/mood boards?

4. **Geographic Scope:**
   - Focus on specific regions initially (e.g., Europe) or global?
   - Multi-language support roadmap?

5. **Booking Integration Priority:**
   - Which providers to integrate first (flights, hotels, activities)?
   - Direct bookings vs. affiliate redirects vs. hybrid?

---

**Document Version:** 1.0  
**Last Reviewed:** April 4, 2026  
**Next Review:** July 4, 2026  
**Maintained By:** AItinerary Product Team
