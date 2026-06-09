package esbot;

import static io.gatling.javaapi.core.CoreDsl.atOnceUsers;
import static io.gatling.javaapi.core.CoreDsl.pause;
import static io.gatling.javaapi.core.CoreDsl.scenario;

import io.gatling.javaapi.core.ScenarioBuilder;

/**
 * Smoke test: one user through session and health endpoints (no LLM).
 */
public class ESBotSmokeSimulation extends ESBotAPISimulation {

  private static final ScenarioBuilder SMOKE = scenario("ESBot Smoke Test")
      .exec(session -> session.set("userId", "smoke"))
      .exec(createSession())
      .pause(1)
      .exec(healthCheck())
      .exec(getSession())
      .exec(listSessions())
      .exec(getMessages());

  {
    setUp(SMOKE.injectOpen(atOnceUsers(1))).protocols(HTTP_PROTOCOL);
  }
}
