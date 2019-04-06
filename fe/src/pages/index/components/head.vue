<template>
  <div>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-menu-item index="1"><router-link to="/">主页</router-link></el-menu-item>
      <el-menu-item index="1"><router-link to="/help">帮助</router-link></el-menu-item>
      <el-button type="primary" onclick="window.location='login.html'">登录/注册</el-button>
    </el-menu>
  </div>
</template>

<script>
    export default {
        name: "head"
    }
</script>

<style scoped>

</style>
