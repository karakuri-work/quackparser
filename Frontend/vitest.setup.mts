import { setupServer } from "msw/node";
import { afterAll, afterEach, beforeAll, vi } from "vitest";
import { successHandlers } from "./tests/mocks/handlers";

export const server = setupServer(...successHandlers);

Object.defineProperty(navigator, "clipboard", {
  value: {
    writeText: vi.fn(),
    readText: vi.fn(),
  },
  configurable: true,
});

beforeAll(() => {
  server.listen({ onUnhandledRequest: "error" });
});

afterEach(() => {
  server.resetHandlers();
  vi.clearAllMocks();
});

afterAll(() => {
  server.close();
});
