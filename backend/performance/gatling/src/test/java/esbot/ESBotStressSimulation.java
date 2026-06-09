package esbot;

import static io.gatling.javaapi.core.CoreDsl.constantConcurrentUsers;
import static io.gatling.javaapi.core.CoreDsl.rampConcurrentUsers;

import java.time.Duration;

/**
 * Stress simulation that ramps beyond the 50-user NFR to observe system limits.
 */
public class ESBotStressSimulation extends ESBotAPISimulation {

  private static final int USERS = Integer.parseInt(System.getProperty("stressUsers", "200"));
  private static final int RAMP_SECONDS = Integer.parseInt(System.getProperty("stressRampSeconds", "600"));
  private static final int DURATION_SECONDS = Integer.parseInt(System.getProperty("stressDurationSeconds", "900"));

  {
    setUp(
        SESSION_FLOW.injectClosed(
            rampConcurrentUsers(0).to(USERS).during(Duration.ofSeconds(RAMP_SECONDS)),
            constantConcurrentUsers(USERS).during(Duration.ofSeconds(DURATION_SECONDS))
        )
    ).maxDuration(Duration.ofSeconds(RAMP_SECONDS + DURATION_SECONDS + 120))
        .protocols(HTTP_PROTOCOL);
  }
}
