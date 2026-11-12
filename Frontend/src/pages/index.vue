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
              accept=".pdf,.docx,.pptx,.xlsx,.png,.jpg"
              hide-details
              @update:model-value="handleFileUpload"
            ></v-file-input>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-text class="overflow-auto" style="height: 400px">
            <div>
              <pre>{{ markdownContent }}</pre>
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
const { markdownContent, isLoading, handleFileUpload } = useConversion();
</script>
