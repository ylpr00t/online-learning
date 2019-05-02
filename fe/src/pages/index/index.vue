<template>
  <div id="content-main">
    <div id="content-second">
      <headers></headers>
    </div>
    <footers></footers>
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
html,body,#content-main {
  width: 100%;
  height: 100%;
  background: #8cc5ff;
}
#content-main {
  width: 75%;
  background: #f0f0f0;
  margin-left: auto;
  margin-right: auto;
}
#content-second {
  height: 100%;
}
  footers {height:10px;margin-top:-20px;background-color: #ffc0cb;}
</style>



