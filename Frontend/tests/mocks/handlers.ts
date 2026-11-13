import { http, HttpResponse } from "msw";

export const successHandlers = [
  http.post("http://localhost:8000/api/v1/convert", async () => {
    return HttpResponse.json({
      success: true,
      markdown: "# Hello World\n\nThis is a **mock** response.",
      error: null,
    });
  }),
];

export const errorHandlers = [
  http.post("http://localhost:8000/api/v1/convert", async () => {
    return HttpResponse.json(
      {
        success: false,
        markdown: null,
        error: "Server error",
      },
      { status: 500 },
    );
  }),
];
