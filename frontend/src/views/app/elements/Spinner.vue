<template>
  <div class="d-flex justify-content-center" v-if="show">
    <div class="spinner-border" role="status">
      <span class="sr-only">Loading...</span>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      show: Boolean
    }
  };
</script>

<style>
</style>