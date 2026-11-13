<template>
  <v-app>
    <v-main>
      <v-app-bar>
        <v-app-bar-title>
          <div class="d-flex align-center ga-2">
            <v-avatar rounded="0" image="/icon.png" />
            <span>QUACK PARSER</span>
          </div>
        </v-app-bar-title>
      </v-app-bar>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup></script>
