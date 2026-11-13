import { describe, it, expect } from "vitest";
import { http, HttpResponse } from "msw";
import { useConversion } from "../../src/components/useConversion";
import { server } from "../../vitest.setup.mts";

const API_URL = "http://localhost:8000/api/v1/convert";

describe("handleFileUpload", () => {
  it("converts an uploaded file and updates the content on success", async () => {
    // 正常系は vitest.setup.mts の successHandlers がそのまま使われます
    const file = new File(["# test"], "test.md", { type: "text/markdown" });
    const {
      status,
      errorMessage,
      rawMarkdown,
      markdownContent,
      handleFileUpload,
    } = useConversion();

    await handleFileUpload(file);

    expect(status.value).toBe("success");
    expect(errorMessage.value).toBeNull();
    expect(rawMarkdown.value).toBe(
      "# Hello World\n\nThis is a **mock** response.",
    );
    expect(markdownContent.value).toContain("<h1>Hello World</h1>");
    expect(markdownContent.value).toContain("<strong>mock</strong>");
  });

  it("handles an API error response", async () => {
    // このテストの間だけ 500 エラーを返すように上書き
    server.use(
      http.post(API_URL, () => {
        return HttpResponse.json(
          {
            success: false,
            markdown: null,
            error: "Server error",
          },
          { status: 500 },
        );
      }),
    );

    const file = new File(["# test"], "test.md", { type: "text/markdown" });
    const { status, errorMessage, handleFileUpload } = useConversion();

    await handleFileUpload(file);

    expect(status.value).toBe("error");
    expect(errorMessage.value).toBe("Server error");
  });

  it("handles a network failure", async () => {
    server.use(
      http.post(API_URL, () => {
        return HttpResponse.error();
      }),
    );

    const file = new File(["# test"], "test.md", { type: "text/markdown" });
    const { status, errorMessage, handleFileUpload } = useConversion();

    await handleFileUpload(file);

    expect(status.value).toBe("error");
    expect(errorMessage.value).toBeTruthy();
  });

  it("handles a null file with a 'No file selected.' message", async () => {
    const { status, errorMessage, handleFileUpload } = useConversion();

    await handleFileUpload(null);

    expect(status.value).toBe("error");
    expect(errorMessage.value).toBe("No file selected.");
  });
});

describe("handleCopy", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("sets isCopied to true and auto-resets it to false after 2 seconds on a successful copy", async () => {
    const { rawMarkdown, isCopied, handleCopy } = useConversion();

    rawMarkdown.value = "# Markdown";
    expect(isCopied.value).toBe(false);

    await handleCopy();

    expect(navigator.clipboard.writeText).toHaveBeenCalledTimes(1);
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith("# Markdown");

    expect(isCopied.value).toBe(true);
    vi.advanceTimersByTime(2000);
    expect(isCopied.value).toBe(false);
  });

  it("keeps isCopied false when the clipboard write fails", async () => {
    const { rawMarkdown, isCopied, handleCopy } = useConversion();
    rawMarkdown.value = "# Markdown";

    vi.mocked(navigator.clipboard.writeText).mockRejectedValueOnce(
      new Error("Clipboard permission denied"),
    );

    await handleCopy();

    expect(isCopied.value).toBe(false);
  });
});
