<!-- src/App.vue -->
<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <a class="navbar-brand" href="/">Budget Planner</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Budget Planner</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/categories" class="nav-link">Category Manager</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<style>
/* You can include some global navigation styles here or in your assets/styles.css */
</style>