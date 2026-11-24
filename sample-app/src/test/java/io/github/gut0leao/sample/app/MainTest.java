package io.github.gut0leao.sample.app;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

class MainTest {
    @Test
    void printsOnlyTheFixedGreetingEvenWithArguments() {
        PrintStream original = System.out;
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        try (PrintStream captured = new PrintStream(output, true, StandardCharsets.UTF_8)) {
            System.setOut(captured);
            Main.main(new String[]{"ignored argument"});
        } finally {
            System.setOut(original);
        }
        assertEquals("Hello from sample-app!" + System.lineSeparator(),
                output.toString(StandardCharsets.UTF_8));
    }
}
