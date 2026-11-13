<template>
  <v-app>
    <v-main>
      <v-app-bar>
        <div class="d-flex align-center pa-2">
          <v-avatar image="/icon.png" />
          <div class="d-flex flex-column justify-center">
            <div class="font-weight-bold">QUACK PARSER</div>
            <div class="text-caption text-disabled">
              Markdown Conversion via Docling
            </div>
          </div>
        </div>
      </v-app-bar>
      <router-view />
    </v-main>
  </v-app>
</template>
