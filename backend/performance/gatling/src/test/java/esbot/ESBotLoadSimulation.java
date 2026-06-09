package esbot;

import static io.gatling.javaapi.core.CoreDsl.constantConcurrentUsers;
import static io.gatling.javaapi.core.CoreDsl.rampConcurrentUsers;

import java.time.Duration;

/**
 * Load simulation aligned with the ESBot NFR: up to 50 concurrent users.
 */
public class ESBotLoadSimulation extends ESBotAPISimulation {

  private static final int USERS = Integer.parseInt(System.getProperty("loadUsers", "50"));
  private static final int RAMP_SECONDS = Integer.parseInt(System.getProperty("loadRampSeconds", "60"));
  private static final int DURATION_SECONDS = Integer.parseInt(System.getProperty("loadDurationSeconds", "300"));

  {
    setUp(
        SESSION_FLOW.injectClosed(
            rampConcurrentUsers(0).to(USERS).during(Duration.ofSeconds(RAMP_SECONDS)),
            constantConcurrentUsers(USERS).during(Duration.ofSeconds(DURATION_SECONDS))
        )
    ).maxDuration(Duration.ofSeconds(RAMP_SECONDS + DURATION_SECONDS + 60))
        .protocols(HTTP_PROTOCOL);
  }
}
