<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-text>
            <v-file-input
              variant="outlined"
              label="Select File"
              prepend-icon="mdi-file-document-outline"
              accept=".pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.png,.jpeg,.jpg"
              hide-details
              @update:model-value="handleFileUpload"
            ></v-file-input>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-text class="overflow-auto" style="height: 480px">
            <div
              v-if="status === 'processing'"
              class="d-flex flex-column align-center justify-center h-100 text-center"
            >
              <v-progress-circular
                indeterminate
                color="primary"
                size="32"
                width="4"
                class="mb-2"
              ></v-progress-circular>
              <div class="text-body-2 text-medium-emphasis">
                Converting file...
              </div>
            </div>
            <div
              v-else-if="status === 'error'"
              class="d-flex flex-column align-center justify-center h-100 text-center"
            >
              <v-icon
                icon="mdi-alert-circle-outline"
                color="error"
                size="32"
                class="mb-2"
              ></v-icon>
              <div class="text-body-2 text-error">
                {{ errorMessage }}
              </div>
            </div>
            <div v-else-if="status === 'success'">
              <div class="markdown-body" v-html="markdownContent"></div>
            </div>
            <div
              v-else
              class="d-flex flex-column align-center justify-center h-100 text-center"
            >
              <div class="text-body-2 text-medium-emphasis">
                Select a file to generate Markdown
              </div>
            </div>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              variant="elevated"
              prepend-icon="mdi-content-copy"
              >Copy to Clipboard</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { useConversion } from "../components/useConversion";
const { status, markdownContent, errorMessage, handleFileUpload } =
  useConversion();
</script>
