<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-text>
            <v-file-upload
              density="compact"
              variant="compact"
              accept=".pdf,.docx,.pptx,.xlsx,.png,.jpg"
              title="Select File"
            >
            </v-file-upload>

            <v-sheet
              class="border rounded-lg pa-4"
              height="400"
              overflow="auto"
            >
              <div>Markdown output will appear here.</div>
            </v-sheet>

            <div class="d-flex justify-end">
              <v-btn color="primary">Copy to Clipboard</v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup></script>
