package esbot;

import static io.gatling.javaapi.core.CoreDsl.StringBody;
import static io.gatling.javaapi.core.CoreDsl.exec;
import static io.gatling.javaapi.core.CoreDsl.jsonPath;
import static io.gatling.javaapi.core.CoreDsl.pause;
import static io.gatling.javaapi.core.CoreDsl.scenario;
import static io.gatling.javaapi.http.HttpDsl.http;
import static io.gatling.javaapi.http.HttpDsl.status;

import io.gatling.javaapi.core.ActionBuilder;
import io.gatling.javaapi.core.ScenarioBuilder;
import io.gatling.javaapi.http.HttpProtocolBuilder;

/**
 * Shared HTTP protocol and session-only REST steps (no LLM/chat/quiz endpoints).
 */
public abstract class ESBotAPISimulation extends io.gatling.javaapi.core.Simulation {

  protected static final String BASE_URL = System.getProperty("baseUrl", "http://localhost:8000");

  protected static final HttpProtocolBuilder HTTP_PROTOCOL = http
      .baseUrl(BASE_URL)
      .acceptHeader("application/json")
      .contentTypeHeader("application/json")
      .userAgentHeader("ESBot-Gatling/0.1");

  protected static ActionBuilder createSession() {
    return http("Create Session")
        .post("/api/v1/sessions")
        .body(StringBody("{\"user_id\":\"gatling-#{userId}\",\"title\":\"Gatling Perf Session\"}"))
        .check(status().is(201))
        .check(jsonPath("$.id").saveAs("sessionId"));
  }

  protected static ActionBuilder healthCheck() {
    return http("Health Check")
        .get("/api/v1/health")
        .check(status().is(200))
        .check(jsonPath("$.status").is("ok"));
  }

  protected static ActionBuilder getSession() {
    return http("Get Session")
        .get("/api/v1/sessions/#{sessionId}")
        .check(status().is(200))
        .check(jsonPath("$.id").exists());
  }

  protected static ActionBuilder listSessions() {
    return http("List Sessions")
        .get("/api/v1/sessions?user_id=gatling-#{userId}")
        .check(status().is(200))
        .check(jsonPath("$.sessions").exists());
  }

  protected static ActionBuilder getMessages() {
    return http("Get Message History")
        .get("/api/v1/sessions/#{sessionId}/messages")
        .check(status().is(200))
        .check(jsonPath("$.messages").exists());
  }

  protected static final ScenarioBuilder SESSION_FLOW = scenario("ESBot Session API")
      .exec(session -> session.set("userId", String.valueOf(session.userId())))
      .exec(createSession())
      .pause(1, 2)
      .forever()
      .on(
          exec(healthCheck())
              .pause(1)
              .exec(getSession())
              .pause(1)
              .exec(listSessions())
              .pause(1)
              .exec(getMessages())
              .pause(1, 3)
      );
}
