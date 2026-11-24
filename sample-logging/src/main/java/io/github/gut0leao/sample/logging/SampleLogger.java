package io.github.gut0leao.sample.logging;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public final class SampleLogger {
    private static final Logger LOGGER = LogManager.getLogger(SampleLogger.class);

    private SampleLogger() {
    }

    public static void logGreeting() {
        LOGGER.info("Hello from sample-app!");
    }
}
