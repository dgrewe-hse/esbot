<template>
  <div id="app-root">
    <header class="app-header">
      <h1>ESBot</h1>
      <p class="tagline">AI-powered learning assistant</p>
    </header>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
</script>

<style>
*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  background: #f0f2f5;
  color: #1a1a2e;
}

#app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: #0a7ea4;
  color: #fff;
  padding: 0.75rem 1.5rem;
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.tagline {
  margin: 0.15rem 0 0;
  font-size: 0.85rem;
  opacity: 0.9;
}

main {
  flex: 1;
  padding: 1rem;
}
</style>
