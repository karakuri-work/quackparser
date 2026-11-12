import { ref } from "vue";
import MarkdownIt from "markdown-it";
import DOMPurify from "dompurify";
import "github-markdown-css/github-markdown-dark.css";

interface ConvertResponse {
  success: boolean;
  markdown: string | null;
  error: string | null;
}

export function useConversion() {
  const markdownContent = ref("Markdown output will appear here.");
  const handleFileUpload = async (file: File | File[]) => {
    const API_URL = "http://localhost:8000/api/v1/convert";
    const markdownIt = new MarkdownIt({
      html: false,
      linkify: false,
      breaks: true,
    });

    markdownContent.value = "Processing your file...";

    try {
      const selectedFile = Array.isArray(file) ? file[0] : file;
      if (!selectedFile) {
        markdownContent.value = "Error: No file selected.";
        return;
      }

      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      const data = (await response.json()) as ConvertResponse;

      if (!response.ok) {
        markdownContent.value = `Error: ${data.error || response.statusText}`;
        return;
      }

      const rawHtml = markdownIt.render(data.markdown || "");
      const sanitizeHtml = DOMPurify.sanitize(rawHtml);

      markdownContent.value = sanitizeHtml;
    } catch (error) {
      markdownContent.value = `Error: ${(error as Error).message}`;
    }
  };

  return {
    markdownContent,
    handleFileUpload,
  };
}
