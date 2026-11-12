import { ref } from "vue";
import type { Ref } from "vue";

interface ConvertResponse {
  success: boolean;
  markdown: string | null;
  error: string | null;
}

export function useConversion() {
  const markdownContent = ref("Markdown output will appear here.");
  const isLoading = ref(false);

  const API_URL = "http://127.0.0.1:8000/convert";

  const handleFileUpload = async (file: File | File[]) => {
    isLoading.value = true;
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

      markdownContent.value = data.markdown || "";
    } catch (error) {
      markdownContent.value = `Error: ${(error as Error).message}`;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    markdownContent,
    isLoading,
    handleFileUpload,
  };
}
