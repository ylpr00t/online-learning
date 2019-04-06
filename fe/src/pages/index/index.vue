<template>
  <div>
    <headers></headers>
    <div class="content">
      <!--路由匹配到的结果渲染在这里-->
      <router-view></router-view>
      <footers></footers>
    </div>
  </div>
</template>

<script>
  import head from './components/head.vue'
  import foot from './components/foot.vue'
  export default {
    name: 'index',
    components: {
      headers: head,
      footers: foot,
    }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>



