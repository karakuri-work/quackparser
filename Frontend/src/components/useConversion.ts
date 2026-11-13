import { ref } from "vue";
import MarkdownIt from "markdown-it";
import DOMPurify from "dompurify";
import "github-markdown-css/github-markdown-dark.css";

const API_URL = "http://localhost:8000/api/v1/convert";

const md = new MarkdownIt({
  html: false,
  linkify: false,
  breaks: true,
});

type ConversionStatus = "idle" | "processing" | "success" | "error";

interface ConvertResponse {
  success: boolean;
  markdown: string | null;
  error: string | null;
}

export function useConversion() {
  const status = ref<ConversionStatus>("idle");
  const markdownContent = ref("");
  const rawMarkdown = ref("");
  const errorMessage = ref<string | null>(null);
  const isCopied = ref(false);

  const handleFileUpload = async (file: File | File[]) => {
    status.value = "processing";
    errorMessage.value = null;

    try {
      const selectedFile = Array.isArray(file) ? file[0] : file;
      if (!selectedFile) {
        status.value = "error";
        errorMessage.value = "No file selected.";
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
        status.value = "error";
        errorMessage.value = data.error || response.statusText;
        return;
      }

      status.value = "success";
      rawMarkdown.value = data.markdown || "";
      const rawHtml = md.render(rawMarkdown.value);
      markdownContent.value = DOMPurify.sanitize(rawHtml);
    } catch (error) {
      status.value = "error";
      errorMessage.value = (error as Error).message;
    }
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(rawMarkdown.value);
      isCopied.value = true;
      setTimeout(() => {
        isCopied.value = false;
      }, 2000);
    } catch (error) {}
  };

  return {
    status,
    errorMessage,
    markdownContent,
    rawMarkdown,
    isCopied,
    handleFileUpload,
    handleCopy,
  };
}
